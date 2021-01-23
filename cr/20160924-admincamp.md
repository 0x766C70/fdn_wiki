[[!meta title="Admincamp n°7 - 24/25 septembre 2016"]]
[[!meta date="20160924"]]
[[!tag done]]

# Présences

**venir c'est bien, s'inscrire en plus c'est mieux !**

Là : olb, fabien, Scara (com'), Benjamin (cuisine et SI), caps', tom28 (samedi uniquement),belette (samedi uniquement), blackmoor, vg, DelTree (sans PC sauf miracle)

Pas là : Stéphane Ascoët (autre événement militant, dommage j'aurais bien assisté à l'enterrement de Vador), mat, nono


# Coordination

## Changer de secrétaire tournant

Pour rappel, le/la secrétaire est une personne chargée de s'assurer que les
mails reçus sur la liste adminsys@ reçoivent une réponse.  Ça suppose de
répondre aux gens comme quoi on a reçu leur demande, et d'aller taper sur
celleux qui savent faire pour que ça soit traité.  C'est aussi un bon moyen
d'apprendre, en se mettant en doublon sur les interventions programmées.

Blackmoor se propose pour la prochaine session (jusqu'en novembre).


## Prochain admincamp ? (collisionne avec Capitole du Libre)

Il est décidé de décaler le prochain admincamp au 11-12-13 novembre : on espère
que tout le monde pourra venir, les présent·e·s sont tou·te·s dispos.  Il
faudra envoyer des mails rapidement pour prévenir (notamment Régis qui avait
dit vouloir venir).


## Qui porte le projet collecte Liazo ?

Il y a un enjeu fort autour de la collecte ADSL chez Liazo. Coté Bureau, la
contractualisation a été faite mi septembre. 

Les aspects SI se gèrent avec Benjamin, il va y avoir du travail sur la tréso
et le suivi ADSL. 

Il y a nécessité d'avoir une ou deux personnes qui coordonnent le sujet. 

Benjamin et Olb vont s'y coller, l'un pour les aspects dev SI, l'autre en tant
que personne ressource sur les aspects système et réseau.  CapsLock et Fabien
sont volontaires pour plancher (et apprendre) sur le sujet.

## Rappel de la dernière fois

### Rappel : propositon de maintenir un changelog global sur le wiki

L'idée est d'avoir un endroit où chaque personne qui fait quelque chose sur l'infra racconte ce qu'il a fait (et met des liens vers la doc).
C'est pratique pour se faire idée de se qui se passe, et ne pas être largué quand on essaye de raccrocher.

### Prochain gros chantier : ménage dans la baie 11A4 de Téléhouse2

- benner une machine inutilisée
- éteindre et benner vador
- déplacer un lns à coté de l'autre et du switch

Pour cela, il est nécessaire de :
- migrer le wiki adhérent (olb)
- migrer le mx secondaire (tom28)
- commander des rails adaptés à la baie télécom en 11A4 à Téléhouse 2 (fait [fabien]).

### Création d'un troisième résolveur DNS hors de l'AS de Gitoyen

Sur isengard.

À priori, il sera limité à l'AS auquel FDN participe.



# Choses à faire (non exhaustif)

## puppetiser la conf des droïdes pour jessie (notamment /etc/lvm/lvm.conf ?)
## Annoncer adminsys.fdn.fr sur bénévoles/membres
## tunnels chiffrés: alléger les filtres dans bird lns01, lns02
## https: continuer let's encrypt que manque-t-il ? Le serveur Sympa mais apparemment c'est pas simple - Bah faut avancer sur solo quoi. Tom28 & Fabien étaient sur le coup.
## configurer chewie memoire vive / apache & mysql
## web asso: migration de blog.fdn.fr sur chewie
## etckeeper : faire un mail à admin@ quand /etc change
## resolver DNS : migration des resolvers DNS sur resolver2
## noyau : mettre en place le système de rôles pour les authorisations (olb)
## mails : Passer sur la config SSL/TLS des mails
## tunnels chiffrés : créer une nouvelle vm pour les vpn (2 cpu)
## tunnels chiffrés : il faudrait virer l'ancienne allocation dans le reverse DNS de 2001:910:802::/64 qui ne servira pas finalement.
## supervision : plein de boutons à tourner, de sondes à ajouter, de trucs et de machins à puppetiser...
## supervision : pertinence d'alertes par mail ? pas pour tout, bien sûr
## nanobsd gitoyen, soucis d'etherchanel (need help)
## livraison gitoyen-fdn pbo, redondance
## Mise en place d'un virtualenv pour le site vpn openbar sur chewie
## Déprovisionner les radius TTN et la conf ADSL (checks nagios, L2TPNS...)
## Toujours des problèmes sur les accès adhacc et le wiki adminsys...
## Migration de Gitlab vers une machine dédiée (soulager leia)
## Migration de puppet master vers une machine dédiée (soulager leia)

## ...


# Choses faites

Cf [[changelog]].

