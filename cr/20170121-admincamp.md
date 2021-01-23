[[!meta title="Admincamp n°9 - 21 janvier 2017"]]
[[!meta date="20170121"]]
[[!tag done]]

Pad : [[https://pad.gresille.org/p/aiqu9ah4ua-fdn-admincamp-20170121]]     
Lieu : local de La Quadrature du Net, 60 rue des Orteaux 75020 Paris, France    
Là : Olb, Fabien, quotah, Caps', guerby (si guest ok :) => oui), mat, blackmoor, vg, belette (samedi), tom28 (dimanche après-midi avec son fork), petit, DelTree    
Pas là : Bernard Cazeneuve    
À distance : Youpi sauf le samedi après-midi, tom28 (samedi par intermittence) ; Bruno Le Roux ; benoit   


# Réunion du Samedi 21 Janvier 2017 (début 15h30)

## Préparation de l'aprèm

> - quel est l'état de l'équipe ?
> - est-ce que l'on a besoin/envie de changer le noyau ?
> - a-t-on été assez inclusifs pour accueillir de nouveaux membres (communication, invitation à participer aux admincamps, etc ?)
> - est-ce qu'on arrive à suivre les projets / contributions au fil des admincamps ?

Qu'est ce que l'on veut produire ?

- une présentation pour l'AG ?
- un bilan sur le site web

Deux petit groupes :

→document bilan de ce qui a été fait (qq persones) + roadmap
→comment ammeliorer la transmission/formation/suivi, l'intégration ?


## Bilan adminsys 2016

> - Qu'est-ce qu'on a fait ?

### Fonctionnement de l'équipe

- Mise en place de la dynamique des admincamps
- Mise en place d'un noyau décisionnel et de roles satellites
- Autonomisation du groupe
- Reprise d'une activité & vision à long terme sur l'adminsys FDN

### Outils de l'équipe adminsys

- Gestion complète des authentifications via puppet (dont la capacité de supprimer des droits d'accès)
- Mise en place d'une liste abuse@
- Passage à etckeeper
- Mise en place d'un wiki adminsys type ikiwiki
- outil de backup des configurations des switchs

### Remise à plat de l'infra

- Ménage de tous les comptes unix sur les machines
- Ménage physique en baie (à TH2, à PBO)
- Remplacement des serveurs par des machines neuves : droides + lns/routeurs
- Remplacement des switchs (en cours)
- Remise à plat du cluster de virtualisation (jessie, problèmes de perf...)
- Rationalisation des machines physiques / virtuelles / VM :
    - Suppression des machines historiques inutiles
    - Répartition entre TH2 et PBO
    - Rangement et cloisonement des services dans des VM adéquates (blog, site web, wiki, gitlab...)
- Ménage dans les configurations, sédimentations, vétusté...

### Travail sur les services

- Mise en place de la collecte liazo (en cours) 
- Évolution du monitoring

    - Passage à checkmk pour monitorer nos modifs sur les différentes machines

    - Mise en place d'une supervision compréhensible par les membres (page de statut en quelque sorte) via Cachet et Nagios

    - Mise en place de tests d'un point de vue abonné (pour le VPN, services TCP/UDP, web...)

    - Supervision depuis ailleurs que FDN (Isengard)

- Passage à Let's Encrypt pour nos services Web + ML
- DNS : nouvelle infra DNS (serveurs auth / récursifs séparés, gitification, délégation des zones...)
- Services web de l'asso : 
    - Nouveau site web FDN
    - Blog et vpn openbar

## Roadmap 2017

> - comment on se projette ?
> - qu'est ce qui nous fait envie ?
> - de quoi a besoin l'asso ?

Tempête de cerveaux :

### Ce qui concerne juste adminsys

- MàJ des machines (bientot stretch !)
- Mise en place des nouveaux switchs 
- tuning des résolveurs pour les renforcer en cas d'attaque ; dnssec, DNS over TCP ?
- DNS faisant autorité : est-ce qu'on met en place dnssec ?
- Réinstaller un serveur jabber non troué (avant ça, demander sur la liste si quelqu'un s'en occupe)
- vulgarisation de la mise en place de certains outils/services/pratiques (selon pertinence politique) type DNS, VPN, xDSL...
- Maintien et jardinage de notre wiki / documentation technique / réorganisation de la hiérarchie 

### Ce qui concerne AG

- proposer aux membres d'héberger physiquement leurs machines à PBO
- proposer l'hébergement de VM pour les membres
- proposer un service de monitoring mutualisé entre membres ?
- remise à plat de l'hébergement Web mutualisé (est-ce que ce service est toujours voulu / maintenable par les équipes en présence ?)
- remise à plat de l'hébergement mail (est-ce que ce service est toujours voulu ouvert aux membres / maintenable par les équipes en présence ?)
- Mettre en place une infra NTP (vieille demande de Thy) ??
- liste à compléter par les idées des membres
- vos envies ?

→ lancement d'une discussion sur AG avec reply-to sur benevoles sur les évolutions (à voir avec / en coordination avec le projet du buro)


## Fonctionnement, intégration, transmission, suivition...

### 1 - trouver des gens « sang neuf »

Problématiques :

- peur du côté technique et de pas savoir où on arrive
- fonctionnement opaque vu de l'extérieur
- venir aux admincamp, c'est pas facile en terme de trajet

Propositions :
    
- énoncer un code de conduite pour assurer un cadre soft / non excluant dans les deux sens ; permettant à chacun de pouvoir venir en sachant à quoi s'attendre (repères)
- plus de communication sur ce que l'on fait : 
    * sur l'ambiance photos dans le wiki, autres activités éventuelles
    * compte-rendu des admincamps à destination de bénévoles
- marquer des tâches comme faciles à faire pour les nouveaux/nouvelles
- proposer des moments visioconf ? par exemple quand on est en mode réunion ?

### 2 - les faire rester

Problématiques :

- problèmes d'"engagement"
- Frustration vis à vis de la vitesse de réalisation des tâches
- manque d'identification des "responsables" des tâches

Propositions :

- Assigner des tâches / désigner un "responsable" pour les tâches en cours de réalisation (pour les tâches récurrentes : on documente)
- écrire une page "comment rejoindre le groupe adminsys" (toutes les info pratiques)
- inclure un lien vers une page Integration nouveaux/nouvelles dans les communications faites aux bénévoles
- parainage des nouveaux
- faire des admincamps dédiés à l'accueil des nouveaux dont certains potiellement centrés sur un sujet technique annoncé à l'avance
- rendre addict par des récompenses
- s'astreindre à écrire ce que l'on fait dans le changelog
- Une réu à distance entre chaque admincamp ? Téléphone ? IRC ? Faire le point sur ce qui a été fait.  Préparer l'admincamp suivant, envoyer le mail d'annonce...


## Préparation pour l'AG

### Proposition de sondage : 

https://pad.gresille.org/p/RcwTSYCLvT-sondage-fdn-ag-2017

### Proposition de slides pour l'AG

[ Présentation intéractive ? ]

Plan : 

- Fonctionnement actuel du groupe adminsys

    - objectifs qu'on s'est fixé

- Créer une nouvelle dynamique

- les roles (admincamp uniquement) :

   - adminsys

   - secrétaire

   - noyau

- Rendre lisible les actions entreprises (CR ; Changelog lisible ; soins autour du wiki)

    - cadre de travail lors des admincamps / Humaniser la chose (programme type ; commodités du lieu ; photos ; tweets ; ...)

- « C'est un truc de geeks » (introduction à la section suivante ->) 

   - Talkshow de la com? (parler de leur expérience admincamp)

- Nous rejoindre / intégrer l'équipe

  - Page web dédiée (outils...)
  - Proposition d'admincamp d'accueil / expliquer qu'on peut mettre en place très facilement des parainages pour accompagner les nouveaux
  - La Dark infra c'est (presque) fini : on a viré plein d'historique ; on repart sur des bases neuves (cloisonnement des services ; ...)

- Travaux réalisés : mise en valeur

- Roadmap - (faire adhérer)

- Comment participer (bis repetita)


# Coordination (dimanche après midi)

## Changer de secrétaire tournant

Pour rappel, le/la secrétaire est une personne chargée de s'assurer que les
mails reçus sur la liste adminsys@ reçoivent une réponse.  Ça suppose de
répondre aux gens comme quoi on a reçu leur demande, et d'aller taper sur
celleux qui savent faire pour que ça soit traité.  C'est aussi un bon moyen
d'apprendre, en se mettant en doublon sur les interventions programmées.  Le
secrétaire est aussi chargé d'annoncer les dates du prochain admincamp sur ag@
(attention perturbations) et benevoles@ (pad + inscriptions) environ un mois
avant.  Le role de secrétaire est réatribué à chaque admincamp.

→ olb (olb demande à belette).


## Rappel des prochaines dates d'admincamp

- 11/12 mars 2017
- 20/21 mai 2017, spécifique accueil nouveaux/nouvelles
- 5/6 aout 2017
- 14/15 octobre 2017

## Choses à faire pour le prochain admincamp

- ramène des sfp glc-t cisco pour tester (tom, olb)
- finir la migration de gitlab (mat)
- proposer un code de conduite (fabien)
- mettre une todo dans le wiki (fabien)
- (avant la prochaine mais à faire : sondage et slides pour l'ag : caps, belette, fabien ?, ?)
- Créer la page "nous rejoindre" sur wiki admin (+infos pratiques) (olb, fabien)
- AG : présentation / animation / présence autour d'un sujet sur l'adminsys FDN (caps, belette)
- Page sur site fdn.fr pour promouvoir adminsys/admincamp (fabien, olb)
- Préparation du sondage (type framatruc) pré-AG (pour la préparation un pad va être lancé par le buro) (caps, belette, blackmoor)
- "Photos dans mon telephone" (Fabien)

## Sous

On a depensé entre 150 et 200€ pour la nouriture sur l'admincamp, pour deux jours et une quinzaine de personnes.

## Reporté 

→ question plus générale de la transformation des admincamp : pourquoi on vient
aux admincamps ? (Pour rencontrer les gens ?)


