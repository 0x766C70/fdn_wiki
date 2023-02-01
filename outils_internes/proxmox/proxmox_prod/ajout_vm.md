# Ajout d'une vm dans PVE

## Prérequis

Les entrées IPv4 et IPv6 doivent être renseignées dans le DNS avant de lancer le script

## id

Les VMs sous proxmox sont identifiées par un id qui doit être choisi (et unique), actuellement les deux derniers bytes de l'ipv4 sont utilisées comme id tels quels e.g. `tiree.fdn.fr` qui a pour IP 80.67.169.74 a comme id 169074

## scripts

Les scripts de déploiement sont dans un git disponible sur chaque hyperviseur, actuellement dans `/mnt/data/mkosi/`. Ils sont répliqués manuellement via *remote* croisé `git`. Donc s'il est mis à jour sur un des noeuds, il faut le mettre à jour également sur l'autre (`git push`).

Trois scripts sont prévus pour être lancés par des admins :
- `buildtemplate.sh` doit être lancé une fois de temps en temps, soit pour mettre à jour le template disque pour prendre les mises à jour d'une distro (et gagner du temps lors d'un nouveau déploiement), soit pour créer le template d'une nouvelle release/distro.
Le script postinst.sh lancé par mkosi devra probablement être adapté pour d'autres distro, mais son rôle principal est de lancer puppet une première fois pour avoir au moins les admins configurés. Il faudra valider le certificat de `template.fdn.fr` lors de la création d'un nouveau template, et ne pas oublier de le `cleanup` après pour le déploiement suivant.

- `buildvm.sh` qui déploie vraiment une VM à partir du tar créé précédement. Le script crée les disques qui correspondent dans la configuration demandée, y extrait le tar, configure le hostname/IP (partie à adapter pour d'autres distros éventuelles).
Ce script a besoin de l'IP pour la configurer dans l'image et pour décider de l'id de la VM, il faut donc que la machine soit préalablement déclarée dans les DNS.
La VM tournera sur l'hyperviseur sur lequel elle est lancée, et devra être migrée après si jugé utile.

- `copyvm.sh` qui permet de copier une vm (`tar`) **en fonctionnement** depuis n'importe où sur Proxmox. Ce script utilise le script `buildvm.sh` pour créer la vm sur Porxmox. Avant de le lancer, s'assurer d'avoir bien **arrêté** tous les services utiles de la vm (**puppet**, web, bases de données, dns, etc.), sinon les données ne seront pas consistantes entre l'ancienne et la nouvelle vm. Vu que **toutes** les données sont copiées, il n'y a pas besoin de s'occuper de `puppet` pour la nouvelle vm, néanmoins il est nécessaire de **couper** l'ancienne vm après la copie (avant le démarrage de la nouvelle vm) au risque de se retrouver avec deux vm avec la même adresse IP... :boom:

> Note : le paquet `lzop` doit être installé sur l'ancienne vm pour `copyvm.sh`

Les trois scripts sont configurable par variables d'environnement telles que définies en début de script :
```
# head buildvm.sh
DISTRO=${DISTRO:-debian}
RELEASE=${RELEASE:-buster}
TEMPLATE_ID=${TEMPLATE_ID:-} # empty = guess from 'template-$(hostname -s)'
MEM=${MEM:-2048} # in MB
CPU=${CPU:-2}
# DISKS cannot be passed as is: expect a string argument
declare -A DISKS=${DISKS:-( [/]=5G [/var]=10G )}
# same, expects something like DISKS_STORAGE="( [/srv]=gluster )"
declare -A DISKS_STORAGE=${DISKS_STORAGE:-( )}
DISKS_STORAGE_DEFAULT=${DISKS_STORAGE_DEFAULT:-gluster-ssl}

# head buildtemplate.sh
DISTRO="${DISTRO:-debian}"
RELEASE="${RELEASE:-buster}"
EXTRA_PKGS="${EXTRA_PKGS:-puppet,vim,lsb-release,iproute2,openssh-server,ifupdown,qemu-guest-agent,grub2,linux-image-amd64}"
```

## exemples

```
# DISKS="( [/]=5G [/var]=10G [/srv]=40G)" DISKS_STORAGE="( [/srv]=gluster )" ./buildvm.sh tiree.fdn.fr
# MEM=4096 ./buildvm.sh mail.test.fdn.fr
# sudo DISKS="( [/]=5G [/var]=10G [/var/opt/gitlab]=15G [/var/opt/gitlab/backups]=5G)" CPU=4 MEM=4096 ./buildvm.sh git.test.fdn.fr
```

## après buildvm.sh

*  puppet est installé et configuré en même temps que la création de la VM (chouette)
*  une autre passe puppet après l'installation permet de descendre les config spécifiques de la VM ainsi que toute la config de base, quelques étapes pour que cela fonctionne :

0. (uniquement si le même nom de VM existait avant, donc dans le cas d'une re-installe, et :warning: à faire avant cette re-install) @palpatine : `puppetserver ca clean --certname xxx.fdn.fr` (repertoire `/opt/puppetlabs/server/apps/puppetserver/bin`)
1. @palpatine : `puppetserver ca list` puis `puppetserver ca sign --certname xxx.fdn.fr` (repertoire `/opt/puppetlabs/server/apps/puppetserver/bin`)
2. @vm : `etckeeper commit -m "first pass puppet"` (sans cela, puppet ne (re)passera pas)
3. la VM fraîchement créée va lancer puppet après une minute ou deux automatiquement lors de son prochain test de certificat vers palpatine (si vraiment pressé : `puppet agent -t` sur la VM)
