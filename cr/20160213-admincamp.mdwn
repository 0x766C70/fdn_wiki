[[!meta title="Admincamp n°4 - 13/14 février 2016"]]
[[!meta date="20160213"]]
[[!tag done]]

Lieu : La Quadrature du Net, 60 rue des Orteaux, 75020 Paris    
Présent·e·s : Olb, Mat, Nono, CapsLock, Fabien, Benjamin, Sebian, Scara    
Nouveaux·elles : Clément, Benoît (ben), Benoît (belette), Thomas, Kankan


[[!toc levels=2]]

# Réunion de coordination

## Prochains admincamp

* 23/24 avril 2016
* 25/26 juin 2016
* 24/25 septembre 2016

## Question sur l'organisation du travail d'adminsys

### suivi et doc

On est en principe tenu de faire un compte rendu d'interventions pendant les
admincamp. Ces compte-rendus sont stockés sur notre nouveau wiki :
https://adminsys.fdn.fr/

Le nouveau wiki adminsys est un wiki hébergé sur [[infra/machines/obiwan]] et répliqué sur nos
machines car il se manipule via git.

Les anciennes pages liées à l'adminsys sur le wiki de fdn sont importables sur
ce nouveau wiki via un script d'import (cf [[archives_dokuwiki]]).  Avant
de copier une page et l'importer dans le nouveau wiki, il faut vérifier que les
infos sont toujours d'actu et supprimer le contenu de l'ancienne en le
remplaçant par un lien vers la nouvelle.


On a aussi etckeeper pour voir les changements sur les machines.

### aperçu de l'infra

Petit schéma sur l'infra actuelle de fdn :

      Paris Bourse                              Téléhouse2
      (liazo)                                   (gitoyen)
     +---------------------+                   +--------------------+
     |                     |                   |                    |                
     |             switch  |··· commutation ···| switch             |··· Transit (gitoyen)                                                     
     |             3560    |    (gitoyen)      | procurve           |                                                                           
     |                     |                   |                    |··· Collecte xDSL (nérim)                                             
     | * c3po (éteint)     |                   | * lns11            |                                                                           
     | * r2d2 (éteint)     |                   | * lns22            |··· Liens L2 pour collecte revendue
     | * c3px              |                   | * vador            |    (sames, grenode, pclight, franciliens, tetaneutral)
     | * r4p17             |                   | * lns01 (à benner) |              
     |                     |                   |                    |              
     +---------------------+                   +--------------------+              


## Accès à Bourse 
    
Le datacenter est situé au 35 rue des Jeûneurs, Paris 2. C'est un immeuble
assez classique. Il y a un digicode (cf. Password Store) pour rentrer dans
l'immeuble, puis il faut monter au 2ème étage. 

Deux cas de figure : 

- En heures de bureau (semaine, ~8h-18h), il suffit de sonner à la porte, on vient vous ouvrir

- En dehors, il faut demander l'ouverture à Liazo (l'entreprise qui exploite le DC) :

  * prévenir par mail le plus à l'avance possible de l'intervention

  * téléphoner ou envoyer un sms sur le numéro d'astreinte (frémo, en général)
    pour demander l'ouverture de la porte par SSH.

Une fois rentré dans le DC, il y a un accès aux sales par contrôle biométrique.
Il faut donc avoir ses circuits veineux enregistrés dans leur système, à
l'avance (y aller une première fois, en gros). C'est la salle de gauche, notrebaie est  située au fond à droite, dans le couloir froid. Y'a des stickers pour
aider à se repérer :p La baie s'ouvre avec un code, qui est stocké dans le
Password Store. 


##  Secrétaire tournant

L'idée du secrétaire est d'avoir quelqu'un "responsable" de répondre aux
demandes formulées sur la mailing list.  Le but étant qu'on réponde dans un
temps raisonnable et de déclencher les actions nécessaires soit en faisant
soi-même soit en déléguant à la personne qui sait faire.

jusqu'au prochain admincamp (celui du 23/24 avril 2016) les personnes suivantes
se sont auto-désignées comme volontaires pour assurer ce role :

  * olb
  * ben 
  * belette


## Binômes

Lorsque l'on arrive dans l'équipe adminsys, pour faire des choses avec les accès
root on se met dans un screen/tmux avec un root.


## Certificats X509 et letsencrypt

Renouvellement nécessaire au moins tous les 3 mois (recommandé tous les mois).
Se fait assez bien avec ce script : https://github.com/diafygi/acme-tiny . Il n'y
a pour l'instant pas de wildcard. Mais a priori, nous n'en avons pas besoin, on
peut faire un certificat par domaine sans soucis. À vérifier qu'un même domaine
soit pas utilisé à plusieurs endroits.

> > > À noter qu'il y a un peu de "rate-limit" (5 certificats par domaine et
> > > par semaine, cf
> > > https://community.letsencrypt.org/t/quick-start-guide/1631 )
> >
> > Du coup, un csr avec des subjectaltname n'est pas une mauvaise idée. 
>
> Ça, c'était probablement pendant la phase béta. Il est clairement préférable
> de ne pas mélanger les certificats : un certificat par site/service/... c'est
> bien, avec plusieurs domaines potentiellement. --olb

Domaines qu'on peut migrer sans soucis pour tester : adminsys.fdn.fr ;
wiki-adh.fdn.fr ; www.fdn.fr Question des cyphers SSL/TLS ? On nous a rapporté
plusieurs fois qu'on avait des configs (très ?) faibles :-/

=> belette, nono, ben, fabien (de loin)


## Problématique de perfs sur le cluster Ganeti

Nous avons un problème de performance disque su les cluster. Nons avons décidé
de passer de RAID6 à RAID1 (d'où la réinstallation prévue des cluster).

Si les problématiques de performances continuent nous envisageons d'acheter des
nouveaux disques pour les droides. Actuellement nous avons des Western Digital
série Re (référence WD1003FBYZ-010FB0) :
http://www.wdc.com/wdproducts/library/SpecSheet/ENG/2879-771444.pdf un SSD 1To
ça coute entre 300 et 400 HT.

Si jamais il y a de l'energie pour monter un service de vm pour les membres. Ce
sera probablement nécessaire et le bureau a dit que s'il fallait, c'était
possible. Pour l'instant, on attend de voir ce que donne le passage de raid6 à
raid1.

## Réinstallation des deux anciens droides

Il serait pertinent de remettre en état les deux anciens droïdes pour avoir une
infra de test : par exemple pour tester les maj de ganeti, drbd & co. À
rajouter dans les choses à faire.

## Switchs,  réseau et redondance

L'idée serait à moyen terme d'avoir du réseau redondé (bonding sur les
machines & double switch) et pourquoi pas d'avoir du 10G pour le réseau de
réplication du cluster. Il s'agirait d'acheter des switchs et des cartes pour
les machines.

Au delà de la redondance, ce serait pas déconnant de remplacer le switch
procurve.


## puppet & etckeeper

Nous utilisons conjointement puppet et etckeeper. Actuellement, quand puppet
passe, et commite les changements dans /etc qu'il n'a pas effectué : c'est
pénible. L'idée est d'empêcher puppet de passer si etc est modifié.

* Pourquoi pas faire une sonde nagios pour raler si le dernier passage de puppet a échoué ?
* Pourquoi pas faire une sonde nagios pour raler si des changements sont à appliquer sur les LNS ?
* Faire en sorte que etckeeper envoie des mails à admin@fdn.fr lors d'un changement.

olb s'y colle


## Migration des machines vers jessie

Comment on fait ?

Proposition de faire un admin camp à thème : "migration jessie". L'idée semble convenir.


## Question de réinstaller from scratch certaines machines ?

C'est possible si des gens sont motivés : il semblerait plus pertinent de voir
la chose par service plutôt que par machine.


## Évolutions de l'infra ADSL

Possibilité d'une nouvelle collecte xDSL avec Liazo : Clément, Fabien, Ben sont intéressés.


# Choses faites / en cours

## [fait] divers sur puppet

  * Gérer l'alias root sur les machines
  * Conf ssh (passwordauthentication no)
  * Supprimer les anciens dépots puppet du gitlab

## [fait] adminsys sur le nouveau site web

* Activation de l'instance www.fdn.fr et migration des données. Il manque plus
  que le DNS.

* Écriture d'un script (`scripts/prod2devel`) pour mettre à jour
  www-devel.fdn.fr à partir de www.fdn.fr

## [en cours] Réinstallation des deux nouveaux droides

Le but étant d'avoir des performances io plus élevées ; on parle entre autre de
virer le raid6 au profit d'un raid 1 et de cloisonner le réseau de réplication.

Ca suppose de déplacer l'ensemble des instances ganéti sur un noeud du cluster
pendant qu'on réinstalle le second noeud. Puis on remet les machines sur le
noeud fraichement installé, et on réinstalle le second noeud.

Technos en présence : Ganeti et KVM

Remarques :

* Attention ne pas utiliser tout le disque (1Tio base 10 !)
* les disques seront peut être à changer (plus tard) en reconstruisant les tableaux RAID

Déroulement :

 1. [fait] Évacuation de r4p17 :

    - déplacement de toutes les vm sur c3px (`gnt instance migrate INSTANCE` pour INSTANCE dans vm qui sont sur r4p17)
    - conversion de toutes les vm en plain (`gnt -instance modify -t plain INSTANCE`)
    - suppression du nœud r4p17 du cluster de ganeti (`gnt-node remove r4p17.fdn.fr`)

    À ce moment là de l'histoire, le cluster ne tient plus que sur une seule
    machine (et là c'est le drame :))

 2. [fait] Réinstallation de r4p17 :

    - Configuration du port ipmi (nouveau câble ?)
    - Configuration de l'ipmi sur la machine (+vérification)
    - installation d'une debian classique (jessie, 64 bits)
    - installation puppet agent + run puppet
    - Conf réseau
      * machine :
        - br3 - infra - 80.67.169.79 (eth1.3)
        - br801 - admin - 10.0.0.79 (eth1.801)
        - br802 - replication - 10.0.2.79 (eth0.802)
      * switch
        - suppression du vlan3 détagué sur eth0
        - création du vlan802 tagué sur eth0

 3. [fait] Integration de r4p17 au cluster et changement de master
 
 4. [en cours] Évacuation de c3px
 
 5. Réinstallation de c3px
 
 6. Intégration de c3px au cluster et repartition des vm
 
 7. Configuration des ports ipmi dédié (à faire sur place à paris bourse)

## [fait] bot IRC pour le annoncer les pannes

Résolution de problème sur le bot IRC pour annoncer des pannes de FDN :

- soucis d'encodage
- le bot répondait au message sur IRC

Pour info, ce bot publie les alertes présentes dans le sujet du channel de FDN,
sur une liste et sur une page web.

- liste : http://listes.ldn-fai.net/mailman/listinfo/fdn
- page web : http://fdn.ldn-fai.net/

## [fait] Authentification sur nouveau wiki adminsys

Nous avons rendu accessible le wiki aux adhérent-e-s le site sur
admisnys.fdn.fr via leur couple login/mot de passe (adhacc).

## [en cours] DNS (resolveurs & dns faisant autorité)

Séparer les serveurs faisant autorité de ceux qui sont résolveurs.

Ce qui a été fait : gestion des zones via des dépots git ; réinstallation de
deux serveurs faisant autorité.

On a des slaves qui sont encore installés sur les anciens serveurs. Des mails
sont partis pour demandé aux adhérents de changer leur slave.

Le serveur faisant autorité va changer d'ip puisqu'on ne peut pas changer celle
des résolveurs dont on a communiqué l'IP dans diverses oppérations de
communication (résolveur ouvert administré par FDN

## [fait] Finir de ranger la baie de PBO


## [fait] Écriture des scripts fdn_ipmi_kvm & fdn_ipmi_sol

Pour avoir facilement une console sur nos machines supermicro (avec les
fonctionnalité supermicro). Exemple d'utilisation (il faut être dans le pass) :

    ./bin/fdn_ipmi_kvm c3px

Ce script monte une connexion SSH et sur lns11 et met en place sur forwarding
de port.
    
    ./bin/fdn_ipmi_sol c3px



## [encours] Installer Rancid pour backuper la conf des switchs

Pour info: https://github.com/dotwaffle/rancid-git/pull/80 paquet dispo ici
http://apt.sebian.fr/rancid/ (log de build dans le .build)

On a 2 switchs : un à pbo et un à th2 ; un cisco et un hp.

On sait qu'on a un point faible ici : on a pas de redondance sur les switch

Clément est prêt à travailler dessus, ça n'a pas l'air très complexe, il est en
attente :

- qu'on lui dise sur quelle VM travailler 
- l'accès à la VM 
- accès en écriture au wiki pour documentation.
- accès aux switchs


## [encours] Certifs X509

Jusque là on prenait nos certificats chez CAcert. Récemment, letsencrypt qui
est devenu opérationel. La question se pose : est-ce qu'on passe nos
certificats chez letsencrypt ou pas ? On a environ un an de tranquilité puisque
nos certificats cacert expirent en fin d'année

Par contre on peut avoir besoin de de certificats tout de suite pour certains
services (site web, wiki adminsys et blog).


# Choses à faire

## Vador : le retour de l'empire contre-attaque des étoiles

[[infra/machines/vador]] est une machine machine physique à TH2 que nous souhaitons benner.
Mais il y a encore des services dessus : DNS faisant autorité, resolver DNS, wiki adhérents.
Dès que ces services sont déplacés, on peut l'eteindre.

## Benner lns01

Voir avec Gitoyen pour virer l'ancien LNS à téléhouse en 11A4.

## Gitlab

Gitlab est installé sur [[infra/machines/leia]].  L'idée c'est déplacer gitlab dans
une vm dédiée. On signale que gitlab arrive bientot dans debian directement
packagé proprement ; on peut l'installer via omnibus histoire de ne pas
attendre que ce soit dispo dans les répos stable (le paquet arrive dans Debian
sid, et ne sera probablement pas backporté) :
https://tracker.debian.org/pkg/gitlab

Attention, il y a notamment la gestion des zones dns dans les dépots de ce
gitlab.


## Évolution de la supervision

Machine de supervision dans un autre AS : l'idée est de pouvoir monitorer
l'infra fdn en dehors de celle-ci. Et notamment passer à check-mk pour la
supervision interne.


## Ranger la baie de PBO

TODO connexe : noter dans le wiki qui contacter quand on veut faire quelque
chose (inter dc ; etc)


## Arrêt temporaire de la baie 11A4 à Téléhouse 2

Il est question à Gitoyen de faire un grand ménage dans cette baie. À voir avec
eux.


## Finir l'inventaire des ressources IP et MàJ db RIPE

* Créer un rôle adminsys FDN avec des personnes correspondant au noyau
* Reprendre la main sur le l'objet mnt des objets FDN

C'est un peu le bazar dans les ressources prises chez gitoyen ; si à terme on
peut renuméroter pour proprifier c'est yabien

Proprifier les accès aussi : pour l'instant ya que deux personnes qui ont les
accès dans leur obscure boite mail.


## Achat de matos

* Un switch de spare
* Des rails pour la 11A4
* Des disques pour les droides (?)
* Des câbles ethernet


## Pousser la configuration ipv6 pour les clients openvpn

Étudier le mail de Antony Bourguignon


# Idées en l'air

  - possibilite d'avoir un VPN sur chaque ligne ADSL pour qu'orange / nerim /
    autres ne puissent pas jouer aux indiscrets entre l'abonné et FDN (tout ca
    gratuitement vu que ca coutera rien a l'asso).

  - Crypto VPN : ajouter une VM VPN avec les cyphers AES pour profiter d'AES-NI
    (le cypher est en dur dans la conf OpenVPN).

    > Il est pas tellement nécessaire d'ajouter une vm : une nouvelle instance
    > d'openvpn devrait suffire. À discuter ?

