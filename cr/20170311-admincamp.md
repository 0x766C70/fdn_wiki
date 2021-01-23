[[!tag done]]

Pad : [[https://pad.gresille.org/p/sa0iethe-fdn-admincamp-20170311]]    
Lieu : local de La Quadrature du Net, 60 rue des Orteaux 75020 Paris, France    
Là :  olb, belette (samedi sûr), blackmoor (pas le samedi après-midi[AG April]), vg (pas là le samedi après-midi pour l'ag april aussi), tom28 (samedi midi/après-midi)    
Pas là : André Vanderlynden    
À distance : youpi, tom28 (dimanche par intermittence)    


# Récap

## Rappel des prochaines dates d'admincamp

> - 20/21 mai 2017, spécifique accueil nouveaux/nouvelles
> - 5/6 aout 2017
> - 14/15 octobre 2017

## Un petit admin camp avant l'AG

Cet admin camp à été particulièrement calme et petit en effectif.  
Nous avons continué à travailler sur l'AG ainsi que sur les nouveaux switchs.



# Choses faites sur le week-end

## Switchs

### Compatibilité des switchs 10G avec les ports 100Mbps

Belette, tom28, olb ont testé les switchs N3K-3064PQ-10GE avec des SFP GLC-T
de Cisco. Ça marche bien en 100Mbps. (Ouf !)  
C'est donc bien les SFP solid optic d'Alturna qui ne sont pas compatibles.

→ olb recontacte alturna et demande des SFP compatibles 100Mbps

Au passage, on a testé aussi deux SFP+ 10G LR dans les switchs et ça marche bien.

→ belette ramène deux autres SFP+ LR.

### Conf des switchs

Nous avons mis à jour l'os des deux switch.  

Nous avons préparé la configuration des nouveaux switches : config commune +
config spécifique PBO. Reste à faire : config spécifique TH2.


## Préparation de l'AG

### sondage framapoll

Belette et Blackmoor ont travaillé sur le sondage (source:
https://pad.gresille.org/p/RcwTSYCLvT-sondage-fdn-ag-2017)  
  -> https://framaforms.org/sondage-french-data-network-1489229278  
  -> base pour le bureau, côté adminsys ok modulo quelques points à ajouter si envie



# Choses à faire pour le prochain admincamp

- envoyer un mail au bureau pour la préparation de l'ag
- slides pour l'AG
- bilan rédigé des admincamps (olb)
- mail sur AG pour wiki, bilan, on recrute (olb)
- creation page publique sur fdn.fr (se mettre dans la peau d'un nouvel arrivant et comprendre / retirer les barrières potentielles...)    
(texte à retravaillé)    
**Wiki AdminSys**    

FDN possède un wiki particulier dédié au travail des adminsys de FDN: https://adminsys.fdn.fr/
Il s'agit d'un wiki séparé du wiki des adhérents (https://wiki-adh.fdn.fr/wiki?do=login).
Il est accessible en lecture seule à tous les adhérents FDN, grâce à leur login/password de l'espace adhérents.

Ce wiki contient les docs de mis en place et maintient des outils/applications que gères les adminsys.
Il peut être ...
Éventuellement créer une page nous rejoindre sur le wiki adminsys et rendre publique la page d'accueil.

- finir la migration de gitlab sur kamino (vm chiffrée) (mat)
- proposer un code de conduite (fabien)
- AG : présentation / animation / présence autour d'un sujet sur l'adminsys FDN (caps, belette)
- tunnels chiffrés : alléger les filtres dans bird lns01, lns02
- tunnels chiffrés : créer une nouvelle vm x86_64 pour les vpn (2 cpu), pour remplacer la vm i386 vpn1
- tunnels chiffrés : il faudrait virer l'ancienne allocation dans le reverse DNS de 2001:910:802::/64 qui ne servira pas finalement.
- https: continuer let's encrypt que manque-t-il ? Le serveur Sympa mais apparemment c'est pas simple - Bah faut avancer sur solo quoi. Tom28 & Fabien étaient sur le coup.
- web : configurer chewie memoire vive / apache & mysql (dimenssioner la mémoire, apache, mysql et php comme il faut)
- etckeeper : faire un mail à admin@ quand /etc change
- resolver DNS : migration des resolvers DNS sur resolver2
- mails : Passer sur la config SSL/TLS des mails (vg a envie de regarder et de s'en occuper)
- supervision : plein de boutons à tourner, de sondes à ajouter, de trucs et de machins à puppetiser... (précisions ?)
- Déprovisionner la conf des radius pour Tétaneutral ainsi que la conf ADSL (checks nagios, L2TPNS...)
- [noyau] Migration de puppet master vers une machine dédiée (soulager leia)
- [noyau] cluster ganeti : fermer les ports ou resteindre les services inutilement ouverts
- wiki adhérents: lorsque l'on clic sur le bouton "Wiki" du site web fdn.fr on ne tombe pas sur la page de login (si pas co) ou d'accueil (si déjà co)
- wiki adhérents: lorsque l'on se connecte au wiki (en venant du site, pas testé autrement) on tombe sur la page n'existe pas au lieu de la page d'accueil


# Choses à discuter

- supervision : pertinence d'alertes par mail ? pas pour tout, bien sûr
- [gitoyen] livraison gitoyen-fdn pbo, redondance
- mettre une todo dans le wiki (fabien)


# Conf des switchs N3K-3064PQ-10GE (pour mémoire/svg)

## Conf commune

    vlan 3
      name fdn-infra
    vlan 14
      name fdn-lns-radius
    vlan 16
      name nerim-dsl
    vlan 17
      name nerim-dsl-pppoe
    vlan 20
      name tetaneutral-collecte
    vlan 21
      name grenode-collecte
    vlan 22
      name sames-collecte
    vlan 119
      name gitoyen-grand-ternet
    vlan 126
      name liazo-radius
    vlan 127
      name liazo-best-effort
    vlan 128
      name liazo-premium
    vlan 801
      name fdn-admin
    vlan 802
      name fdn-replication
    vlan 2019
      name franciliens-collecte
    vlan 2052
      name pclight-collecte
    
    interface ethernet 1/48
      description upstream-gitoyen
      switchport mode trunk
      switchport trunk allowed vlan 3,14,16,17,20-22,119,126-128,801,802,2019,2052
    
    interface ethernet 1/1-16
      switchport mode access
      switchport access vlan 801


## PBO

    interface ethernet 1/1
     description c3po-replication
     switchport trunk allowed vlan 802
     switchport mode trunk
    !
    interface ethernet 1/2
     description c3po-vlans
     switchport trunk allowed vlan 3,801
     switchport mode trunk
    !
    interface ethernet 1/3
     description r2d2-replication
     switchport trunk allowed vlan 802
     switchport mode trunk
    !
    interface ethernet 1/4
     description r2d2-vlans
     switchport trunk allowed vlan 3,801
     switchport mode trunk
    !
    interface ethernet 1/5
     description c3px replication
     switchport trunk allowed vlan 802
     switchport mode trunk
    !
    interface ethernet 1/6
     description c3px vlans
     switchport trunk allowed vlan 3,801
     switchport mode trunk
    !
    interface ethernet 1/7
     description r4p17 replication
     switchport trunk allowed vlan 802
     switchport mode trunk
    !
    interface ethernet 1/8
     description r4p17 vlans
     switchport trunk allowed vlan 3,801
     switchport mode trunk
    !
    interface ethernet 1/10
     description RMLL
     switchport access vlan 3
     switchport mode access
    !
    
    interface ethernet 1/16
     description "Acces pour intervention"
     switchport access vlan 3
     switchport mode access
    !
    
    
    interface eth1/17
     description R2D2 IPMI
     switchport access vlan 801
     switchport mode access
    
    interface eth1/18
     description C3PO IPMI
     switchport access vlan 801
     switchport mode access
    
    interface eth1/19
     description C3PX IPMI
     switchport trunk allowed vlan 801
     switchport mode trunk
    !
    interface eth1/20
     description R4P17 IPMI
     switchport trunk allowed vlan 801
     switchport mode trunk
    !

