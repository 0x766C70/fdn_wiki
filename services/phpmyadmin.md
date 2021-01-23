[[!meta title="phpMyAdmin"]]
  - Les bases de données sont accessibles via phpMyAdmin http://www.fdn.fr/phpmyadmin 8-)
  - Pour avoir les codes d'accès superadministrateur, faire, sur le serveur Web [[adminsys:serveurs:yoda]] :  ''cat /root/.my.cnf''
  - Pour créer un couple utilisateur+base, il faut aller dans ''Privilèges'' 8-) Attention à ne pas donner les droits globaux :-(
  - Pour qu'il ait les droits de se connecter a PHPMyAdmin, il faut donner les droits sur le serveur ''localhost''
Exemple de requêtes :
<code>
CREATE USER 'mdugenou'@'%' IDENTIFIED BY  '***';

GRANT USAGE ON * . * TO  'mdugenou'@'%' IDENTIFIED BY  '***' WITH MAX_QUERIES_PER_HOUR 0 MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0 ;

CREATE DATABASE IF NOT EXISTS  `mdugenou` ;

GRANT ALL PRIVILEGES ON  `mdugenou` . * TO  'mdugenou'@'%';

</code>
Fournir éventuellement les requêtes résultantes à l'usager demandeur 8-o