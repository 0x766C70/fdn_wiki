*Cette page présente la configuration MySQL sur l'infra FDN.*

# MySQL

**Brouillon à compléter...**

Le serveur maître est celui qui héberge le SI, actuellement il s'agit de [[adminsys:serveurs:si]].
Les serveurs esclaves récupèrent l'information depuis le maître directement (pas de cascade).

Pour éviter de s'emmêler les pieds dans les fibres, le ''server-id'' (''my.cnf'') est déterminé en prenant le dernier octet de l'adresse IP principale de la machine qui héberge le serveur (pour le bloc 80.67.169.0/25 normalement).  En dehors de ce bloc, il faudra trouver une autre convention (c'est un entier 32 bits non signé, il y a de la marge).

[[http://dev.mysql.com/doc/refman/5.0/fr/replication-howto.html|Documentation MySQL 5.0 (français)]]

## Server maître

### Configuration

#### my.cnf

  * Lui mettre un ''server-id'', sans ça, les esclaves refuseront de se connecter à lui.
  * Il faut activer le bin-log (journal binaire), qui contient toutes les modifications des données, et qui est lu par l'esclave.
  * Il est possible de filtrer quelles bases de données sont dans le binlog (''binlog-do-db''), mais ce n'est pas filtré sur vador.

Et redémarrer le serveur après avoir modifié ces paramètres.

#### Droits d'accès

    mysql> GRANT REPLICATION SLAVE ON *.* TO user@'host' IDENTIFIED BY 'password';
  
où

  * ''*.*'' est le pattern de base de données autorisés (vu que tout est dans le binlog de vador, j'ai gardé la même valeur pour les LNS),
  * ''user'' le nom d'utilisateur utilisé par l'esclave pour se connecter au maître,
  * ''host'' l'adresse IP utilisée par l'esclave lorsqu'il se connecte au maître (obtenue via ''ip route get 80.67.169.40'' par exemple)
  * ''password'', le mot de passe de l'utilisateur précédemment mentionné.


## Serveur esclave


### Configuration

#### my.cnf

  * Lui mettre un ''server-id'', différent des autres (attention aux gestionnaires de configuration)
  * Activer les logs (pas obligatoire), peut se faire en décommentant les deux lignes general_log{_file,}
  * Ajouter les filtres db/table pour le strict nécessaire.

À titre d'exemple, un extrait du my.cnf de [[:adminsys:serveurs:lns02]] :
    server_id               = 42
    replicate_do_db         = adsl
    replicate_do_table      = adsl.RADUSER
    replicate_do_table      = adsl.UATTR
    replicate_do_table      = adsl.GATTR

Ensuite on arrête le serveur mysql
    service mysql stop

#### /var/lib/mysql

Il faut ensuite importer la base de données si c'est pas déjà fait.

**Attention**, pour garantir la cohérence des données, il faut bien faire chaque étape.

== Sur le maître ==

1. Verrouiller toutes les bases et toutes les tables :
    mysql> FLUSH TABLES WITH READ LOCK;

2. Copier les fichiers de la base qui vous intéresse
    root@maitre # tar cvzf mysql-dump-replication.tar.gz -C /var/lib/mysql ./adsl

3. Noter l'état actuel du maitre
    mysql> show master status;
    +------------------+----------+--------------+------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
    +------------------+----------+--------------+------------------+
    | mysql-bin.003327 |      630 |              |                  | 
    +------------------+----------+--------------+------------------+
    1 row in set (0.00 sec)

4. Déverrouiller les tables
    mysql> UNLOCK TABLES;

== Sur l'esclave ==

Se démerder pour y tranférer l'archive mysql-dump-replication.tar.gz, et la décompresser dans /var/lib/mysql
    root@esclave # tar xvzf mysql-dump-replication.tar.gz -C /var/lib/mysql
  
Relancer la base de données
    root@esclave # service mysql start
  
Se connecter à la base de données
    root@esclave # mysql --defaults-file=/etc/mysql/debian.cnf # That's a hack
  
Dégager les tables inutiles, i.e. celle qui sont pas en ''replicate-do-table''
    mysql> \u adsl
    mysql> DROP TABLE ADHACCESS, ADRESSE, CLIENT, CLIENTINFO, CLOTURE, COMPTA, CONVOCATION, CREANCE, DEBIT, DEPLOIEMENT, DOMAINE, DON, ELIGIBILITE, EVENT, FACTURE, INFO, IPADDR, LIGNE, LIGNEINFO, MANDAT, MAPVIL, NEWINFO, NOTIF, ORDRETD, PAIEMENT,  PAYANT, PLUTAR, PRELEVEMENT, PRIXDEBIT, PRIX, PRLBQ, PRLLIG, PRLLIGSEPA, PROPEVENT, PROPPLUTAR, RUN, SEQ, SITE, STAT, TARIF, TASK, TASKSELF, TVADCL, TVA, UNIXGROUP, UNIXUSER, UNIXUSERUNIXGROUP, VALIDATION, VPN, VPNINFO, WAITING;

Vérifier qu'il n'y a plus que les tables nécessaires:
    mysql> SHOW TABLES;
  
#### Esclavage

Une fois la base de données propre, on peut démarrer l'esclavage.
    mysql> CHANGE MASTER TO
    master_host='80.67.169.40',
    master_user='<user>',
    master_password='<password>',
    master_log_file='mysql-bin.003327',
    master_log_pos=630;
    
En prenant les valeurs positionnées lors du ''GRANT REPLICATION SLAVE'' et du ''SHOW MASTER STATUS''.

Banzai :
    mysql> START SLAVE;
    mysql> SHOW SLAVE STATUS;

Si tout va bien, la première valeur renvoyée par la dernière commande devrait être quelque chose comme ''Waiting for master to send event'' (colonne Slave_IO_STATE).

## Remplacement du maître suite au déménagement du SI

Suite au déménagement du SI de [[adminsys:serveurs:vador]] vers [[adminsys:serveurs:si]], les bases de données ne sont plus répliquées - tous les nouveaux adhérents se voient refuser l'accès au service.

Pour restaurer la synchronisation, il faut activer le maître sur si et changer la configuration des esclaves sur les lns.

== Sur le nouveau maître ==

  * On créé un backup de la conf MySQL :
    <code>
    john@si:~$ cd /etc/mysql/
    john@si:/etc/mysql$ sudo cp my.cnf my.cnf.orig.20141221
    </code>


  * On attribue un server-id au maître (le dernier octet de son IP par convention) et on active le log binaire nécessaire à la réplication :
    <code>
    john@si:/etc/mysql$ sudo nano my.cnf
    --
    # Dernier octet de l'adresse IP
    server-id = 63
    log_bin   = /var/log/mysql/mysql-bin.log
    --
    </code>


  * On redémarre le serveur MySQL :
    <code>
    john@si:/etc/mysql$ sudo service mysql restart
    </code>


  * N'ayant pas les mots de passe actuels à disposition, on va re-créér un utilisateur de réplication. Une autre solution aurait été de changer le mot de passe, mais sans savoir s'il y a des éventuels effets de bord, j'ai choisi de jouer la sécurité.
    <code>
    john@si:/etc/mysql$ mysql -u root -p
    --
    Création de l'utilisateur :
    mysql> CREATE USER 'dbrepl'@'lns0%.fdn.fr' IDENTIFIED BY '<mot de passe>';
    
    Attribution des droits de réplication :
    mysql> GRANT REPLICATION SLAVE ON *.* TO 'dbrepl'@'lns0%.fdn.fr';
    
    Rafraîchissement des droits au niveau du serveur :
    mysql> FLUSH PRIVILEGES;
    
    Verrouillage des tables en lecture :
    mysql> FLUSH TABLES WITH READ LOCK;
    
    Vérification de l'activation du serveur maître :
    mysql> SHOW MASTER STATUS;
    +------------------+----------+--------------+------------------+
    | File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
    +------------------+----------+--------------+------------------+
    | mysql-bin.000001 |      460 |              |                  |
    +------------------+----------+--------------+------------------+
    
    Fini pour l'instant :
    mysql> quit
    --
    </code>


  * On crée une copie initiale des données à répliquer :
    <code>
    john@si:/etc/mysql$ mysqldump adsl RADUSER UATTR GATTR --add-drop-table -u root -p > mysql-lns.sql
    </code>


  * On libère les tables en écriture :
    <code>
    john@si:/etc/mysql$ mysql -u root -p
    --
    mysql> UNLOCK TABLES;
    
    mysql> quit
    --
    </code>


  * On récupère la copie des tables MySQL qu'il va falloir restaurer sur les LNS :
    <code>
    $ scp si.fdn.fr:mysql-lns.sql .
    </code>


  * Terminé pour le maître, on passe aux esclaves.

== Sur chaque esclave ==

  * On transfère la copie des tables MySQL :
    <code>
    $ scp mysql-lns.sql lns01.fdn.fr:
    </code>


  * Là non plus, les mots de passe ne sont pas connus - on va donc tricher en utilisant l'utilisateur de maintenance créé par l'installation Debian. Son mot de passe est stocké dans le fichier /etc/mysql/debian.cnf.

  * On fait une copie de sauvegarde de la base (disaster recovery) :
    <code>
    john@lns01:~$ mysqldump --all-databases --add-drop-database -u debian-sys-maint -p > mysql.sql
    </code>


  * On restaure les tables que l'on a sauvegardé précedemment sur le maître :
    <code>
    john@lns01:~$ mysql -u debian-sys-maint -p adsl < mysql-lns.sql
    </code>


  * On change les coordonnées du maître sur le serveur esclave :
    <code>
    john@lns01:~$ mysql -u debian-sys-maint -p
    --
    Arrêt de l'esclave :
    mysql> STOP SLAVE;
    
    Réinitialisation de l'esclave (nécessaire car on repart sur un nouveau log binaire) :
    mysql> RESET SLAVE;
    
    Configuration du nouveau maître (le fichier de log et sa position nous ont été fournis par le statut du maître) :
    mysql> CHANGE MASTER TO MASTER_HOST='si.fdn.fr', MASTER_USER='dbrepl', MASTER_PASSWORD='<mot de passe>', MASTER_LOG_FILE='mysql-bin.000001', MASTER_LOG_POS=460;
    
    Démarrage de l'esclave :
    mysql> START SLAVE;
    
    Vérification du statut de l'esclave :
    mysql> SHOW SLAVE STATUS;
    +----------------------------------+-------------+-------------+-------------+---------------+------------------+---------------------+-------------------------
    +---------------+-----------------------+------------------+-------------------+-----------------+---------------------+------------------------------------+---
    ---------------------+-------------------------+-----------------------------+------------+------------+--------------+---------------------+-----------------+-
    ----------------+----------------+---------------+--------------------+--------------------+--------------------+-----------------+-------------------+---------
    -------+-----------------------+-------------------------------+---------------+---------------+----------------+----------------+-----------------------------+
    ------------------+
    | Slave_IO_State                   | Master_Host | Master_User | Master_Port | Connect_Retry | Master_Log_File  | Read_Master_Log_Pos | Relay_Log_File          
    | Relay_Log_Pos | Relay_Master_Log_File | Slave_IO_Running | Slave_SQL_Running | Replicate_Do_DB | Replicate_Ignore_DB | Replicate_Do_Table                 | Re
    plicate_Ignore_Table | Replicate_Wild_Do_Table | Replicate_Wild_Ignore_Table | Last_Errno | Last_Error | Skip_Counter | Exec_Master_Log_Pos | Relay_Log_Space | 
    Until_Condition | Until_Log_File | Until_Log_Pos | Master_SSL_Allowed | Master_SSL_CA_File | Master_SSL_CA_Path | Master_SSL_Cert | Master_SSL_Cipher | Master_S
    SL_Key | Seconds_Behind_Master | Master_SSL_Verify_Server_Cert | Last_IO_Errno | Last_IO_Error | Last_SQL_Errno | Last_SQL_Error | Replicate_Ignore_Server_Ids |
     Master_Server_Id |
    +----------------------------------+-------------+-------------+-------------+---------------+------------------+---------------------+-------------------------
    +---------------+-----------------------+------------------+-------------------+-----------------+---------------------+------------------------------------+---
    ---------------------+-------------------------+-----------------------------+------------+------------+--------------+---------------------+-----------------+-
    ----------------+----------------+---------------+--------------------+--------------------+--------------------+-----------------+-------------------+---------
    -------+-----------------------+-------------------------------+---------------+---------------+----------------+----------------+-----------------------------+
    ------------------+
    | Waiting for master to send event | si.fdn.fr   | dbrepl      |        3306 |            60 | mysql-bin.000001 |                 460 | mysqld-relay-bin.000002 
    |           253 | mysql-bin.000001      | Yes              | Yes               | adsl            |                     | adsl.GATTR,adsl.RADUSER,adsl.UATTR |   
                         |                         |                             |          0 |            |            0 |                 460 |             410 | 
    None            |                |             0 | No                 |                    |                    |                 |                   |         
           |                     0 | No                            |             0 |               |              0 |                |                             |
                   63 |
    +----------------------------------+-------------+-------------+-------------+---------------+------------------+---------------------+-------------------------
    +---------------+-----------------------+------------------+-------------------+-----------------+---------------------+------------------------------------+---
    ---------------------+-------------------------+-----------------------------+------------+------------+--------------+---------------------+-----------------+-
    ----------------+----------------+---------------+--------------------+--------------------+--------------------+-----------------+-------------------+---------
    -------+-----------------------+-------------------------------+---------------+---------------+----------------+----------------+-----------------------------+
    ------------------+
    </code>


  * La position actuelle correspond au statut du maître et il est bien en attente d'évènements, c'est tout bon. :-) On pourra vérifier que la synchronisation fonctionne après l'ajout d'un nouveau compte par exemple.

## Monitoring

Sur les serveurs esclaves, on utilise un plugin externe http://www.claudiokuenzler.com/nagios-plugins/check_mysql_slavestatus.php

Le plugin vérifie plusieurs éléments : Que mysql tourne, que la connexion vers le maitre est active, et le retard par rapport au maitre.

La sortie du plugin est typiquement :

    OK: Slave SQL running: Yes Slave IO running: Yes / master: 80.67.169.40 / slave is 0 seconds behind master

La configuration nécessite un user nagios qui a le droit de lire le statut de l'esclave

    mysql> GRANT REPLICATION CLIENT on *.* TO 'nagios'@'localhost' IDENTIFIED BY 'secret';
  
(Le mot de passe est dans le fichier nrpe_local.cfg, le même pour les LNS et vador).

### Installation initiale du serveur :
**Ce chapitre est probablement obsolète** 8-O
  * installation de mysql 4.1 (mysql-server-4.1)

    => mdp root : yi5aeGho
    => /root/.my.cnf

  * installation de php4 (php4, php4-mysql)

    => vérifier /etc/apache-ssl/conf.d/modules que le module PHP4 soit bien chargé
    => vérifier /etc/php4/apache/php.ini que le module mysql soit bien chargé
