# Proxmox

Gestion d'hyperviseur

# Maintenance
## Bascules des VMs

L'interface proxmox permet de faire des bascules de VM en masse (typiquement avant les mises à jour).

Il n'y a malheureusement visiblement pas de moyen simple de se souvenir d'une configuration "optimale",
donc au moment de remettre en place prendre simplement en gros la moitié des VMs en évitant de regrouper
les VMs d'un service particulier (e.g. une dns de chaque côté)

Pour tout ce qui est routé (VPNs...), la convention pour avoir des chemins optimaux dans nos configurations
est de mettre les VMs *paires* sur tc14 et *impaires* sur r5d4.



## reboot

Les disques des VMs sont sur des partitions chiffrées, il faut donc les déchiffrer après
démarrage avec le script `/root/start-gluster.sh` qui vous demandera le mot de passe luks et:
 - déchiffre les disques
 - monte les partitons
 - démarre gluster
 - démarre le raid10 pour les VMs locales


## Mises à jour

Principalement pour gluster, il faut faire très attention aux mises à jour, en particulier
absolument attendre une resynchro entre la mise à jour de chaque hyperviseur.

```shell
# optionellement en amont démigrer toutes les VMs qui tournent sur l'hyperviseur.
# ce n'est pas indispensable en pratique, mais s'il sera rebooté par la suite autant
# le faire.
# Les VMs non-migrables peuvent rester allumer à cette étape.
node1# qm migrate... ou bien "bulk migrate" dans l'interface
# couper le maitre
node1# systemctl stop glusterd
# on upgrade ; les briques et clients tournent encore
node1# apt upgrade
# C'est probablement un bon moment pour rebooter: pour les VMs non migrable,
# c'est le moment de les arrêter proprement.

# S'il n'y a pas de reboot, tuez les briques gluster et relancez le service:
node1# pkill glusterfsd
node1# systemctl start glusterd

# S'il y a eu reboot, le script de démarrage démarre gluster:
# les VMs non-migrables peuvent être redémarrées immédiatement après.
node1# /root/start-gluster.sh

node1# gluster volume status
# doit lister les 2 nodes, toutes les briques Online Y avec un PID
# sinon attendre un peu
# sinon pleurer.
node1# gluster volume heal data info
# au début listera probablement quelques fichiers, puis assez rapidement plus rien
# si ça dure, regarder dans un iftop s'il y a bien du traffic
# si plus rien ne se passe et qu'il reste des trucs passer en case troubleshoot
# et impérativement réparer ça avant de continuer.
# Une fois que c'est bien clean, on peut passer à l'autre nœud ;
# si migration en masse de VMs il y a, c'est le moment.
node2# qm migrate...
# On déroule pareil:
node2# systemctl stop glusterd
node2# apt upgrade

# reboot ou restart des briques+service
node2# pkill glusterfsd
node2# systemctl start glusterd

node2# gluster volume status
node2# gluster volume heal data info
# et une fois que c'est clean on remigre les VMs dans l'autre sens.


# enfin, si le nœud n'a pas été rebooté, finir de redémarrer les processus
# qui utilisent encore le vieux gluster:
umount -a -t fuse.glusterfs # proxmox remonte tout seul derrière
pkill -x glusterfs # pour le heal daemon et le montage fuse si le umount ne passe pas
# Puis vérifier que plus rien n'utilise les vieilles libs gluster:
node[1-2]# lsof | grep deleted
# ne doit pas contenir de lib ou bin
```
