# Proxmox Backup Server

## Présentation

Les machines virtuelles du cluster de **prod** sont sauvegardées sur le cluster de **backup**, via la solution Proxmox Backup Server (PBS) installée sur la machine virtuelle *scarif*.

PBS est capable non seulement de sauvegarder facilement les machines virtuelles et conteneurs qui tournent sous PVE, mais également n'importe quel serveur sur lequel peut être installé le [client Proxmox Backup](https://pbs.proxmox.com/docs/installation.html#client-installation).

## PBS et configuration

### Scarif

Machine virtuelle sur le cluster de **backup**, avec 3 disques : `/` (5Go) pour le système, `/var` (10 Go) et `/mnt/backups` où sont stockées les données sauvegardées. Cette vm est répliquée toutes les deux heures sur le deuxième noeud du cluster.

### Accès

Seuls les admincore ont actuellement accès à PBS :
- URL : https://pbs.fdn.fr:8007/
- identifiant : identifiant admincore
- mot de pasee : mot de passe admincore
- royaume : Linux PAM standard authentication

Pour configurer les accès : *Configuration > Access Control*

Il existe un utilisateur spécial, **pve-bot**, configuré sur le royaume **pbs** et utilisé pour effectuer les sauvegardes depuis le PVE de **prod** (voir plus bas).

### Datastores

C'est le stockage virtuel sur lequel sont stockés les donnés sauvegardées. À ce jour un seul datastore **backups** configuré sur `/mnt/backups`.

Pour chaque datastore, on a accès aux informations suivantes :
- *Summary* : statisques d'utilisation du datastore
- *Content* : sauvegardes stockées par machine sauvegardée sous forme `<type>/<id>`. Il est possible de voir les différentes sauvegardes pour chaque machine en cliquant sur le `+`
- *Prune & GC* : décider quelles sauvegardes on souhaite conserver et faire le ménage. Actuellement on conserve par défaut, pour chaque machine : les 6 dernières qutotidiennes, les 3 dernières hebdomadaires et la dernière mensuelle. Ce nettoyage est effectué tous les jours. 
- *Sync jobs* : il est possible de synchroniser ces sauvegardes sur un autre serveur PBS si besoin. Ce n'est pas le cas pour nous (cf. réplication de la vm).
- *Verify jobs* : scan d'intégrité des backups, effectué quotidiennement.
- *Options* : adresse mail à notifier, raisons de notifcation, vérification des nouvelles sauvegardes (désactivé car demande beaucoup d'accès disque et fait foirer les sauvegardes pour cause de timeout et vérif quotidienne activéee cf. ci-dessus)
- *Permissions* : qui a accès spécifiquement à ce datastore, c'est là qu'on retrouve notamment **pve-bot**.

## PVE

### Configuration et sauvegardes

cf. *Cluster > Storage*

Storage **pbs** configuré avec l'utilisateur **pve-bot@pbs** pour accéder au datastore **backups** (cf. ci-dessus).

Les vms sauvegardées sont configurées dans *Cluster > Backup*, tous les jours à 3h en mode *snapshot*. Toutes les vms ne sont pas sauvegardées : par exemple seule **vpn1** est sauvegardée, aucune vm de tests ni templates, etc.

Pour connaître l'espace disponible sur le datastore **backups** : *Cluster > node > pbs*.

 ### Sauvegardes

Il existe deux modes principaux de sauvegarde :
- mode *snapshot* : les vm ne sont pas éteintes, ie sauvegarde *à chaud* ;
- mode *stop* : les vms sont éteintes, sauvegardées puis redémarrées, ie sauvegarde *à froid*.

Il est à noter que certaines vielles vm, comme **ackbar**, ne peuvent être sauvegardées en mode *snapshot*, parce que les OS ne comprennent pas les commandes `qemu` envoyées par PVE. À la mise en place des sauvegardes une première sauvegarde à froid a été effectuée et est disponible sur PBS. Si on veut sauvegarder de nouveau ces vm il suffit de les arrêter, lancer la sauvegarde manuellement puis les relancer.

Pour connaître le statut de sauvegarde d'une vm, voir *vm > Backup* : y réside la liste des sauvegardes pour ces vms ainsi que leur état de vérification. En général la dernière sauvegarde n'a pas été vérifiée et c'est normal vue la configuration de PBS (voir plus haut).

Il est possible de lancer une sauvegarde manuelle d'une vm, cf. *vm > Backup > Backup now* : choisir le mode sauvegarde puis *Backup*.

Note : une sauvegarde va aller stocker les données sur le cluster de **backup** et celle-ci sera donc conservée. À contrario, un *snapshot* ne sera fait que sur le cluster de **prod** et permettra de revenir à un état précédent pré-enregistré : la finalité de ces deux fonctionnalités n'est pas la même ;)

### Restoration

Pour restorer une vm depuis une sauvegarde : *vm > Backup*, puis sélection d'une sauvegarde, puis *Restore*, puis suivre les instructions.

TODO: tester *File Restore* et écrire la doc idoine.
