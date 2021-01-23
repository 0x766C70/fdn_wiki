[[!tag done]]

Date : 12 et 13 septembre 2015, à partir de 9h le matin    
Lieu : La Quadrature du Net, 60 rue des Orteaux, 75020 Paris

[[!toc]]


# Réunion

## Fibre entre FDN et Gixe, on en est où ?

C'est une fibre pour SAMES qui a des équipements chez Gixe. On a laissé que le
VLAN de SAMES dessus. On a pas d'action à faire là-dessus.

## Proposition de matos

Belette nous propose du matériel :

- 1x Cisco Catalyst 2970G-24TS-E 24ports 10/100/1000 + 4 ports sfp un peu vieux
mais fonctionnel si ça intéresse...
- 24 cables RJ45 cat6 blindés (SSTP) de longueur 2 à 5m

On le prend : olb répond à belette

## Spécifier l'offre vm abonnés ?

- accès chiffré au bootstrap de la vm (vnc + tls + pki)
- problème de performance disque (raid6 -> deux raid1 ou raid10)
  - nous faisons deux raid 1 sur chacun des nouveaux droides (un pour FDN, un pour les abonnés), rallumer les anciens droides pour les abonnés
  - transition : réinstaller c3px et r4p17 l'un après l'autre, un seul suffit pour les VM actuelles
- écrire des scripts instance-debootstrap pour industrialiser la création de vm pour abonnée
- sur le nommage : un domaine vps.fdn.fr dans lequel les abonnés choisissent le nom qu'ils veulent. Reverse  à configurer en fonction.
- sur les IP : il reste un /25 (80.67.169.128/25) libre sur le /24 80.67.169.0 (infra fdn).

  Un travail de rangement, et d'analyse de ce que l'on utilise peut être intéressant avant de demander à Gitoyen un /24 pour les vps. (Cf. point dédié).

- Intégration du bouzin dans le SI, à voir avec Benjamin (et/ou d'autres ?). (avec l'équipe si)


## inventaire des ressources assignées à et utilisées par FDN

Il s'agit des préfixes IP utilisés par FDN.  nono et fabien s'en occupent.

TODO :
    - documenter ce qu'on trouvera  -> https://wiki-adh.fdn.fr/wiki/adminsys:ressources
    - s'assurer que le DNS est en face des trous

Pour les maj de la bd du ripe on verra après l'état des lieux.


## Machine de supervision dans un autre AS

30G disque / 1Go ram

Fabien se charge de demander à LDN puis aux autres si ça n'aboutit pas.

- ldn
- grenode
- pclight
- absolight

Installation d'une supervision basique : nono.

## Demandes diverses potentiellement en souffrance

- Demande de nico Accès / clés à changer/installer pour nico sur si et solo (olb et fabien)
- Demande de manu si et les lns (olb et fabien)
- Demande de julien : déconfigurer le vpn du loop sur les lns (nono et fabien)  -> fait
- Demande de nico : Je veux m'assurer que l'ensemble des services utilisés par Xavier Benech ont bien été résiliés. (mat)


## La suite structurelle 

- Les prochains admincamps seront ouverts aux personnes qui souhaitent s'investir dans l'adminsys fdn.
- Il a une distinction claire en terme de prise de décision entre les inscrits à la liste noyau et l'équipe adminsys au sens large.
- Le fait d'être membre de l'équipe adminsys est conditionné à l'activité réelle et à la présence aux admincamps (>= 1 fois par an).
- On maintient la liste adminsys pour l'équipe, seront inscrites à cette liste seulement les personnes qui sont déjà venues en admincamp (ou qui sont manifestement actives).
- On conseille au reste des abonnés actuels de la liste de s'abonner à la liste bénévoles à la place (à la prochaine IRL, on mettra à jour la liste en conséquence)
- On va créer un espace de documentation à la fois interne et externe. Tous les membres de FDN pouront le lire. L'équipe adminsys pourra le modifier. Il y aura un point d'entrée web agréable et lisible pour permettre aux membres de s'informer sur l'activité des adminsys. La solution technique retenue est un ikiwiki sur obiwan, avec un espace web (olb et fabien).


## Remboursement de billets pour cet admincamp

- olb et fabien se font rembourser leur billet de trains (~ 230€).


## Prochains admincamp

Dates :

- 5/6 décembre 2015
- 13/14 février 2016
- 23/24 avril 2016
- 25/26 juin 2016
- 24/25 septembre 2016 (à préciser)

Remarques :

- Lancer un appel a canapé parisien pour héberger les adminsys de passage du vendredi au lundi quand c'est sur Paris.
- Demander aux fai locaux si ils n'ont pas envie qu'on aille faire ça chez eux.
- Demander à la quadrature si on pourait utiliser le garage : vendredi fin d'après midi -> lundi début de matinée sur tout ou partie de ces weekends.


# Fait / À faire

- [fait] créer un objet org fdn dans la base du ripe pour mettre un abuse. Et faire en sorte que abuse@ soit lue.

- puppet r10k + fusion des dépots ?

  - fusion des dépôts fait
  - r10k on verra quand le besoin se fera sentir

- gestion des mises à jour (apt-dater)

  - [fait] installation de apt-dater sur les machines
  - configuration sur obiwan

- une machine pour les outils internes

  - [fait] creation de la machine chiffrée (obiwan)
  - [fait] puppet
  - rajouter supervision
  - backup

- [fait] mise en route de lns11

- problématique perf disque du cluster

  - TODO : réinstaller les machines avec 2 paries RAID 1, cf plus bas

- DNS faisant autorité et nouveaux resolveurs

  - affecter une nouvelle ip à vador pour le dns slave faisant autorité
  - mettre à jour le glue record

- Créer un contact technique gandi adminsys pour les domaines de fdn

- Une machine chiffrée pour ADN

  - [fait] machine créée
  - mettre en place une pki pour VNC / tls

- Reprendre la main sur toutes les vms FDN (RSF [y'a un peu de taf sur cette machine d'ailleurs], ackbar...)

  - rsf
  - ackbar

- passage en revue de la supervision -> checkmk ?


