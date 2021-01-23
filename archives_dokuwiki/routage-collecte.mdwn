# Routage de la collecte ADSL pour les FAI locaux 

Dans le cadre du projet FFDN, FDN offre la possibilité aux FAI locaux de leur router sa collecte ADSL vers leur réseau afin qu'ils puissent profiter de ce service. Cette page recense les choses nécessaires à effectuer pour connecter un nouveau FAI, et liste ceux déjà connectés ou souhaitant une connexion.

# Prérequis pour demander à se raccorder à la collecte

  * Avoir une liaison jusqu'au LNS de FDN, en amenant un VLAN jusqu'au réseau de FDN
  * Avoir un trigramme qui sera utilisé pour le pseudo-realm (%yyy@fdn.nerim)
  * Des préfixes (v4/v6) à attribuer à ses abonnés
  * Un serveur radius prêt à accueillir des logins en xxxxx%leFAI@fdn.nerim
  * Un routeur qui routera les paquets…

# Préconisations pour les FAI

  * Pour être cohérent en v4 et v6, on réserve le même nombre de préfixes de site IPv6 que d'adresses IPv4. Donc il faut choisir la taille de préfixe de site que vous attribuez à vos abonnés : /48 ou /56 (si vous êtes radin). Ça vous donne ainsi, si vous réservez un /24 pour vos abonnés en v4, et que vous leur attribuez à chacun un /48, vous devez réserver un /40 (48-(32-24)) au total.
  * Prévoyez un peu votre « consommation » d'adresse à l'avance, ce n'est pas le genre de conf qu'on changera tous les quatre matins.
  * On vous propose deux interconnexions :
    * Une statique, où vous n'êtes relié qu'à un LNS, en statique
    * (à venir) Une dynamique, où vous mettez en place un speaker BGP avec une session sur chaque LNS afin d'en switcher dynamiquement
  * [à compléter]

# À faire chez FDN pour un nouveau FAI

## Sur les LNS

  * Allouer des adresses d'interco, soit dans la plage FDN (un /29 en v4 ; un /64 dans 2001:910:801::/48 en v6), soit dans une autre plage décidée par le FAI local (pareil, un /29 en v4 et un /64 en v6)
  * Ajouter un nom pour la table de routage dont on aura choisi un numéro consécutif aux précédents (dans /etc/iproute2/rt_tables)
  * Ajouter des règles de source-routing ; exemple (dans /etc/network/interfaces) pour l'interco 80.67.161.32/29 qui route 91.224.148.64/27 (en v6 on met les adresses dans le même paragraphe, mais en up/down afin d'éviter les merde de ifupdown), sur le VLAN 20 :

    auto eth0.20
    iface eth0.20 inet static
        address		80.67.161.34
        netmask		255.255.255.248
        up		ip rule add iif tun0 from 91.224.148.64/27 table tetaneutral
        down		ip rule del iif tun0 from 91.224.148.64/27 table tetaneutral
        up		ip -6 addr add 2001:910:801::1/64 dev $IFACE
        down		ip -6 addr del 2001:910:801::1/64 dev $IFACE
        up		ip -6 rule add iif tun0 from 2a01:6600:8080:4000::/51 table tetaneutral
        down		ip -6 rule del iif tun0 from 2a01:6600:8080:4000::/51 table tetaneutral

  * Ajouter les conf BIRD v4 et v6 dans /etc/bird.conf et /etc/bird6.conf, qui indiquent la route par défaut (et ajoutent une table, un proto direct qui injecte le préfixe d'interco, un proto kernel pour la synchro avec la table kernel, et un proto static qui injecte la route par défaut) et les inclure dans la conf principale (quand la version de bird qu'on utilise le supportera, utiliser les include avec fichier séparé /etc/bird[6]/leFAI.conf)
  * ifup l'interco et invoke-rc.d bird[6] reload

## Sur vador 

Dans /etc/freeradius/proxy.conf, ajouter une section :

    realm leFAI@fdn.nerim {
    type        = radius
    authhost    = 80.67.161.35:1812
    accthost    = 80.67.161.35:1813
    secret      = un_secret_bien_gardé
    nostrip
    }

puis invoke-rc.d freeradius reload

(en parenthèse, la gestion de ces realms s'est fait grâce à l'instanciation d'un nouveau module pour gérer les suffixes en xxxxx%yyy@fdn.nerim ; un invok-rc.d freeradius restart est nécessaire pour qu'il soit chargé)

# Liste des FAI connectés

(Avec leur trigramme entre parenthèse)

  * Tetaneutral.net (ttn) (vlan 20)
  * Franciliens (idf) (vlan 2019 ==> Absolight en baie 12G2 à TH2)
  * Rézine (rzn) (vlan 21)
  * Sames Wireless (sms) (vlan 22)
  * Pclight (rit) (vlan 2052 ==> Absolight en baie 12G2 à TH2)
