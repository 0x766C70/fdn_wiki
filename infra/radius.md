## RADIUS

* freeradius3

## Migration des configurations 2 => 3

Tous les anciens modules qui étaient dans le fichier "radiusd.conf" ont été migrés dans le dossier "mods-avaible".

Le fichier "sql.conf" a été migré dans le fichier de module "sql".

Toute la configuration lié au AAA de freeradius est désormais dans un VHOST (server) pour se rendre conforme à la version 3.

## Fichiers de configs

* radiusd.conf : Configuration général de freeradius,
* proxy.conf : Liste des RADIUS distant pour valider un user,
* clients.conf : Liste des serveur qui peuvent consulter le radius,
* users1 et users2 : Liste des utilisateurs locaux pour le radius,
* huntgroups : Défini le groupe selon l'adresse IP du serveur.
