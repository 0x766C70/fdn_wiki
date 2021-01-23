[[!tag done]]

Lieu : local de La Quadrature du Net, 60 rue des Orteaux 75020 Paris, France
Heure : 9h30

Venir c'est bien, s'inscrire c'est mieux !

Là le samedi (pseudo@groupe)

  * Caps
  * DelTree
  * Chakiral@benevole
  * VG@adminsys
  * Blackmoor@adminsys
  * belette@adminsys
  * wanig@adminsys
  * olb


Là le dimanche (pseudo@groupe)

  * Caps
  * DelTree
  * Chakiral@benevole
  * VG@adminsys
  * Blackmoor@adminsys
  * Vince@adminsys
  * wanig@adminsys
  * olb


À distance:

  * tom28@adminsys, par intermittence
  * youpi, le dimanche


Pas là:

  * Stéphane Ascoët@adminsys probablement pas là
  * Fabien, coincé à Grenoble ce week-end :-( See u next time !


# Rappel des prochaines dates d'admincamp :

 * 24/25 fevrier 2018
 * 5/6/7/8 mai 2018
 * 21/22 juillet 2018
 * 29/30 septembre 2018


# Choses faites

Cf [[changelog/20171217_camp]]

# Coordination

## backups

Besoin d'internaliser les backups sur une machine controlée par les adhérents
de FDN. L'idée serait de poser une machine chez FAImaison dédiée à cet usage :

- envoyer un mail a faimaison \o/ belette (tarif, 1U, conso électrique) :
  https://transparence.faimaison.net/public/ )

- trouver une machine \o/

En reparler la prochaine fois.

## liste adminsys polluée

le rythme des admincamp donne le rythme auquel des réponses peuvent être
données : il n'y a pas trop de demandes traitées entre admincamp.

Quelques pistes :

- flécher les demandes pour qu'elles soient plus précises et concises ?  avoir un formulaire de saisie pour les demandes pour restreindre le bruit ? le lier au SI pour faire de la validation des demandes (exemple : pas possible de demander un reverse pour une IP que l'adhérent ne possède pas ; pas possible d'avoir du service si pas d'abos aux services, etc)

- faire que les demandes passent en premier par le support plutôt que d'arriver directement sur adminsys@ ?

- est-ce que les gens du support sont ok sur ce principe ?


→ envoyer un mail au groupe support pour leur proposer de venir nous voir au
prochain admincamp pour discuter des groupes adminsys/support, du rôle, des
tâches...

→ par la suite en parler pendant AG mettre à jour le site web pour ne plus
faire apparaitre adminsys@ comme point d'entrée ; ouvrir la discussion pour
définir quelles listes doivent être contactées pour telle ou telle demande


### Échanger un lns et un droide

Actuellement les deux lns/passerelle sont à Téléhouse 2 et les deux droïdes
sont à Paris Bourse.

Objectif avoir une passerelle sur les deux sites pour améliorer la résilience
de FDN.  Pour que cela ait du sens un faudrait également avoir un droide de
chaque coté pour les services critiques (DNS, VPN, etc). Pourquoi pas le faire
à l'admincamp N+2 aka celui pas loin de l'ag ?

Au procahin admincamp une équipe prépare cette intervention.

* vérifier avec gitoyen qu'on a les bonnes sessions BGP (et les bonnes priorités)
* check vlan bien propagé
* déplacer un des LNS
* yolo
* verifier que ça va bien se passer pour la réplication


## Infra mail

vg a besoin d'une deuxième personne pour s'ateler à une proposition
d'évolution.

en parler dans le mail de cr de adminsys.


## prosody/xmpp

décision du bureau: vous pouvez supprimer les comptes sans contacts
fermer l'ouverture de compte

wanig fait la migration.

Diaporama pour lutter contre le spam avec ejabberd  : https://fr.slideshare.net/mremond/fighting-xmpp-abuse-and-spam-with-ejabberd-ejabberd-workshop-1
(quelques étapes simples pour limiter les dégâts, mais pas pour discriminer les bons utilisateurs des spammeurs)


## RTC

- relancer neuronnexion la dessus cf TODO wiki
- besoin d'un moyen de tester -> qui a une ligne cuivre ? Pas besoin de cuivre, ça passe suffisament bien en VoIP ADSL/fibre pour pouvoir tester
- ce serait bien d'avoir une sonde pour vérifier que ça marche

Mail de Youpi 5 mars 2017 :
- corriger la cible radius en 80.67.169.41 et 42 (côté nnx)
- y faire arriver les requêtes pour @fdn.nerim aussi
- y faire arriver les requêtes pour @vpn.fdn.fr aussi
- y faire arriver les requêtes pour @fdn.dslnet.fr aussi
- faire marcher toto/toto :)

## Cluster de virtu pour les adhérents

wanig cherche un binome pour bosser dessus.

en parler dans le mail de cr de adminsys.


## Changer les disques du cluster de vm

Pourquoi pas, les disques actuels sont lents mais ce n'est pas critique. Si
quelqu'un veux s'en occupper...

## librenms

Installation de librenms => oui. Benoit s'est proposé pour le faire.


## Gitoyen pour fdn (vince/tom)

- inscription listes
- reflexion sur les tarifs...

→ todo : envoyer à tom  et vince les infos pour s'inscrire aux listes de Gitoyen


## Compte rendu et mail prochain admincamp

-> olb fait le compte-rendu et envoie un mail sur membre dans la foulée pour
annoncé le porchaine admincamp
