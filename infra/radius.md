# RADIUS

Configuration des serveurs freeradius3

## Fichiers de configs

Toute la conf est dans puppet, répartie dans les fichiers suivants:

* radiusd.conf : Configuration général de freeradius,
* proxy.conf : Liste des RADIUS distant pour valider un user,
* clients.conf : Liste des serveur qui peuvent consulter le radius,
* users1 et users2 : Liste des utilisateurs locaux pour le radius,
* huntgroups : Défini le groupe selon l'adresse IP du serveur.
* mods-available : Configs spécifiques à certains modules (par exemple sql)

### Migration des configurations 2 => 3

Tous les anciens modules qui étaient dans le fichier "radiusd.conf" ont été migrés dans le dossier "mods-avaible".

Le fichier "sql.conf" a été migré dans le fichier de module "sql".

Toute la configuration lié au AAA de freeradius est désormais dans un VHOST (server) pour se rendre conforme à la version 3.

## replication mysql

### setup

* sur SI

```
create user 'dbrepl_radius0'@'radius0.fdn.fr' identified  by 'XXX';
grant replication slave on *.* to 'dbrepl_radius0'@'radius0.fdn.fr';
show master status;
```
-> Retenir le `File` et `Position` pour l'ajout du slave, puis prendre un dump:
```
mysqldump adsl GATTR IPADDR RADUSER UATTR > dump
```

* sur radius0

Verifier /etc/mysql/conf.d/replicat.conf: server-id (note ip) et filtre sur les tables (normalement fait par puppet)

Reprendre un dump, créer l'user pour radius. Le mdp pour radius est dans le fichier `/etc/freeradius/3.0/mods-enabled/sql`
```
$ mysql
CREATE DATABASE adsl
GRANT SELECT ON adsl.* TO 'l2tpns'@'localhost' IDENTIFIED BY '<mdp>';
$ mysql adsl <dump
```

Bien remplacer les valeurs de `master_log_file='mysql-bin.002579', master_log_pos=8563083` à File/Position du show master status.

```
stop slave; (si update, peut être utile pour replacer master_log_pos par exemple après une erreur)
change master to master_host='80.67.169.63', master_user='dbrepl_radius0', master_password='XXX', master_log_file='mysql-bin.002579', master_log_pos=8563083;
start slave;
```

### verifs

* sur SI

```
show grants for 'dbrepl'@'lns0%.fdn.fr'
show master status;
show slave hosts;
```

* sur radius0

```
show slave status;
```

* comparer:
** le `Read_Master_Log_Pos` au `Position` du master
** le `Relay_Master_Log_File` au `File` du master
** Aussi juste comparer la table UATTR par exemple (par exemple juste le nombre de lignes pour faire simple: `use adsl; select count(*) from UATTR;`)
