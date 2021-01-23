[[!meta title="WIP - backups"]]

> olb : **attention: ** ceci est une ébauche de documentation qui n'a pas
> encore été mise en place.

Toutes les nuits, l'ensemble des machines de FDN sont sauvegardées sur la machine
backup.fdn.fr qui se situe à ··· . Ces sauvegardes sont incrémentales, chiffrées et
compressées.  Nous conservons une sauvegarde tous les jours pendant un mois, et une
sauvegarde toutes les semaines pendant 3 mois.

Ce sont les machines qui initie leur propre sauvegarde. Cependant, elles n'ont pas
la possibilité de supprimer des anciennes sauvegarde.

Par ailleurs, ces sauvegardes sont accessibles par l'ensemble du noyau adminsys.

[[!toc levels=2]]

Procédures
==========

## Restauration

Quelques commandes utiles :
    
    man borg

Lister l'ensemble des sauvegardes pour une machine donnée :

    borg list \
        backup@backup.fdn.fr:palpatine.fdn.fr

Lister le contenu d'une sauvegarde :

    borg list \
        backup@backup.fdn.fr:palpatine.fdn.fr::nom

Monter à distance le contenu d'une sauvegarde :

    borg mount \
        backup@backup.fdn.fr:palpatine.fdn.fr::nom \
        /mon/point/de/montage

Il faut démonter l'archive par la suite :
    
    borg umount \
        /mon/point/de/montage

## Backuper une machine

Pour mettre en place le backup d'une machine, il suffit de :

- générer un secret partagé :

      fdn_pass generate -n 64 machines/<host>/backup

- mettre ce secret partagé dans le fichier `/root/backup-passphrase`

Lancer puppet sur la machine, puis sur l'espace de backup (ou simplement
attendre). Si une machine ne dispose pas du fichier /root/backup-passphrase,
puppet se pleindra.


## Rajout d'une base de données à backuper

Le principe pour backuper une base de données est de réaliser un export dans
/var/backups/<madb>, avant la sauvegarde des fichiers qui inclus le répertoire
/var/backups

Il existe tout un tas de 'hooks' pour backupninja pour les bases de données les
plus connus. Ces hooks se placent dans /etc/backup.d/

## Rajout d'un répertoire à backuper

La conf puppet de chaque machine comporte la liste de répertoires à
backuper en plus des répertoires traditionnels (/etc, /home,
/var/backups).



Installation initiale
=====================

## Espace de backup

L'idéal est que ce soit une vm avec un point de montage sur l'espace de backup.
On a un compte backup@backup.fdn.fr, dans lequel sont autorisés toutes les clés
SSH des machines avec limitation de commande.

L'idéal est que ce soit une vm car on pourra l'intégrer à puppet.

## Choix des outils

borg-backup :

- déduplication de données : les fichiers sont coupés en morceaux, et un même
  morceau n'est stocké qu'une seule fois.
- compression des données
- chiffrement des données
- backup incrémentaux
- backup initiés par les machines elles-mêmes (avec possibilité de ne pas
  permettre la suppression des données par les machines qui se backup elle
  même).

backupninja :

- ensemble de scripts facilitant l'automatisation des backup sous
  debian.

## Automatisation avec puppet

Par machine à backuper, il faut :

- un secret partagé (a stocker dans pass)

Puppet se charge du reste : cf modules fdn/backup, backupninja et borg-backup.

## CRON de nettoyage

Sur la machine de backup, un cron tourne tout les jours pour nettoyer les vieux
backups. Ça se fait en lançant les bonnes commande borg. Installée également
par puppet (Cf : sudo -u backup crontab -l).


