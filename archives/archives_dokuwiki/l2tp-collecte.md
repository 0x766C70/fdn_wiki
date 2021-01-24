# Livraison par tunnel l2tp, de la collecte ADSL pour les FAI locaux 

Dans le cadre du projet FFDN, FDN offre la possibilité aux FAI locaux de leur router sa collecte ADSL vers leur réseau afin qu'ils puissent profiter de ce service. Cette page recense les choses nécessaires à effectuer pour connecter un nouveau FAI, et liste ceux déjà connectés ou souhaitant une connexion.

# Prérequis pour demander à se raccorder à la collecte

  * Avoir un serveur radius et LNS (Radius et LNS peuvent être hébergé sur le même serveur). Le serveur radius devra être prêt à accueillir des logins en xxxxx%monfai@fdn.nerim.
  * Des préfixes (v4/v6) à attribuer à ses abonnés.

# À faire chez FDN pour un nouveau FAI

## Sur vador 

Dans /etc/freeradius/proxy.conf, ajouter une section :

    realm monfai@fdn.nerim {
    type        = radius
    authhost    = 80.67.161.35:1812
    accthost    = 80.67.161.35:1813
    secret      = un_secret_bien_gardé
    nostrip
    }

puis invoke-rc.d freeradius reload

(la gestion de ces realms s'est fait grâce à l'instanciation d'un nouveau module pour gérer les suffixes en xxxxx%yyy@fdn.nerim ; un invok-rc.d freeradius restart est nécessaire pour qu'il soit chargé)

# À faire chez le FAI Local

Dans /etc/freeradius/clients.conf 
  
    # A remplacer par l'IP du radius FDN
    client 80.67.176.122 {
        shortname = radiusfdn
        secret = testing123
        nastype     = other
    }

Dans /etc/freeradius/proxy.conf
    ...
    realm monfai@fdn.nerim { 
	type = radius
	authhost = LOCAL
	accthost = LOCAL
    }
    ...

Dans /etc/freeradius/sites-enabled/default ajouter le module "realmpercent"
    ...
    authorize {
    ...
        realmpercent
        suffix
    ...
    }
    ...

Un exemple de configuration (fai avec 2 LNS en load balancing) d'un fichier /etc/freeradius/users  (remplacez les IPs de  Tunnel-Server-Endpoint par les IP de vos LNS)

    DEFAULT Auth-Type := Accept, Realm == "monfai@fdn.nerim", NAS-IP-Address != "80.68.167.11"
        Tunnel-Type:1 = L2TP,
        Tunnel-Medium-Type:1 = IPv4,
        Tunnel-Password:1 = "secretl2tp",
        Tunnel-Server-Endpoint:1 = "80.68.167.11",
        Tunnel-Assignment-Id:1 = "monfai_lns1",
        Tunnel-Type:2 += L2TP,
        Tunnel-Medium-Type:2 += IPv4,
        Tunnel-Password:2 += "secretl2tp",
        Tunnel-Server-Endpoint:2 += "80.68.167.12",
        Tunnel-Assignment-Id:2 += "monfai_lns2"

    adherent1 Cleartext-Password := "passwdadh1", Realm == "monfai@fdn.nerim"
        Framed-IP-Address = 88.55.66.1,
        Fall-Through = yes

    adherent2 Cleartext-Password := "passwdadh2", Realm == "monfai@fdn.nerim"
        Framed-IP-Address = 88.55.66.2,
        Fall-Through = yes

    DEFAULT Auth-Type == Accept
       Service-Type = Framed-User,
       Framed-Protocol = PPP,
       Framed-IP-Netmask = 255.255.255.255

    DEFAULT Auth-Type := Reject

# Configuration Serveur LNS

Exemple de configuration d'un serveur LNS avec l2tpns (fichier /etc/l2tpns/startup-config).

    set debug 2

    set log_file "/var/log/l2tpns"
    set pid_file "/var/run/l2tpns.pid"

    set hostname "mylns"
    set l2tp_secret "secretl2tp"

    # IP de l'interface par ou arrivera le tunnel l2tp
    set bind_address   80.68.167.11
    # Ce que l'on veut, le kernel y routera le trafic d'internet vers les clients 
    set iftun_address 10.10.10.10

    # IP de votre serveur DNS
    set primary_dns 80.67.167.42
    set secondary_dns 0.0.0.0

    set accounting_dir "/var/run/l2tpns/acct"
    set dump_speed no

    set cluster_address 239.192.13.42
    set cluster_interface "eth0"
    set cluster_mcast_ttl 1

    set cluster_hb_interval 20
    set cluster_hb_timeout 40
    set cluster_master_min_adv 1

    set cli_bind_address 127.0.0.1

    # IP de votre serveur radius 
    set primary_radius 80.67.167.11
    #set secondary_radius 80.67.167.12

    set primary_radius_port 1812
    #set secondary_radius_port 1812

    set radius_accounting yes
    set radius_secret "freeradiussecret"
    set radius_authtypes "chap, pap"

    # Set scheduling priority of process to SCHED_FIFO (utile si plusieurs core)
    set scheduler_fifo yes

    # Plugins
    load plugin "throttlectl"
    load plugin "autothrottle"
    load plugin "snoopctl"
    load plugin "autosnoop"
