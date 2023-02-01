# Proxmox - cluster de backup

## Présentation

- serveurs :
  - **c3px** : 4 disques rotatifs, `/boot` en *raid1*, `/` en *raid10*, restant au sein d'un pool ZFS *tank* en *raidz1* (*raid5*)
  - **r4p17** : 4 disques rotatifs, `/boot` en *raid1*, `/` en *raid10*, restant au sein d'un pool ZFS *tank* en *raidz1* (*raid5*)
- version PVE : **7**
- URLs :
  - https://c3px.fdn.fr:8006
  - https://r4p17.fdn.fr:8006

Ce cluster ne contient qu'une seule machine virtuelle, *scarif*, hébergeant Proxmox Backup Server (PBS) pour stocker les sauvegardes des machines virtuelles du cluster de **prod**

## Buildbook

Pour avoir une idée de comment le cluster a été installé et configuré, jeter un oeil au [buildbook](/infra/new.droides/buildbook.md)

:warning: :warning: :warning: il y a boire et à manger dans cette vieille doc.

## Configuration

### Utilisateurs

Cf. *Datacenter > Permissions > Users*.

PVE permet plusieurs systèmes d'authentification, dont notamment (cf. *Datacenter > Permissions > Realms*) :
- *Linux PAM standard authentication* : utilise les comptes unix configurés sur chaque noeud ;
- *PVE authentication serveur* : base de données gérée par PVE.

FDN utilise principalement l'authentification PAM pour permettre la connexion à l'IHM de PVE. Les comptes unix sont gérés via `puppet` comme sur les autres serveurs. Le serveur d'authentification PVE peut -être utile pour donner accès à des personnes n'ayant pas de compte unix (déconseillé).

Il est recommandé d'associer chaque utilisateur à un groupe d'utilisateurs, pour simplifier la gestion des autorisations au niveau des machines virtuelles. Essayer autant que faire se peut d'utiliser les mêmes groupes que ceux utilisés dans `puppet` pour la gestion des utilisateurs.

Ce cluster ne contenant qu'une vm administrée par les admincore, pour rajouter les droits à un admincore il suffit de le rajouter dans PVE au groupe **noyau**.

### Stockage

Cf. *Datacenter > Storage* :
- **local** : ???
- **zfs** : machines virtuelles et données associées

### Sauvegardes de la vm

*scarif* n'est pas sauvegardée. En cas de gros problème il faut la réinstaller.


### Réplication

*scarif* est répliqué sur l'autre noeud toutes les deux heures, histoire de pouvoir remonter le service si un des noeuds tombe.

### Firewall

Cf. *Datacenter > Firewall > Options*

PVE permet de gérer un firewall directement au niveau du cluster. FDN n'a pas chois cette option. Le firewall est géré sur chaque noeud de la même manière que sur les autres machines, c'est à dire via `puppet`.

## Utilisation

### Création d'une vm

Comme pour la **prod**, des scripts de création de machine virtuelle sont disponibles à `/mnt/zfs/mkosi`, mais contrairement à la **prod** il ne sont pas répliqués sur l'autre noeud car pour l'instant il n'est pas prévu de créer d'autres machines virtuelles sur ce cluster. Voir la [procédure](./proxmox_prod/ajout_vm.md) détaillée de la **prod**, adaptée, en cas de réel besoin.

### Bascules des VMs

L'interface proxmox permet de faire des bascules de VM en masse (typiquement avant les mises à jour).

### Snapshots

Il est possible de faire des mises à jour de *scarif*, comme n'importe quelle vm.

Il faut savoir que les snapshots empêchent de faire des manipulation sur les disques (tels qu'agrandissement) et qu'un snapshot consomme des ressources, donc ceux-ci sont à supprimer une fois l'action pour laquelle ils avaient été faits est terminée.

## Maintenance

### reboot

Les disques des VMs sont sur des partitions chiffrées, il faut donc les déchiffrer après démarrage avec le script `/root/start-zfs-datastore.sh` qui vous demandera le mot de passe luks et déchiffrera les disques.

### Mise à jour

Pour mettre à jour le cluster PVE, il faut mettre à jour chaque noeud l'un après l'autre.

Il est possible de le faire via l'interface web en théorie (*[noeud] > Updates*) mais il est recommandé de le faire en CLI pour éviter tout effet de bord avec l'IHM, qui pourrait également être mise à jour en même temps.

Macro-procédure :
- sur chaque noeud :
  1. migrer les vms sur l'autre noeud
  1. mettre à jour le noeud : `apt update && apt upgrade`
  1. redémarrer le serveur (cf. ci-dessus)
- rééquilibrer les machines virtuelles sur les deux noeud (cf. ci-dessus)
