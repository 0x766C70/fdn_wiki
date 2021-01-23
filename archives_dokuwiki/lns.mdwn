# C'est quoi un LNS ?

Les LNS sont un peu la « pièce maîtresse » de FDN : ils reçoivent les tunnels de la collecte ADSL et routent ce trafic vers notre transitaire, Gitoyen. Ils sont donc l'intermédiaire entre la collecte qu'on reçoit en L2TP, et le trafic IP avec le reste d'Internet.

# Comment ça marche

Expliquer l2tpns, le mode cluster et ses subtilités…

# Comment c'était avant (et encore aujourd'hui)

## Côté collecte


À l'époque de Cegetel/Neuf, les deux LNS étaient en cluster. La collecte arrivait sur l'IP des LNS par une seule adresse de gateway d'un LNS : la route était statiquement définie côté Cegetel. Le trafic retour vers Cegetel provenait par contre bien des deux LNS.

Puis, quand vint Nerim, les deux LNS n'ont pas été remis en redondance : seul un a été mis en place. Cf [[adsl:migration|Interlocuteurs]].

## Côté Gitoyen

Du côté Gitoyen, un Fondry FWS4802 a toujours fait intermédiaire avec les LNS (et donc les accès ADSL). Il sert à annoncer les routes en BGP à Gitoyen (en IPv4 seulement, qu'il reçoit des LNS, pour l'ADSL), et est capable de faire du multipath, chose nécessaire au fonctionnement en cluster de l2tpns. Pour IPv6, une route statique est définie chez Gitoyen, qui envoie le trafic sur lns01 ; on ne se préoccupe donc pas du Foundry.

Les 3 routeurs de Gitoyen (x-ray, yankee et zoulou) portent l'IP 80.67.169.1 sur une interface carp. Le Foundry a une patte dans 80.67.168.0/27 (le backbone de Gitoyen) où il annonce les routes de FDN (où on le trouve sur 80.67.169.2).

# S'entraîner

[[adminsys:lnssandbox|Créer un « bac à sable » de l'architecture de routage de FDN]]

# La migration vers une « nouvelle » architecture

Voir la page de travaux pour ce qui est en cours : [[travaux:upgrade_lns|Mise à jour des LNS]]

## Configuration réseau prévue des LNS

on évolue dans le cadre suivant :
  * on va communiquer vers l'extérieur, via Gitoyen (= "route par défaut") ; on s'interconnecte en BGP (20766 coté Gitoyen, AS privé coté FDN) \\
  * on va communiquer avec Nerim, pour leur annoncer nos routes (les ips des LNS), et recevoir d'eux l'accès vers les BAS FT/SFR ; on s'interconnecte en BGP (13193 coté Nerim, AS privé coté FDN) \\
  * on va encore communiquer avec SFR-anciennement-Cegetel (raisons historiques, et peut servir pour des tests) ; routage statique \\
  * on va avoir à communiquer avec des FAIs associatifs tiers (source-routing des connexions qu'on termine pour eux) ; interconnexions non définies, pour l'instant 

## Futur de la communication avec Gitoyen

Un /29 est prévu pour chacun des membres, pour s'interconnecter en BGP avec les routeurs de Gitoyen.

Pour FDN il s'agit de 80.67.168.208/29 dans le VLAN 119.
  * 80.67.168.209 = x-ray
  * 80.67.168.210 = yankke
  * 80.67.168.211 = zoulou
  * 80.67.168.213 = lns01
  * 80.67.168.214 = lns02

Subnet ipv6 2001:910:0:800::/64 dans le VLAN 119.
  * 2001:910:0:800::209 = x-ray
  * 2001:910:0:800::210 = yankke
  * 2001:910:0:800::211 = zoulou
  * 2001:910:0:800::213 = lns01
  * 2001:910:0:800::214 = lns02

Dans le futur, il faudrait que les ip 80.67.169.1 et 2001:910:800:: soit portée par les routeurs d'FDN.

### roadmap pour que les LNS soient directement connectés à Gitoyen

( pour les étapes "gitoyen", j'ai (domi) les accès nécessaires )

Préfixes pour les filtres :
  * 80.67.176.0/22 : ip individuelles des connectes adsl/vpn
  * 80.67.166.0/24 : subnet SamesWireless
  * 80.67.160.0/24 : subnets abonnés
  * 80.67.175.128/26 : subnet rhizome
  * dans 80.67.168.0/24 mais pas 80.67.168.0/27 : subnets abonnés, mais protéger 80.67.168.0/27 qui est le core gitoyen
  * 80.67.169.0/24 : subnet serveurs
  * 80.67.161.0/24 : subnet serveurs, interco, bazar

Etapes :
  * configurer les ips sur chaque LNS **ok**
  * configurer les ips sur chaque routeur Gitoyen **ok**
  * vérifier la connectivité **ok**
  * décider si on veut prendre une full-view de Gitoyen ou pas 
  * configurer les sessions BGP ( local AS 65432 ) de chaque LNS vers chaque routeur Gitoyen **presque**
    * lns01 vers x-ray, yankee, zoulou **ok**
    * lns02 vers x-ray, yankee, zoulou **ok**
    * filtre des préfixes « vers Gitoyen »
  * configurer les sessions BGP sur chaque routeur Gitoyen **presque**
    * x-ray vers lns01, lns02 **ok**
    * yankee vers lns01, lns02 **ok**
    * zoulou vers lns01, lns02 **ok**
    * filtres des préfixes « reçus de FDN »
Plus tard :
  * passerelle en vrrp/carp/whatever 80.67.169.1 sur les 2 LNS **ok**
  * supprimer le carp 80.67.169.1 sur x-ray, yankee, zoulou **ok**

# Les trucs à savoir

  * Pourquoi on voit des messages du genre “bird: Netlink: No such process” dans le syslog des LNS ?

En fait, quand un abonné se connecte, l2tpns ajoute une route dans la table de routage du kernel pour l'atteindre. Si auparavant, il existait une route pour cet abonné en passant par l'autre LNS, elle va être remplacée car l2tpns « force » l'ajout de sa route. Bird va alors voir qu'il existe une route kernel, qui est configurée pour être plus prioritaire que la route passant par l'autre LNS et qu'il a mise en place, et il va donc vouloir supprimer celle-ci. Sauf qu'elle a déjà été écrasée par l2tpns, et donc le kernel ne va pas la trouver lorsque bird demandera sa suppression : d'où cette erreur.

  * le module nf_conntrack fait bouffer bien 2 fois plus de CPU même si on n'utilise pas iptables -> on met 

install nf_conntrack /bin/true

dans /etc/modprobe.d/no-conntrack.conf, pour éviter qu'il se charge tout seul (e.g. en appelant iptables -L -t nat)

  * vador.fdn.fr se connecte aux lns pour récupérer les stats -> il faut ajouter la clé publique de root@vador dans lns:/root/.ssh/authorized_keys , y installer rsync , ajouter le nom lnsxy dans SRVLIST de vador:/usr/local/bin/syncrrd.sh , et s'assurer que

vador# ssh root@lnsxy

fonctionne. Il faut également ajouter le nom lnsxy dans FDN-libs/Adsl/Adhs.pm et FDN-libs/cgi/adh/adh-statimg.cgi et les mettre à jour sur Vador.

## Installation des nouveaux lns (2015)

  * éteindre port du vieux LNS secondaire
  * configuration d'un nouveau LNS
  * copie de la conf réseau
  * configuration du switch
  * installation de bird
  * installation de mysql :
    * Replication MySQL over TLS, parce qu'avec TH2 et PBO, on traverse des réseaux tiers.
    * Besoin d'une PKI, création en cours sur si.fdn dans /etc/pki (see Readme)
    * Ajout des paramètres x509 dans la conf du mysql sur si.fdn.fr
    * Ajout des paramètres x509 dans la conf du mysql sur lns22
    * Replication SQL après backup & lock tables sur si, avec MASTER_SSL=1 lors du change master.
    * Recréation de l'user l2tpns via la commande donnée dans freeradius/sql.conf
  * mise en route d'un nouveau LNS en tant que secondaire et tester
  * deracker le vieux LNS secondaire
  * racker le nouveau LNS secondaire
  * switch secondaire/primaire
  * eteindre et deracker le deuxième vieux LNS
  * racker le deuxième nouveau LNS 
  * envoyer un mail
    
services :
  * keepalived
  * l2tpns
  * mysql
  * freeradius
  * bird
  * bird6
