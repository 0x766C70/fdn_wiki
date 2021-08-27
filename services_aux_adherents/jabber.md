
FDN héberge un service XMPP pour les adhérents sur la [machine](./infra/machines/jyn.md) pour le domaine **[jabber.fdn.fr](https://jabber.fdn.fr/)**.

On utilise pour cela [prosody](https://prosody.im/) et les données sont stockées dans une base de données MariaDB.

## Configuration

Les fichiers de configuration sont dans `/etc/prosody` :

- **prosody.cfg.lua** : configuration principale ;
- **conf.d/jabber.fdn.fr.cfg.lua** : configuration du domaine **[jabber.fdn.fr](https://jabber.fdn.fr/)**

## Administration

### prosodyctl

Source : [prosodyctl](https://prosody.im/doc/prosodyctl)

- gestion process : `prosodyctl [status|start|stop|restart|reload]` ou `systemctl [status|start|stop|restart|reload] prosody`
- ajout d'un utilisateur : `prosodyctl adduser <user>@jabber.fdn.fr` puis fournir le mot de passe (2x)
- suppression d'un utilisateur : `prosodyctl deluser <user>@jabber.fdn.fr`

### telnet

Source : [console](https://prosody.im/doc/console)

L'accès via telnet en localhost pour l'administration est configuré : `telnet localhost 5582`.

- lister les utilisateurs : `user:list('jabber.fdn.fr')`
- lister les connexions avec d'autres serveurs : `s2s:show('jabber.fdn.fr')`
- lister les connexions clientes actuelles : `c2s:show('jabber.fdn.fr')`

## Troubleshooting

- logs prosody : **/var/log/prosody/prosody.log**
- logs mariadb : **/var/log/mysql/error.log**

### Impossible de se connecter

Prosody a besoin de se connecter à MariaDB pour vérifier l'authenticité d'un utilisateur. Il se peut que prosody ait été redémarré avant mariadb (notamment lors d'un reboot) ce qui provoque une erreur d'authentification. Pour régler cela il suffit de redémarrer prosody (`systemctl restart prosody`) après avoir vérifié que mariadb tournait bien (`systemctl status mariadb`).

Cf. logs prosody :

```
Mar 01 11:44:05 modulemanager	error	Error initializing module 'storage_sql' on 'jabber.fdn.fr': /usr/lib/prosody/modules/mod_storage_sql.lua:172: Failed to
 connect to database: Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2 "No such file or directory")
```
