[[!tag done]]

Lieu : La quadrature du net
Date : 11, 12, 13 novembre


# Prochaines dates d'admincamp

  - 21/22 janvier 2017
  - 11/12 mars 2017
  - (25/26 mars AG FDN)
  - 20/21 mai 2017
  - 5/6 aout 2017
  - 14/15 octobre 2017

# Changer de secrétaire tournant

Pour rappel, le/la secrétaire est une personne chargée de s'assurer que les mails reçus sur la liste adminsys@ reçoivent une réponse.
Ça suppose de répondre aux gens comme quoi on a reçu leur demande, et d'aller taper sur celleux qui savent faire pour que ça soit traité.
C'est aussi un bon moyen d'apprendre, en se mettant en doublon sur les interventions programmées.
Le secrétaire est aussi chargé d'annoncer les dates du prochain admincamp sur ag@ (attention perturbations) et benevoles@ (pad + inscriptions) environ un mois avant.
Le role de secrétaire est réatribué à chaque admincamp.

==> tom28 se charge du secrétariat jusqu'au 21/22 janvier


# Utilisation du channel irc #fdn-adminsys

Fabien crée le channel #fdn-supervision et branche le bot nagios dessus.


# Point sur ce qu'on a fait

  - Olb : plein de petits trucs autour de puppet et etckeeper, gestion des comptes unix par puppet avec des rôles, fin de la pupettisation de let's encrypt (et sa doc), la pupetisation de la conf des droides (suite au passage à jessie), let's encrypt sur lists.fdn.fr, déprovisionnement de la collecte TTNN, sonde nagios pour vérifier le passage de puppet. Un souci sur ganeti a aussi été réparé (mauvais metavg, corrigé).
  - Blackmoor : tests sur le vpn openbar pour avancer sur le tuto du futur site web.
  - Vg : correction des problèmes de compilation de pelican pour le site du vpn openbar sur chewie. Python 3.4 needed, à voir ? Scripts de déploiement du vpn openbar sur le modèle du site web fdn.
  - Quota et scara : ont avancé sur le site du vpn openbar
  - CapsLock / Fabien : on a mis en place les sessions BGP avec Liazo (modulo un problème coté Liazo qui n'est toujours pas résolu) ; on a appris radius et commencé à le confer ; il nous reste à passer dire bonjour sur L2TPNS et faire un premier test. Il restera alors à Benjamin d'avancer sur le SI.
  - Fabien : créé un compte htpasswd sur le SI pour Stéphane Ascoet
  - Belette : monitoring des vpn : mise en place d'une sonde qui permet de vérifier que les vpn fonctionnent. Il bosse aussi sur "l'expérience utilisateur", càd voir l'état des services d'un point de vue utilisateur. Un compte de radius de test vpn a été créé pour les sondes d'Isengard (conf radius).
  - Caps : commencé à préparer une VM pour soulager leia de son gitlab (kamino.fdn.fr)
  - youpi : modification de la conf exemple VPN pour essayer différents profils: dans l'ordre UDP 1194, UDP 53, UDP 123, TCP 443, TCP 993, TCP 22, TCP 80.


# Évolutions de l'infra, investissements & roadmap

## Achat de switchs ?

On a reçu une offre intéressante pour des switchs Cisco Nexus 48 SFP+ 10G + uplink 40G à 2k€ pièce.
On en a pas strictement besoin actuellement. Mais Gitoyen est en train de passer au 10G, et un jour il faudra le faire.
Il se trouve que les prix sont très très intéressants. Se pose la question d'en acheter 2 et 1/3 pour FDN.
Si on fait ça, il faut aussi prendre en compte le prix des optiques, à changer.

Fabien voit avec Rosemonde si ça passe en tréso, mais on voudrait se lancer là-dessus.
Olb lance la commande avec Gitoyen et Globenet, si possible, avoir une facture dédiée pour FDN pour 2 switchs serait idéale.

contraintes techniques pour notre choix de switch :
* les mêmes switchs coté th2 et PB
* 48 ports
* au moins 4SFP+
* marque : cisco
* 2 switchs (si on partage le spare avec Gitoyen : s'aligner sur leur référence ; sinon réfléchir à prendre un spare de notre coté)




## RoadMap pour l'avenir

### Redondance réseau pbo/th2

###  Mail

Problème :

- besoin d'automatiser la création de boîte avec le si
- besoin de sécurisation des protocol de livraison
- limiter le nombre de livraison possible
- caractériser le service de mail : qu'est-ce que l'on veut fournir aux membres ?
- antispam (listes et mail perso)

1ère étape : écrire ce que l'on voudrait faire comme système de messagerie : tom28 (pas moteur),


### Cluster de vm pour membres


### Autres services à reprendre

- News
- Web
- Jabber


## Plus de gens dans adminsys ?

Formaliser un appel à énergie à destination des membres : lister les travaux qu'on voudrait voir réalisés et indiquer qu'il nous manque les moteurs nécessaires pour réaliser nos envies.
Cet appel à participation pourra être envoyé en même temps que le bilan du prochain admincamp avec l'annonce du wiki adminsys. Objectif : en faire un sujet préparé pour l'AG.
Sujet préparé, donc, au prochain admincamp (celui de janvier)


