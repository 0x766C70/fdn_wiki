[[!tag done]]

Dates: 23/24 avril    
Lieu: 60 rue des Orteaux, Paris 20e    
Présent⋅e⋅s : Fabien, Olivier, Belette, Ben, Khrys, Kankan, Nono, Scara, Mat, Clément, Benjamin

[[!toc levels=1]]

# Choses faites

## DNS

Les zones slaves du bind de vador et leia ont été virées, ils ne font plus que
resolvers maintenant.

## Let's encrypt

C'est testé, mis en prod, documenté dans le wiki ([[outils/letsencrypt]]). On
en a profité pour améliorer un peu les configs ssl/tls des serveurs web
concernés.  Il reste à passer au moins sur les mails, sur blog.fdn.fr, sur
lists.fdn.fr, sur le webmail...

## web.fdn.fr

Le site web www.fdn.fr ayant déménagé de machine, et cette adresse étant
utilisée pour le web mutualisé certains services associés ne fonctionnent plus.

- Les outils accessibles sur yoda en www.fdn.fr sont maintenant accessible en web.fdn.fr (olb).
- reparer awstats qui est dans les choux depuis la nouvelle version du site (olb)

## Droïdes

- droïdes : réinstaller c3px [fait, clément et olb]
- droïdes : ajouter les deux autres disques sur r4p17 [fait, clément et olb]

## Monitoring à distance

belette

- Mise en place de isengard.fdn.fr : monitoring à distance (nagios) & vue pour les membres (cachet).
- https://adminsys.fdn.fr/outils/supervision/remote_monitoring/

## Nouvelle machines kylo

- création de la machine kylo
- déménagement en cours de vador vers kylo, pas fait pour cause de TTL trop grand.
- début de migration de flyspray

## Sauvegarde de la conf des switchs

- Clément a documenté l'outil oxidized, il faut le mettre en prod : https://adminsys.fdn.fr/outils/oxidized/
- C'est fait, les switchs sont maintenant backuppés avec oxidized. Une page a été créée dans le wiki pour cet outil.


## creation d'un compte mail

- pour flo44 -> mail envoyé pour verifier abonnement


# Choses à faire

- mettre en place le système de rôles pour les authorisations (olb)
- Passer sur la config SSL/TLS des mails
- mettre en place oxidized
- avancer sur le monitoring (conf check_mk, nettoyage nagios, réparer ce qui est en alerte)
- créer une nouvelle vm pour les vpn (2 cpu)
- migrer les resolveurs
- migrer le wiki
- migrer le MX secondaire de vador
- inscrire automatiquement la liste adminsys@ à benevoles@
- boite à sous (olb, fait)
- vpn : il faudrait encore virer l'ancienne allocation dans le reverse DNS de 2001:910:802::/64 qui ne servira pas finalement.


# Réu coordination samedi 16h45

Présent·e·s : mat, ben (bla), fsirjean, olb, clément, belette, nono, scara, kankan, khrys, youpi (remote), quota (remote), benjamin

## Organisation des admincamp 

- gestion du bruit et de l'espace
- les sous nouriture :
    
    benjamin : 22 + 16 + 50
    olivier : 20
    khrys : 18
    scara : 1 brownie + 1 bouteille
    belette : 20

olb fait une boite à sous à prix libre. L'ensemble du contenu (80€) à été donné
à Benjamin.

- remboursement des billets de train : olb (~140), scara (~80), fabien (~60)


## Validation de notre fonctionnement

cf https://adminsys.fdn.fr/fonctionnement/

Validé.

## liste adminsys@ et liste benevoles@

Inscrire automatiquement toutes les personnes de la liste adminsys (et autres listes d'ailleurs) à la liste benevoles

Validé, à toi stéphane ;)

## VPN : pousser une IPv6 automatiquement sur les VPN

  - on avait décidé de pousser automatiquement le dernier /64 du préfixe pour configurer le lien: 2001:910:1301::/48 -> 2001:910:1301:ffff::/64
  - activé ce matin l'ajout automatique par le SI au moment de la création du VPN
  - TODO: il faudrait encore virer l'ancienne allocation dans le reverse DNS de 2001:910:802::/64 qui ne servira pas finalement.
  - est-ce qu'on ajoute systématiquement l'adresse aux anciens VPNs déjà en place ?
    - Le souci c'est que ça override une configuration que l'abonné aurait mise de son côté.
    - Éventuellement rendre le champ modifiable dans l'interface vador de l'abonné, pour qu'il puisse choisir quoi y mettre ? (en vérifiant que c'est bien dans le préfixe, qui lui n'est pas modifiable)
    - TODO (youpi): on a décidé de changer la config pour les anciens VPN, en prévenant à l'avance que ça va changer, pour ceux qui auraient déjà configuré eux-même


## Collecte xDSL

Clément et Ben souhaitent participer à cela. Nicolas du bureau également. L'idée est d'aller voir Liazo à trois.

[TODO Fabien : passer les infos & contacts à Ben].


## Point de suivi des chantiers

- Let's encrypt
  - appliqué à https://adminsys.fdn.fr/
  - utilisé les scripts de grenode qui juste marchent, en cours de doc dans le wiki adminsys, et on pourra le faire sur les autres sites
  - essayer de maintenir une liste des domaines gérés par le script
  - next step: automatisation via puppet?
- LNS
- Droïdes
- DNS
- Vador
  - dns autorité migrés
  - reste le wiki et un mx secondaire
- Monitoring & VM externe ?
- Backups
- Backup conf des switchs


## Monitoring

### Passage à check_mk

Ça avance doucement, travail de fond. Du boulot encore. Le TODO est sur le
wiki adminsys, au début de la page [[outils/supervision/check_mk]]).

Belette et nono s'y collent.

### Remote monitoring via Nagios sur VM

Belette se lance

Voir avec sebian de LDN pour monter une VM pour nous (merci sebian! up & running).

Cf [[infra/machines/isengard]] et [[equipe/tiers/ldn]].

### Cachet (système de visualisations/notifications) human friendly

* cachet.io
* status.framasoft.org

#### Plugins / Intégrations

* https://github.com/mpellegrin/nagios-eventhandler-cachet
* https://github.com/bimlendu/sensu-cachethq
* https://github.com/SamuelMoraesF/CachetNotifier
* https://github.com/willdurand/hubot-cachet


## divers

- web.fdn.fr : changement du nom du web mutualisé. Notament pour les outils tels que awstat & co.
- scripts fdn_ipmi_kvm, fdn_ipmi_sol : permet de prendre facilement la main sur les machine physique.


## Préparer une intervention à TH2

- déplacer un LNS
- benner un vieux LNS
- benner vador : les dns faisant autorité ont été migrés, il reste le wiki adhérent, et un mx secondaire.

Ça semble jouable de virer vador en juin. Il faut en discuter avec Gitoyen pour le faire avec eux. Il y a une commande de matériel à faire avant. Ben s'occupe de la commande de matos, Fabien lui file les infos.


## Prochaines dates d'admincamp

- 25/26 juin 2016
- 24/25 septembre 2016
- 19/20 novembre 2016
- 21/22 janvier 2017


## Déploiement du pelican de open.fdn.fr

Fabien voit avec caps pour trouver un fonctionnement.

