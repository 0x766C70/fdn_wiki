# Proxmox - cluster de prod

## Présentation

- serveurs :
  - **tc14** : 4 disques, `/boot` en *raid1*, `/` en *raid5*, restant ausein d'un pool ZFS *storage* en *raid10*
  - **r5d4** : 4 disques, `/boot` en *raid1*, `/` en *raid5*, restant ausein d'un pool ZFS *storage* en *raid10*
- version PVE : **7**
- URLs :
  - https://tc14.fdn.fr:8006
  - https://r5d4.fdn.fr:8006

## Buildbook

Pour avoir une idée de comment le cluster a été installé et configuré, jeter un oeil au [buildbook](/infra/new.droides/buildbook.md)

:warning: :warning: :warning: il y a boire et à manger dans cette vieille doc. Par exemple à l'origine on utilisait `gluster` pour le stockage des vms : ce n'est plus le cas depuis le passage à ZFS

## Configuration

### Utilisateurs

Cf. *Datacenter > Permissions > Users*.

PVE permet plusieurs systèmes d'authentification, dont notamment (cf. *Datacenter > Permissions > Realms*) :
- *Linux PAM standard authentication* : utilise les comptes unix configurés sur chaque noeud ;
- *PVE authentication serveur* : base de données gérée par PVE.

FDN utilise principalement l'authentification PAM pour permettre la connexion à l'IHM de PVE. Les comptes unix sont gérés via `puppet` comme sur les autres serveurs. Le serveur d'authentification PVE peut -être utile pour donner accès à des personnes n'ayant pas de compte unix (déconseillé).

Il est recommandé d'associer chaque utilisateur à un groupe d'utilisateurs, pour simplifier la gestion des autorisations au niveau des machines virtuelles. Essayer autant que faire se peut d'utiliser les mêmes groupes que ceux utilisés dans `puppet` pour la gestion des utilisateurs.

Les autorisations sont gérées grâces à des rôles (*Datacenter > Permissions > Roles*). Les rôles configurés sont ceux de base de PVE, plus le rôle **benevoleVM** dont le but est de permettre à un adminsys de gérer de manière autonome les machines virtuelles dont il a la charge.

Pour donner des accès à un utilisateur pour une certaine machine virtuelle, deux options :
1. (recommandée) dans *[vm] > Permissions*, ajouter une autorisation en créant une association entre un groupe d'utilisateur dont fait partie cet utilisateur et un rôle
1. dans *[vm] > Permissions*, ajouter une autorisation en créant une association entre cet utilisateur et un rôle

Exemples :
1. Un admincore ayant un accès à un noeud n'est pas automatiquement administrateur de PVE : pour cela, il suffit d'ajouter cet utilisateur au groupe **noyau**. Cet ajout se fait au niveau de l'utilisateur, et non du groupe.
1. Un adminsys veut pouvoir administrer la machine *nitter*. Au niveau des permissions de la vm, on voit qu'il y a déjà une association **@privacy-admin/benevoleVM**, ie entre le groupe **privacy-admin** et le rôle **benevoleVM**. Deux options s'offrent à nous :
  - rajouter l'utilisateur au groupe **privacy-admin** : il aura alors automatiquement les droits **benevoleVM** non seulement sur cette vm, mais également sur toutes les vm ayant les même permissions, par exemple *invidious*.
  - rajouter une autorisation **benevolesVM** pour cet utilisateur uniquement.

### Stockage

Cf. *Datacenter > Storage* :
- **local** : ???
- **data** : machines virtuelles et données associées
- **pbs** : cluster PVE de backup

### Sauvegardes des vms

Cf. *Datacenter > Backup* : les machines virtuelles sont presque toutes sauvegardées tous les jours à 3h du matin, sur le cluster de backup PBS.

Certaines vm ne le sont pas car trop vieilles ou ce n'est pas nécessaire.


### Réplication

Cf. *Datacenter > Replication* : pour permettre la continuité des services en cas de perte d'un noeud du cluster, les machines virtuelles sont répliquées toutes les deux heures sur l'autre noeud. 

### Firewall

Cf. *Datacenter > Firewall > Options*

PVE permet de gérer un firewall directement au niveau du cluster. FDN n'a pas chois cette option. Le firewall est géré sur chaque noeud de la même manière que sur les autres machines, c'est à dire via `puppet`.

## Utilisation

### Création d'une vm

Voir la [procédure](./proxmox_prod/ajout_vm.md) détaillée.

### Bascules des VMs

L'interface proxmox permet de faire des bascules de VM en masse (typiquement avant les mises à jour).

Il n'y a malheureusement visiblement pas de moyen simple de se souvenir d'une configuration "optimale", donc au moment de remettre en place prendre simplement en gros la moitié des VMs en évitant de regrouper les VMs d'un service particulier (e.g. une dns de chaque côté)

Pour tout ce qui est routé (VPNs...), la convention pour avoir des chemins optimaux dans nos configurations est de mettre les VMs *paires* sur tc14 et *impaires* sur r5d4.

### Snapshots

La plupart des VMs peuvent prendre des snapshots dans l'interface.

Il faut savoir que les snapshots empêchent de faire des manipulation sur les disques (tels qu'agrandissement) et qu'un snapshot consomme des ressources, donc ceux-ci sont à supprimer une fois l'action pour laquelle ils avaient été faits est terminée.

S'il faut les garder longtemps, vous voulez des backups!

## Maintenance

### reboot

Les disques des VMs sont sur des partitions chiffrées, il faut donc les déchiffrer après démarrage avec le script `/root/start-zfs-datastore.sh` qui vous demandera le mot de passe luks et déchiffre les disques.

### Mise à jour

Pour mettre à jour le cluster PVE, il faut mettre à jour chaque noeud l'un après l'autre.

Il est possible de le faire via l'interface web en théorie (*[noeud] > Updates*) mais il est recommandé de le faire en CLI pour éviter tout effet de bord avec l'IHM, qui pourrait également être mise à jour en même temps.

Macro-procédure :
- sur chaque noeud :
  1. migrer les vms sur l'autre noeud
  1. mettre à jour le noeud : `apt update && apt upgrade`
  1. redémarrer le serveur (cf. ci-dessus)
- rééquilibrer les machines virtuelles sur les deux noeud (cf. ci-dessus)
