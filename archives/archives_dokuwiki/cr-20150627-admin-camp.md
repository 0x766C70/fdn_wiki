# Compte rendu de l'admin-camp FDN du jeudi 18 au dimanche 21 juin 2015

# Ce que nous avons fait ce weekend

## jeudi

  * DNS dans git par mat (et tout le weekend)
  * Préparation migration des droïdes (découverte de la configuration réseau)
  * sortie des droïdes de TH2 avec olive
  * installation à PBO
  * début de réorganisation de la baie à PBO

## vendredi

  * extinction de lns02 (shut des ports sur le switch)
  * Configuration de LNS22 (début)
  * hébergement blog et www (olb, capslock, et quota)

## samedi

  * fin de configuration de LNS22 et test sur la ligne de absoligth
  * Intervention TH2 avec gitoyen : racké LNS22 au bon endroit
  * Benné LNS02 + destruction du disque
  * réunion groupe adminsys à Numa

## dimanche

  * bascule de lns01 à lns22
  * extinction des ports de lns01
  * enlevé tous les vlans non nécessaires sur la fibre vers gixe
  * fait le tour des comptes unix existants sur l'infra
  * transmission autour du fonctionnement du si
  * transmission autour du fonctionnement de puppet/git
  * résolveur DNS (création des vm)

## Lundi

  * configuration d'un port pour brancher son ordinateur portable à PBO
  * organisation de la baie à PBO (il reste que le serveur des RMLL)
  * débuggage de l'ipmi dur les anciens droïdes (redémarrage et configuration des carte ipmi)

# Choses à faire

  * fabien envoie la nouvelle liste acl pour la baie à PBO.
  * olb lance un sondage pour avoir une idée des dates possibles.
  * trouver un lieu pour l'admincamp (tous)
  * benjamin et olive font cet intervention en juillet.
  * Fabien se charge des commandes de matériel
  * Benjamin vérifie s'il y a des câbles de disponible à Amiens.
  * mat installe rancid
  * On met etckeeper a fdn, on déplace le changelog dans /etc
  * On met la documentation adminsys dans un gestionnaire de version. Le dépôt adminsys semple approprié.
  * benjamin nous envoie la conf mutt pour chiffrer sur la liste adminsys-noyau
  * rendre munin non public.

# Dossiers encore en cours

  * Conf réseau des anciens droïdes à débugger et réinsérer dans le cluster
  * Resolveur dns à configurer (olb)
  * LNS 11 à confer et racker (besoin d'une commande de matos)
  * LNS 01 à benner + détruire le disque
  * Zones DNS dans git à mettre en prod
  * Fin de la proprification de la baie pbo
  * appliquer les changements sur les comptes unix + prévenir/demander/etc
  * vérifier un disque de spare pour les droïdes (olb)
  * Docs diverses

# Réunion du samedi soir

Présents : fulax, benjamin, capslock, mat, olb, fabien, olive, sebian (pour la discussion gitoyen)

## Relation datacenter Paris Bourse (PBO)

Les membres du bureau et du noyau adminsys ont des accès permanents.

TODO: fabien envoie la nouvelle liste acl pour la baie à PBO.

Olive nous demande de prévenir par mail lorsque l'on va intervenir. Si urgence, le faire par téléphone, le numéro sera dans le pass. Le weekend et la nuit, c'est obligatoire.

## Prochain admin camp

On vise septembre/octobre :

  * pas le premier week-end de septembre (fulax et olb)
  * pas la première quinzaine d'octobre (mat)

=> plutôt fin septembre

TODO: olb lance un sondage pour avoir une idée des dates possibles. TODO: trouver un lieu pour l'admincamp (tous)

Chez quelqu'un ?

Sujets que nous pourrions aborder :

  * croissance à bourse
  * se poser sur la questions de la structuration des satellites en vu de faire une prochaine réunion physique en invitant les satellites.
  * automatisation du déploiement de services avec le SI

## Achat d'un switch de rechange

L'idée est de pouvoir facilement remplacer l'un des deux switch s'il crame.

Celui de th2 est moins critique car en cas de crise, fdn pourrait utiliser l'infra de commutation de Gitoyen.

## Intervention à TH2 cet été

  * enlever lns01 et vador (si pas déjà fait)
  * déplacer lns11 à la place de vador

Pas de coupure de services prévues.

TODO: benjamin et olive font cet intervention en juillet.

La baie 11A4 de Gitoyen à TH2 est une baie télécom, l'écartement des montants n'est pas le même que les baies classiques. On a besoin d'extension de rail pour le deuxième nouveau lns (cf point commande). D'autre part nous avons piqué des extensions à Gitoyen. C'est donc deux paires d'extensions qu'il faudra commander.

## Commande matériel

Il faudrait commander.

  * deux paires d'extension de rails,
  * des câbles 3m.
  * 1 disque de rechange pour les droïdes (actuellement les droïdes ont des disques 7200T sata 1To).
  * 1 switch de rechange (cisco 3560),

Le switch de rechange sera stocké à PBO.

TODO: Fabien se charge des commandes de matériel

TODO: Benjamin vérifie s'il y a des câbles de disponible à Amiens.

## Sauvegarder la conf de nos switchs

TODO: mat installe rancid

## Demande de fulax pour faire un atelier config de switch

On fait attention à faire les interventions sur les switchs à plusieurs pour apprendre.

## Compte-rendu écrit des intervention dans les baie.

systématisation des comptes rendu écrits des interventions physiques dans les baies dans le wiki.

## Base technique des adminsys

  * On a causé de puppet. On se questionne sur la barre technique nécessaire à la prise en main de cet outil. On en parle dimanche.
  * TODO: On met etckeeper a fdn, on déplace le changelog dans /etc
  * TODO: On met la documentation adminsys dans un gestionnaire de version. Le dépôt adminsys semble approprié.
  * compte root : plus de clé pour les admin dans /root

## discuter de manière chiffrée sur noyau-adminsys@fdn.fr

TODO: benjamin nous envoie la conf mutt pour chiffrer sur la liste adminsys-noyau

## Gitoyen

  * Discussion sur comment FDN travaille ensemble sur la 11a4 avec Gitoyen.
  * Sauf urgence, l'equipe adminsys va essayer de prévenir Gitoyen pour les interventions pour pouvoir fonctionner ensemble.
  * Gitoyen aimerait une participation de l'équipe adminsys de FDN dans la dynamique de Gitoyen
  * Gitoyen envoie à l'équipe adminsys de FDN des nouvelles de la baie 11A4.
  * Possibliter d'utiliser l'infra de commutation de Gitoyen en cas de switch qui crame à FDN à TH2. Il reste 7 ports et des nouvelles machines vont arriver. Cela dit, si c'est le cas Gitoyen devrait rajouter un switch. Donc oui.

## RSF

  * Un contrat a été signé entre RSF et FDN. FDN infogère cette machine.
  * TODO: rendre munin non public.
  * Le noyaux adminsys est root sur cette machine
