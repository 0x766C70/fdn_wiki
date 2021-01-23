[[!tag done]]

Pad : [[https://pad.gresille.org/p/tei1aixi-fdn-admincamp-20170803]]
     
Lieu : local de La Quadrature du Net, 60 rue des Orteaux 75020 Paris, France    

Là le samedi (pseudo@groupe) :

- olb@adminsys
- blackmoor@adminsys
- vg@adminsys
- belette@adminsys
- vince@benevoles
- boug@benevoles
- bbichero@benevoles (pourra faire adminsys si besoin)
- tom28@adminsys
- DelTree
- fsirjean@adminsys
- Scara@communication (et ménage documents)

Là le dimanche (pseudo@groupe) :

- olb@adminsys
- blackmoor@adminsys
- vg@adminsys
- vince@benevoles
- boug@benevoles (pas sûr d'être là)
- bbichero@benevoles (pourra faire adminsys si besoin)
- HyP@benevoles (intéressé par ce qui est technique si besoin de filer un coup de main)
- tom28@adminsys
- DelTree
- fsirjean@adminsys
- Scara@communication (et ménage documents)


Rappel des prochaines dates de FDNcamp :

- 14/15 octobre 2017
- 16/17 decembre 2017
- 24/25 fevrier 2018
- 5/6/7/8 mai 2018
- 21/22 juillet 2018
- 29/30 septembre 2018


Choses préparées
================

## Installation d'un des deux switchs N3K à PBO

Lors de cet FDNcamp nous imaginons entre autres :

  * pousser la conf sur le switch
  * racker le switch à bourse
  * le mettre en parallèle avec une nouvelle interco 10G avec gitoyen
  * brancher les machines dessus

  Ce que nous avons à faire pour la prochaine fois :

  * SFP en 100Mbps (on en a besoin d'au moins 6 idéalement 8 ou 10):
    - (olb) pousser alturna à trouver une solution -> fait, et ça marche en recodant les SFP
    - (belette) demander à Laser2000 -> fait, aucun retour après X relances, il faut trouver une alternative
    - faire un devis pour 6 SFP cisco GLC-T -> pas besoin

  * (belette) avoir 16 écrous cage -> OK dans mon sac
  * (tom28) avoir une scie à métaux pour les rails à th2 (because baie de taille télécom, demander à sebian pour + de détail) -> OK dans mon sac  * (tom28, belette) avoir des tournevis -> OK dans mon sac
  * (belette) avoir des patch fibre mono-mode (2 en tout) -> 4 dans mon sac
  * avoir des patch r45 -> 6 dans mon sac, cat 6
  * (olb) demander à Liazo de mettre en place une nouvelle interco fibre entre notre demi baie et la baie de l'autre.net (support@) -> ok, fait
  * (olb) prévenir liazo de notre intervention (support@) -> ok, fait
  * (olb) prévenir gitoyen pour qu'il prépare leur switch -> ok, fait
  * (olb) demander une vm à gitoyen avec accès publique et avec réseau d'admin (vlan 801) -> ok, fait

Ce que l'on a à faire pour la fois d'après :

  * finir la configuration du switch pour TH2 sur un [pad](https://pad.gresille.org/p/sa0iethe-fdn-admincamp-20170311)
  * pour TH2, est-ce que l'on utilise un U supplémentaire temporairement, ou est-ce que l'on remplace en mode ninja


## Migration de la messagerie instantanée (jabber) de ejabberd vers prosody

(wannig, prunus)

Sur une nouvelle machine virtuelle (jyn)


Choses faites
=============

Cf [[changelog/20170806]]


Point de coordination
=====================

## Choix des prochaines dates

- (7/8 octobre 2017 => buro)
- 14/15 octobre 2017
- (18 et 19 novembre 2017 => Capitole du libre)
- 16/17 decembre 2017
- 24/25 fevrier 2018
- (fin mars ag 2018)
- 5/6/7/8 mai 2018
- 21/22 juillet 2018
- 29/30 septembre 2018


## Inviter Gitoyen à un FDNCamp

Fabien invite gitoyen à un des trois prochains admincamp. tom28 et vince sont intéressés pour s'investir dans Gitoyen pour FDN.


## Causer de francilien

olb les invite à un des trois prochains admincamp.


## Prochain admincamp

Selon si Gitoyen ou Francilien est présent on fera pas les mêmes choses.


### switch à th2

- belette | olb et boug préparent l'intervention (causer avec gitoyen, \& autres préparations)

### migration prosody

olb relance prunus

### Nouveau service mail-

- vg, fsirjean, tom28, bbircho prépareront quelque chose à nous montrer pour l'admincamp d'après

### [gitoyen] livraison gitoyen-fdn pbo, redondance

et réflechir au déplacement potentiel d'un LNS

- olb, fsirjean, tom28, vince

### Migration de puppet sur obiwan

- olb, bbicherot



## Divers

### généraliser fail2ban

et virer denyhosts si présent.

À pupetiser (donc noyau)


### mise à jour des machines

Ce serait bien de faire le tri entre les machines qu'on veut laisser mourir le
temps de les remplacer par des vm propres et celles qu'on va mettre du temps à
reprendre (par exemple solo).

On peut mettre à jour les machines "faciles" qui sont clairement isolées
(resolver, web fdn, ackbar, vpn, kamino, ...)


### supervision : pertinence d'alertes par mail ?

Prévu une fois les tests openvpn opérationels. Alertes sont déja fonctionnelles vers belette

- belette met les alertes sur admin@
- fsirjean et olb font un un tri pour que le flux de mail sur admin soit correcte


### Questions buro pour jabber

* Faut-il fermer les inscriptions libres à jabber ?
* Nous avons à l'heure actuelle plus de 3000 comptes (dont pas mal de spams).

Nous avons 27 comptes sur les 3000++ qui ont des contacts. Faut-il supprimer les comptes qui n'ont pas de contacts ? Est-ce que youpi@jabber.fdn.fr a des contacts par exemple ? Je l'utilise, mais je ne suis pas bien sûr que mon client envoie les contacts au serveur << j'en vois 3 apparemment << C'est peu je dirais, j'ai bien plus de contacts XMPP dans mon client << bizarre. J'ai créer un compte et ajouté un contact. Il s'affiche bien dans la base. Et pour toi il y en a bien 3 seulement. << on pourrait peut-être utiliser les logs de connexion? << Rien de pertinant à l'interieur (en tout cas pas sur ejabberd). Je viens de vérifier en recréant un compte sur jabber.fdn.fr. Tous les contacts sont bien inscrit dans la base

La plus belle hache du buro a tranché :

- on supprime les 3000 comptes sans aucun état d'âme
- l'ouverture des comptes seront faite par les adminsys sur demande par mail

Vu la réactivité du groupe adminsys c'est pas forcément une bonne idée que le
groupe doivent ouvrir des comptes à la main.


### Créer une page nous rejoindre sur le wiki adminsys et rendre publique la page d'accueil.

boug et bbichero préparent un petit texte de présentation.


### mumble pour les réunions bureaux

(monter une VM chez FDN ou squatter un existant?)

À rediscuter plus tard.

