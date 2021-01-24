# VPN événementiel

Il nous arrive de fournir de l'IP pour des événements, à travers un VPN. Par exemple, ici, on prépare un /23 pour le POOP 2015.

## Réservation des IP

Il faut demander à Gitoyen d'assigner un bloc temporaire, pour la durée de l'événement. 
Ici, Gitoyen nous a passé l'info qu'on avait 80.67.184.0/23 :

    inetnum:        80.67.184.0 - 80.67.185.255
    netname:        FR-FDN-POOP
    descr:          Réseau temporaire dédié au PooP
    descr:          http://poop.leloop.org/
    country:        FR
    admin-c:        GI1036-RIPE
    tech-c:         GI1036-RIPE
    status:         ASSIGNED PA
    mnt-by:         GITOYEN-NCC
    remarks:        abuse-mailbox: abuse@gitoyen.net
    created:        2015-06-10T20:27:04Z
    last-modified:  2015-06-10T20:27:04Z
    source:         RIPE # Filtered

## Créer un VPN dédié à l'événement

Depuis l'interface adhérent de n'importe qui (comprendre, soit l'asso organisatrice si elle est adhérente, soit un membre de l'orga, soit un admin FDN...), ouvrir un VPN. On peut éventuellement modifier le tarif du VPN pour le passer à zéro depuis le SI, si on veut.

## Ajouter un attribut radius

On ajoute le range associé au VPN comme attribut radius.
Dans le SI, sur la page du VPN, compte radius associé, attributs de l'utilisateur, ajouter : 

    Nom de l'attribut :        Framed-Route
    Opérateur :                =
    Valeur de l'attribut :     80.67.184.0/23
    Type :                     reply
    User id :

## Ajouter les routes dans bird

Sur les serveurs openvpn (vpn1 et vpn2), on édite /etc/bird.conf et on ajoute une ligne dans is_tunnel() en s'inspirant des lignes existantes :

    function is_tunnel() {
        return
                (net ~ 80.67.176.0/22 && net.len = 32)
                ||
                # 80.67.168.0/27 = core gitoyen
                (net ~ 80.67.168.0/24 && ! (net ~ 80.67.168.0/27))
                ||
                (net ~ 80.67.166.0/24)
                ||
                (net ~ 80.67.165.0/26)  # NET-FDN-DE-LA-FERME
                ||
                (net ~ 80.67.160.0/24)
                ||
                (net ~ 80.67.167.0/24)  # FAIMAISON
                ||
                (net ~ 80.67.184.0/23)  # FDN-POOP
                ;
    }

Puis sur les lns on édite /etc/bird.conf, fonction abonne() :

    function abonne() {
        return
                (net ~ 80.67.176.0/22 && net.len = 32)
                ||
                # 80.67.168.0/27 = core gitoyen
                (net ~ 80.67.168.0/24 && ! (net ~ 80.67.168.0/27))
                ||
                (net ~ 80.67.166.0/24)
                ||
                (net ~ 80.67.160.0/24)
                # rhizome
                ||
                (net ~ 80.67.175.128/26)
                ||
                (net ~ 80.67.168.112/29) # loupi
                # Franciliens
                ||
                (net ~ 79.143.250.128/25 && net.len = 32)
                ||
                # Rezine
                (net ~ 193.33.56.32/27 && net.len = 32)
                ||
                (net ~ 80.67.180.0/24) # ILICO
                ||
                (net ~ 80.67.167.0/24) # FAIMAISON
                ||
                (net ~ 80.67.184.0/23) # FDN-POOP
                ;
    }
  
## Relire la conf bird

On demande à bird de relire sa conf sur les machines où on l'a modifiée :

    lns01:~# birdc
    > config soft

## On teste

Il peut être utile de tester en se connectant au VPN (récupérer login et secret dans le SI), et en montant une IP dans le range routé sur une interface derrière le VPN. Si ça ping depuis l'extérieur, on a gagné.

## Nettoyage après l'événement

Sur chacune des machines concernées (VPN et LNS), enlever les lignes ajoutées ci-dessus dans le fichier /etc/bird.conf puis dire à bird de recharger sa config :

    killall -HUP bird
