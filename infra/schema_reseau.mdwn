[[!meta title="Schéma Réseau"]]

[[!toc levels=2]]

Le schéma et les informations ci-dessous date du 2017/05/20 (en cours de
migration de la collecte Nérim vers Liazo).

# Schéma high level du réseau FDN

[[!img fdn_network.0.10.svg size=x800]]

Ce schéma est une ébauche, il y a des choses à modifier, corriger, améliorer.

# Explication du schéma

_Retraduction des notes de blackmoor, il faut réorganiser , relire, corrigé, répondre aux '???'_


## Introduction

L'infrastructure de FDN est actuellement répartie dans deux datacenters
(nommée par la suite DC):

- Paris Bourse
- TéléHouse2 (nommé ensuite TH2)

Ils sont tous deux situé sur Paris.

Pour connecter son bout de réseau, FDN passe par Gitoyen.
Gitoyen à aussi une partie [ou tous ???] de sont infrastructure dans ces deux
DC.

Comme on le voit sur le schéma, FDN poccède [tout ou un bout ???] de la baie
Z1A11 à Paris Bourse et partage la baie 11A4 avec Gitoyen à TH2.


## Explications et détails du schéma

Les LNS ont chacuns 2 liens 1GbE:
- un pour la collecte
- un pour le transite et le réseau interne

Les connexions entre les deux switchs de Gitoyen sont en 10G.
Une des connexion fait quelques kilométres, l'autre passe par un autre chemin
[= très bien] et fait environs 15 kilométres.

Quasi tous les services sont sur les droides (en kvm [???]).
Cela comprend [???]:
- les VPNs
- le site FDN
- les sites des abonnées
- les serveurs DNS
- ...

Deux droides à Paris Bourse ne sont pas utilisés actuellement [voir ce que
l'on peut en faire]

Les droides poccèdes 3 liens réseaux, deux d'entre eux sont dédié à la
réplication.


## Vocabulaires

- bgp: 'Border Gateway Protocol', permet de se connecter au monde
- ganeti: gestionnaire de VMs, permet de créer, gérer, migrer les VMs
- LNS: 'L2TP Network Server', machine débian, servant pour la collecte xDSL


## Pourquoi avons nous certains choix d'architecture qui peuvent surprendre ?

Dans un monde idéal, on sait de la redonnance de services sur différent lieu,
ici on voit que toute la collecte est à TH2.
C'est historique: car Nérim d'était qu'a TH2 et le transiste Gitoyen aussi.
Aujourd'hui ce n'est plus le cas pour Gitoyen et FDN est en cours de
changement de fournisseur de collecte (Liazo) qui se trouve sur les deux DC
[???]

Il serait donc possible de redonder sur les 2 sites, mais cela amène peut-être
d'autre problème. [à étudier]


# Informations complémentaires

LDN possède la VM izengar avec un nagios pour nous aider à tester l'état de
nos services.

A Paris Bourse, FDN héberge une machine physique pour les RMLL.

Schéma de la vielle collecte et du routage chez FDN:
_À l'époque avant Nérim_ : [schema_collect_routage_fdn](https://wiki-adh.fdn.fr/essaimage:ressources:schema_collecte_routage_fdn)


# Chantiers

## Chantiers en cours

Les switch sont assez anciens. Ils sont en cours de changement.
Il y avait 1G vers Gitoyen, cale va passer à 10G avec les nouveaux.

## Chantiers potentiels

Les HDD des droides [???] limites actuellement la vitesse de réplication entre
les droides (1G)


