# Créer un « bac à sable » de l'architecture de routage de FDN

Cette page décrit comment mettre en place un « bac à sable » pour jouer avec les outils qui sont utilisés dans l'infrastructure de FDN. À faire de préférence dans une VM, pour partir d'une base « propre » et ne pas tout casser votre système. C'est assez centré sur les LNS. Et pour ceux qui veulent en mettre deux en load-balancing, il faut deux VMs.

Au niveau des valeurs utilisées, je vais garder celles que j'ai en dur, à vous d'adapter :

  * 192.168.2.238/24 pour l'interface locale de la VM
  * 10.0.3.0/24 pour l'interface tun

## Installer une VM Debian

Squeeze par exemple, c'est très bien.

## Configurer le réseau

Vous allez sûrement vouloir interagir avec votre VM par le réseau, et le mieux c'est de la bridger.

Il faut donc créer deux scripts pour qemu, qui vont mettre en place ou éteindre correctement le bridge :

  * netup.sh :
    <code>
    #!/bin/sh
    
    # Create a bridged connexion for TAP connection $1
    
    bridge=br0
    # setup bridge
    echo "Setting up bridge ..."
    brctl addbr $bridge
    brctl addif $bridge eth0
    ip link set $bridge up
    # bring the tap interface up
    echo "Setting up $1 ..."
    ip link set $1 up
    ip address flush dev $1
    ip address add 0.0.0.0 dev $1
    
    # add to bridge
    echo "Bridging $1 to $bridge ..."
    brctl addif $bridge $1
    </code>


  * netdown.sh 
    <code>
    #!/bin/sh
    
    # Delete a bridged connexion for TAP connection $1
    
    bridge=br0
    
    # bring the tap interface down
    echo "Bringing down $1 ..."
    ip link set $1 down
    
    # remove from bridge
    echo "Removing $1 from $bridge ..."
    brctl delif $bridge $1
    
    # setup bridge
    echo "Bringing down bridge ..."
    ip link set $bridge down
    brctl delif $bridge eth0
    brctl delbr $bridge
    </code>


Ce code a été récupéré je ne sais où et adapté par moi. Par contre, du coup, ça oblige à lancer la VM en tant que root…
On devra ajouter à la ligne de commande kvm/qemu :

    <code>-net nic -net tap,script=./netup.sh,downscript=./netdown.sh</code>


## Installer Radius

Pour l'authentification, on utilise freeradius. On va créer quelques utilisateurs bidons, avec l'adresse IP qui leur est associée.

    <code>apt-get install freeradius</code>


On ajoute un client pour l2tpns dans /etc/freeradius/clients.conf :

    <code>
    client l2tpns {
            ipaddr = 192.168.2.238
            secret = testing123
            nastype     = other
            require_message_authenticator = no
    }
    </code>


Il y a bien une conf par défaut quand on utilise uniquement le loopback (à priori faisable dans notre cas), mais ça n'avait pas marché pour je ne suis plus quelle raison. Le « secret » sera aussi reporté dans la configuration l2tpns.

On ajoute des clients de test dans /etc/freeradius/users :

    <code>
    test1 Cleartext-Password := "test1"
            Framed-IP-Address = 10.0.3.101,
            Framed-IP-Netmask = 255.255.255.255
    test2 Cleartext-Password := "test2"
            Framed-IP-Address = 10.0.3.102,
            Framed-IP-Netmask = 255.255.255.255
    </code>


Et ça doit marcher à coup de ''radtest test1 test1 192.168.2.238 0 testing123''.

## Installer BIRD

On utilise actuellement quagga, mais j'ai voulu tester BIRD.

    <code>apt-get install bird</code>


On ajoute la conf suivante :

    <code>
    router id 192.168.2.238;
    
    protocol kernel {
            persist;
            scan time 20;
            export all; # XXX à customiser
            learn;
            import filter {
                    if net ~ 10.0.3.0/24 then
                            if net.len = 32 then
                                    accept;
                    reject;
            };
    }
    </code>


Le « protocol kernel » c'est le protocole déjà installé par défaut, sauf que là on va lui demander d'apprendre les routes insérées par l2tpns.

## Installer l2tpns

Alors, le but ici c'était de tester le l2tpns modifié par mes soins, trouvable ici : http://dolka.fr/code/l2tpns.git

On installe ce qu'il faut pour le compiler :

    <code>
    apt-get install git-core
    apt-get build-depends l2tpns
    </code>


On le récupère :

    <code>
    git clone http://dolka.fr/code/l2tpns.git
    </code>


Pour que ça marche avec une version actuelle de BIRD, il faut aussi changer le protocole pour les routes ajoutées :

    <code>
    diff --git a/l2tpns.c b/l2tpns.c
    index 581198d..57a8614 100644
    --- a/l2tpns.c
    +++ b/l2tpns.c
    @@ -452,7 +452,7 @@ static void routeset(sessionidt s, in_addr_t ip, int prefixlen, in_addr_t gw, in
            req.rt.rtm_family = AF_INET;
            req.rt.rtm_dst_len = prefixlen;
            req.rt.rtm_table = RT_TABLE_MAIN;
    -       req.rt.rtm_protocol = RTPROT_BOOT; // XXX
    +       req.rt.rtm_protocol = 42;
            req.rt.rtm_scope = RT_SCOPE_LINK;
            req.rt.rtm_type = RTN_UNICAST;
     
    @@ -527,7 +527,7 @@ void route6set(sessionidt s, struct in6_addr ip, int prefixlen, int add)
            req.rt.rtm_family = AF_INET6;
            req.rt.rtm_dst_len = prefixlen;
            req.rt.rtm_table = RT_TABLE_MAIN;
    -       req.rt.rtm_protocol = RTPROT_BOOT; // XXX
    +       req.rt.rtm_protocol = 42;
            req.rt.rtm_scope = RT_SCOPE_LINK;
            req.rt.rtm_type = RTN_UNICAST;
    </code>


(ça se copie/colle bien dans un ''git apply'')

Enusuite on :

    <code>dpkg-buildpackage -us -uc</code>


Et on l'installe.

La conf utilisée :

    <code>
    set debug 3
    
    set log_file "/var/log/l2tpns"
    set pid_file "/var/run/l2tpns.pid"
    
    set hostname "lns1"
    set l2tp_secret "foo"
    
    set primary_dns 80.67.169.12
    set secondary_dns 80.67.169.40
    
    set primary_radius 192.168.2.238
    set secondary_radius 192.168.2.238
    set radius_accounting no
    set radius_secret "testing123"
    set radius_authtypes "pap,chap"
    set primary_radius_port 1812
    set secondary_radius_port 1812
    
    set bind_address 10.0.3.1
    set cli_bind_address 127.0.0.1
    
    set accounting_dir "/var/run/l2tpns/acct"
    set dump_speed no
    
    #load plugin "garden"
    load plugin "throttlectl"
    load plugin "autothrottle"
    load plugin "snoopctl"
    load plugin "autosnoop"
    
    set cluster_interface eth0
    set cluster_address 239.192.13.42
    set cluster_mcast_ttl 1
    set cluster_hb_interval 5
    set cluster_hb_timeout 150
    set cluster_master_min_adv 1
    
    set ipv6_prefix 2001:db9:8ff:ffff::0
    </code>


Et aussi, supprimer le contenu de /etc/l2tpns/ip_pool, pour l'instant.

## La connexion d'un client

Depuis une autre machine, on peut maintenant essayer de se connecter. Attention, il faut que cette machine ait une route vers le tun, donc en faisant par exemple :

    <code>ip route add 10.0.3.0/24 dev br0</code>


sur votre hôte.

Comme client L2TP, j'utilise openl2tpd. Il n'est pas encore dans debian, je suis allé chercher les sources ici : http://openl2tp.org/downloads
Compiler, installer… Et puis suivre la doc pour un test : http://www.openl2tp.org/doc/install

Pour nous, taper ce qui suit dans une invite l2tpconfig :
    <code>
    tunnel create tunnel_name=test dest_ipaddr=10.0.3.1
    ppp profile create profile_name=test auth_chap=yes
    session create tunnel_name=test ppp_profile_name=test session_name=test user_name=test1 user_password=test1
    </code>


## TODO

Ajouter la conf en load-balancing.
Faire la conf en v6 aussi.
