FDN fournit à la fois des VPN authentifiés pour nos adhérents (dit standard), un VPN public (ex-openbar), et des VPN authentifiés pour des adhérents de partenaires. Cf. la [documentation VPN](https://git.fdn.fr/fdn-public/wiki/-/blob/master/vpn/README.md) sur le wiki public de FDN.

Dans tous les cas, on utilise actuellement openvpn. Trois exemplaires ,un pour servir en udp, l'autre pour servir en tcp, l'autre (rw) pour servir sur tous les ports.

# liste des VMs

  * vpn1 
  * vpn2
  * vpn3
  * vpn4
  * vpn6
  * vpn7
  * vpn8
  * vpn9
  * vpn10
  * vpn-open1

# Installation nouvelle VM

  * Bien penser à ajouter les nouveaux records vpn & vpn-rw A/AAAA DNS pour la nouvelle machine ajoutée.
  * Installer la VM avec 1GB de RAM, 2x vCPU, 5Go de disque, les modules puppet vpn et vpn-rw et ajouter dans /etc/network/interfaces.d/ l'interface RW en IPv4 & IPv6
  * Puppet gère l'installation des packets nécessaires mais il faut passer etckeeper
  * Cloner le repo puppet depuis palpatine (voir page dédiée sur puppet) sur son poste
  * Configurer le module puppet vpn (fichier hiera: vpn::ip et vpn::ip_rw)
  * Ajouter les sections pour l'interconnexion entre les bird (fichiers bird.conf.erb et bird6.conf.erb dans la repo puppet modules/vpn/templates) commit et git push.
  * Configurer l'accès radius sur les lns dans le module puppet radius, (fichiers `clients.conf` et `huntgroups` dans la repo puppet modules/radius/files), commit et git push.
  * Configurer le routage BGP directement sur les lns (à automatiser dans puppet): ajouter une entrée pour la nouvelle machine vpn dans section #Interco VPNs" /etc/bird.conf et /etc/bird6.conf et `conf soft` dans birdc & birdc6 pour prise en compte des changements.
  * Ajouter les informations (une nouvelle ligne x-... dans print-95.sh et le nom de la nouvelle VM dans la variable SRVLIST (ligne #27) et dans le if(ligne #111) de syncrrd.sh) au module stats de puppet, fichiers `print-95.sh` et `syncrrd.sh` dans la repo puppet /modules/stats/files)
  * ajouter une ligne push route dans le fichier
    modules/vpn/templates/serveur-tcp.conf.erb de puppet, ex:
    push "route 80.67.169.xxx 255.255.255.255 net_gateway".
  * Se connecter depuis la machine si.fdn.fr à la nouvelle machine pour
    accepter la clé host dans le known_hosts tant que on aura pas une version
    de openssh suffisament récente pour avoir l'option 'StrictHostKeyChecking
    accept-new'.
  * Tester depuis un client sur vpn et vpn-rw.
  * Si tout OK ajouter ajouter les IPs correspondantes aux domaines `vpn.fdn.fr` et `vpn-rw.fdn.fr` dans la repo des DNS
  * ajouter manuellement la nouvelle machine sur isengard dans
    /usr/local/nagios/etc/objects/{fdn_group.cfg,fdn.cfg}, relancer nagios:
    systemctl restart nagios.

# VPN authentifiés (VPN standard)

Dans ce cas, on utilise openvpn-auth-radius pour récupérer l'authentification et l'autorisation depuis le serveur RADIUS.

Modules puppet:

  * vpn
  * vpn-rw

## Détails IP pour VPN authentifiés

Les IPs sont actuellement piochées dans 80.67.179.0/24 et 2001:910:1300::/48. C'est dans le SI qu'est fait le choix des IPs, qui sont remontées via RADIUS, par exemple:

  * Framed-IP-Address 	= 	80.67.179.7
  * Framed-IP-Netmask 	= 	255.255.255.255
  * Framed-IPv6-Route 	= 	2001:910:1307::/48
  * Framed-IPv6-Address	= 	2001:910:1307:ffff::1

À noter qu'en IPv6 on attribue systématiquement un préfixe /48 entier, mais
on remonte aussi une IPv6 (2001:910:1307:ffff::1) à l'intérieur de ce préfixe, pour qu'openvpn la configure automatiquement du côté client du tunnel.

# VPN public (ex-openbar)

Dans ce cas, le script d'authentification c'est `/bin/true` :)

Modules: puppet:

  * vpn-open
  * vpn-rw

## Détails IP pour VPN public

Les IPs sont actuellement piochées dans 80.67.171.0/26 et 2001:910:802::/48. Ce sont les serveurs openvpn lui-même qui gèrent chacun leur pool, avec ce découpage:

  * vpn-open1 udp: 80.67.171.0/27 et 2001:910:802:1::/64
  * vpn-open1 tcp: 80.67.171.32/27 et 2001:910:802:2::/64

## Bande passante

On applique par contre une limitation de bande passante pour maîtriser le coût. Les [détails de la limitation de bande passante](https://git.fdn.fr/fdn/wiki/-/blob/master/pages/travaux/vpn_misc/bw.md) sont techniques, mais ça se résume au fichier de configuration `/etc/default/bw-limit` et au script `/etc/init.d/bw-limit restart`

# Renouvellement clés

Jusqu'en décembre 2017 on utilise le wildcard signé par CAcert. Depuis mi-novembre 2017, on ajoute un certificat auto-signé FDN dans les configs client. En décembre 2017, on bascule sur des certificats signés par ce certificat auto-signé.  Cela permet de mettre à jour les clés pour éviter d'utiliser une crypto trop faible: tantôt on change la clé du certificat non auto-signé, tantôt on change la clé du certificat auto-signé.

### Renouvellement certificat auto-signé

Le certificat auto-signé fait 4096 bits. Si on veut le renforcer il faut refaire le tout:

    certtool --bits 4096 --generate-privkey --outfile ca-fdn-20xx.key
    certtool --generate-self-signed --load-privkey ca-fdn-20xx.key --outfile ca-fdn-20xx.crt

Parmi les réponses à donner, ce qui est important est la durée de validité, donner par exemple 7000 jours (20 ans), que c'est une autorité, et que le certificat en signera d'autres. Le reste peut rester par défaut.

Il faut alors resigner tous les certificats avec la nouvelle autorité.

Il faut alors coller le contenu de ce certificat .crt en plus des autres dans les configs vpn chez les abonnés:
  * [Config VPN standard](https://git.fdn.fr/fdn-public/wiki/-/blob/master/vpn/openvpn/client/config-fdn-vpn.md)
  * [Certificat VPN standard](https://www.fdn.fr/assets/files/ca-vpn-fdn.crt)

  * [Config VPN public](https://git.fdn.fr/fdn-public/wiki/-/blob/master/vpn/openvpn/client/config-fdn-vpn-public.md)
  * [Certificat VPN public](https://www.fdn.fr/assets/files/ca-vpn-public-fdn.crt)

  * dans le SI dans `cgi/adh/print-vpncube.cgi`

quand on est raisonnablement sûr que les abonnés ont migré, on peut basculer sur le nouveau certificat auto-signé, et faire enlever l'ancien certificat chez les abonnés.

### Renouvellement certificat serveur

Ces certificats font 4096 bits. Si on veut les renforcer, il faut les refaire:

    certtool --bits 4096 --generate-privkey --outfile star.fdn_20xx.key
    certtool --generate-request --load-privkey star.fdn_20xx.key  --outfile star.fdn_20xx.csr

Parmi les réponses à donner, ce qui est important est que le common name est
`*.fdn.fr`, et que l'on va l'utiliser pour signer et chiffrer.  Le reste peut
rester par défaut.

Il faut transférer le .csr sur le serveur qui a le certificat auto-signé, et là

    certtool --generate-certificate --load-request /tmp/star.fdn_20xx.csr --load-ca-privkey ca-fdn-20xx.key --load-ca-certificate ca-fdn-20xx.crt --outfile /tmp/star.fdn_20xx.crt

Parmi les réponses à donner, ce qui est important est la durée de validité, donner par exemple 7000 jours (20 ans), que le common name est `*.fdn.fr`, et que l'on va l'utiliser pour signer et chiffrer.
Le reste peut rester par défaut.

On peut coller le contenu du certificat ca-fdn-20xx.crt à la suite dans le fichier .crt et le retransférer sur le serveur.

# Patchs

On a dû appliquer quelques patchs par-dessus les packages Debian:

## openvpn

Ces patchs sont appliqués dans la dernière version (2.4.0)

  * Add IPv6 pool environment variables (`pool_ipv6_env`): pour avoir
  `ifconfig_ipv6_pool_remote_ip` dans client-connect pour ajouter la route.
  * fix `/tmp/openvpn_cc` file leak (`openvpn_cc`): openvpn laissait traîner
  des fichier, qui finissent par remplir le disque.

## openvpn-auth-radius

  * `framed-ipv6-route.patch` et `framed-ipv6-address.patch`: Support de l'ajout
  des routes.
  * `disable-acct`: désactivation de l'envoi de l'accounting, dont on ne se
  sert pas, et qui bloque le trafic pendant l'envoi.

# routage BGP

Pour que les routeurs sachent à quel serveur VPN les clients openvpn sont
connectés et donc auquel envoyer les paquets, on expose les routes en iBGP.

Chaque serveur VPN a donc un bird et un bird6 installés, avec une session iBGP
vers les lns01 et lns02.

# vpn-rw

Pour que le client openvpn puisse se connecter depuis des réseaux hostiles, pour chaque serveur VPN on a une IP dont *tous* les ports sont redirigés vers openvpn.

Le module puppet vpn-rw met en place les règles iptables pour cela. Avant de le déployer il faut le configurer pour définir les IPs à utiliser.

# fail2ban

Pour éviter de remplir les disques durs avec les logs d'échecs d'intrus, on utilise fail2ban, automatiquement configuré par les modules puppet vpn et vpn-open.

# Performances CPU

Le chiffrement est une grosse part du coût CPU des VPNs, mais aussi le passage de paquets entre openvpn et le noyau.

## parallélisme

Malheureusement openvpn n'est pas parallèle, mais on a deux serveurs (un UDP, l'autre TCP), donc on met deux processeurs sur les VMs pour en profiter.

# Offuscation

## Generalités

Cette méthode permet d'utiliser l'infrastructure openvpn existante et d'encapsuler les flux openvpn dans un tunnel TLS.
Cela permet de faire circuler les données dans un flux https et permet donc de passer la plupart des filtrages à l'heure actuelle.

Cette architecture a 4 composants supplémentaires qui viennent s'installer sur les VM:

 * apache  : fonction de redirection des requetes vers www.fdn.fr
 * stunnel4: fonction d'encapsulation du flux openvpn
 * sslh    : multiplexage de flux permettant de rediriger le trafic openvpn vers le deamon openvpn et le trafic web vers Apache (le tout sur le même port!)
 * acme    : gestion des certificats let's encrypt pour stunnel

## Installation des composants

`apt-get install apache2 stunnel4 sslh`

Ajout du module acme dans puppet pour les VM concernées vpn[1,2,3].pp

## Configuration des composants

### Apache2 & acme

Suivre la procédure [let's encrypt](./outils_internes/letsencrypt.md)

Modifier le site default (/etc/apache2/site-available/default) par: 

    <VirtualHost *:80>
            ServerName vpn1.fdn.fr
            DocumentRoot "/var/www"
            LogLevel warn
            Include /etc/apache2/include/acme-challenge.conf
            Include /etc/apache2/include/redirect-to-https.conf
    </VirtualHost>

Modifier le redirect (/etc/apache2/include/redirect-to-https.conf) par:

    <ifmodule mod_rewrite.c>
            RewriteEngine On
            RewriteCond %{REQUEST_URI} !^/\.well\-known/acme\-challenge/
            RewriteRule (.*) https://www.fdn.fr [R=301,L]
    </ifmodule>        

Ajouter stunnel dans les reload service (/etc/acme/vpn1.fdn.fr.conf) :

`RELOAD_SERVICE=stunnel4`

Et ajout de stunnel dans /etc/sudoers pour restart auto depuis compte acme:

`acme ALL=(root) NOPASSWD: /etc/init.d/stunnel4 restart`

### sslh

Modification des options par défaut (/etc/default/sslh) :

    RUN=yes
    DAEMON_OPTS="--user sslh --listen 127.0.0.1:1111 --openvpn 127.0.0.1:1194 --ssl 127.0.0.1:80 --http 127.0.0.1:80 --pidfile /var/run/sslh/sslh.pid"

### stunnel4

Ajout de la configuration (/etc/stunnel/openvpn_inside_tls.conf)

    debug = info
    output = /var/log/stunnel.log
    pid        = /stunnel.pid
    
    [sslh]
     connect = 127.0.0.1:1111
     accept = 80.67.169.45:443 
     cert = /etc/apache2/ssl/vpn1.fdn.fr/vpn1.fdn.fr.pem 
     CApath = @sysconfdir/ssl/certs
    
    [sslh_v6]
     connect = ::1:1111
     accept = 2001:910:800::45:443
     cert = /etc/apache2/ssl/vpn1.fdn.fr/vpn1.fdn.fr.pem 
     CApath = @sysconfdir/ssl/certs


Activer le service (/etc/default/stunnel4)

`ENABLED=1`

Démarer les services:

    systemd : systemctl start stunnel4
    systemd : systemctl start sslh
    initd   : /etc/init.d/stunnel4 start
    initd   : /etc/init.d/sslh start

Start @ Boot:    

    systemd : systemctl enable stunnel4
    systemd : systemctl enable sslh
    initd   : update-rc.d stunnel4 defaults 
    initd   : update-rc.d sslh defaults 
