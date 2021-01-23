[[!meta title="Remote Monitoring"]]

# Généralités

Nous disposons de deux nagios chez FDN. Un premier hébergé en interne (sur leia, voir [page dédiée](/outils/supervision/intra_monitoring)) et un second gentiment hébergé à l'extérieur de l'infra de FDN sur isengard, une VM hébergée chez LDN (merci LDN, merci sebian).

Cette VM fait tourner un [Nagios](https://www.nagios.org/) couplé à un [Cachet](https://cachethq.io/) 
afin de présenter une mire de l'état de nos services depuis l'extérieur.

Cachet est accessible sur [https://isengard.fdn.fr/](https://isengard.fdn.fr/).
Nagios pour les checks remote est accessible sur [https://isengard.fdn.fr/nagios](https://isengard.fdn.fr/nagios).

# Sensors

Pour commencer nous choisissons de monitorer :

* ICMP
* Ports TCP/UDP pour vérifier l'ouverture des sockets (TCP 25, TCP 80, TCP 443...)
* Applications (HTTP 200 OK, Résolutions DNS, Bannières SSH, Codes SMTP valides, Validation de certificats X.509...)
* Montée de plusieurs VPN (vpn-open1.fdn.fr, open.fdn.fr, vpn.fdn.fr, vpn1.fdn.fr, vpn2.fdn.fr, vpn3.fdn.fr, vpn-rw.fdn.fr, vpn1-rw.fdn.fr, vpn2-rw.fdn.fr) à la fois en TCP & UDP
* Montée de liaisons PPPoE sur nos LNS 

# Préliminaires

* machine sous debian jessie
* fournir les clefs publiques du groupe noyau pour le proxy serial (en cas d'accès console sur la machine)
* module puppet afin de passer les modules de bases de FDN

# Connexions

* ssh root@fdn.vps.ldn-fai.net (recovery)
* ssh serialproxy@services.ldn-fai.net (recovery serial)
* ssh isengard.fdn.fr

# Installation de Nagios 4 (seule la version 3 est disponible dans les dépôts)

## Installation des dépendances

    apt-get install postfix build-essential libgd2-xpm-dev openssl libssl-dev xinetd apache2-utils apache2 unzip php5

## Utilsateur / droits

    useradd nagios
    groupadd nagcmd
    usermod -a -G nagcmd nagios

## Source & compilation

    cd /opt/
    wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.3.1.tar.gz
    tar xzvf nagios-4.3.1.tar.gz
    cd nagios-4.3.1
    ./configure --with-nagios-group=nagios --with-command-group=nagcmd --with-httpd-conf=/etc/apache2/conf-available
    make all 
    make install
    make install-commandmode
    make install-init
    make install-config
    /usr/bin/install -c -m 644 sample-config/httpd.conf /etc/apache2/sites-available/nagios.conf
    usermod -G nagcmd www-data
    ln -s /etc/init.d/nagios /etc/rcS.d/S99nagios

## Installation des plugins

    wget https://nagios-plugins.org/download/nagios-plugins-2.1.4.tar.gz
    tar xvf nagios-plugins-2.1.4
    cd nagios-plugins-2.1.4
    ./configure --with-nagios-user=nagios --with-nagios-group=nagios
    make
    make install

## Configuration de Postfix pour envoyer des mails mais ne pas devenir un relay SPAM 

    smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated 
    defer_unauth_destination
    myhostname = isengard.fdn.fr
    alias_maps = hash:/etc/aliases
    alias_database = hash:/etc/aliases
    myorigin = /etc/mailname
    mydestination = isengard.fdn.fr, localhost.fdn.fr, localhost
    relayhost =
    mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128
    mailbox_command = procmail -a "$EXTENSION"
    mailbox_size_limit = 0
    recipient_delimiter = +
    inet_interfaces = localhost
    default_transport = smtp
    relay_transport = error

## Ajout d'une email dans contacts

    define contact{
        contact_name	nagiosadmin
        use		generic-contact
        alias		Nagios Admin
        email		adminsys@fdn.fr
        }

## Mettre en route les notifications sur notre template de service

    notifications_enabled           1

## Quelles alertes recevoir (CRITICAL & RECOVERY)

    service_notification_options    c,r

## Configuration d'Apache

    a2enmod rewrite
    a2enmod cgi
    htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin
    a2ensite nagios

On redémarre (c'est bien mieux!)

    service nagios start
    service apache2 reload

## Configuration des machines FDN pour le monitoring

Copier les fichiers fdn.cfg,fdn_group.cfg,fdn_services.cfg dans /usr/local/nagios/etc/objects.

Puis, ajouter à /usr/local/nagios/etc/nagios.cfg

    cfg_file=/usr/local/nagios/etc/objects/fdn.cfg
    cfg_file=/usr/local/nagios/etc/objects/fdn_group.cfg
    cfg_file=/usr/local/nagios/etc/objects/fdn_services.cfg

Ajouter à /usr/local/nagios/etc/objects/commands.cfg

    define command {
        command_name    cachet_notify
        command_line    /usr/local/nagios/plugins/nagios-eventhandler-cachet/cachet_notify "$HOSTNAME$" "$SERVICEDESC$" "$SERVICESTATE$" "$SERVICESTATETYPE$" "$SERVICEOUTPUT$" -m=true
    }

Puis on reload

    service nagios reload

Pour références, les fichiers de configuration utilisés sont ici:

* [[nagios/commands.cfg]]

* [[nagios/contacts.cfg]]

* [[nagios/templates.cfg]]

* [[nagios/fdn.cfg]]

* [[nagios/fdn_group.cfg]]

* [[nagios/fdn_services.cfg]]

# Installation de Cachet

## Dépendances

* PHP 5.5.9 (ok)

* extention gd de php

<!-- code --> 

    apt-get install php5-gd

* Composer

<!-- code -->

    php -r "readfile('https://getcomposer.org/installer');" > composer-setup.php

    php -r "if (hash_file('SHA384', 'composer-setup.php') === '7228c001f88bee97506740ef0888240bd8a760b046ee16db8f4095c0d8d525f2367663f22a46b48d072c816e7fe19959') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"

    php composer-setup.php

    php -r "unlink('composer-setup.php');"

Pour que composer soit disponible globalement sur le système:

    mv composer.phar /usr/local/bin/composer    

* Installation de APCU pour le cache.

<!-- code -->

    apt-get install php5-apcu php5-mysql

* Installation de Base de données My-SQL

<!-- code -->

    apt-get install mysql-server

* Git (ok)

## Création et Configuration de la base de données

    mysql -u -p
    mysql> CREATE DATABASE cachet;
    mysql> GRANT ALL PRIVILEGES ON cachet.* To 'cachetdb'@'localhost' IDENTIFIED BY '********';

## Pour référence: supprimer toutes les entrées

    mysql -u -p
    mysql> use cachet;
    mysql> truncate incidents;

## Copie des sources de Cachet

    cd /var/www
    git clone https://github.com/cachethq/Cachet.git
    cd Cachet
    git tag -l
    git checkout v2.2.1
    cd /var/www/Cachet
    cp /var/www/Cachet/.env.example /var/www/Cachet/.env

## Configuration de Cachet 

    /var/www/Cachet/.env

    APP_ENV=production
    APP_DEBUG=false
    APP_URL=http://isengard.fdn.fr
    APP_KEY=**************

    DB_DRIVER=mysql
    DB_HOST=localhost
    DB_DATABASE=cachet
    DB_USERNAME=cachetdb
    DB_PASSWORD=************
    DB_PORT=null
    DB_PREFIX=null

    CACHE_DRIVER=file
    SESSION_DRIVER=file
    QUEUE_DRIVER=sync
    CACHET_EMOJI=false

    MAIL_DRIVER=smtp
    MAIL_HOST=mailtrap.io
    MAIL_PORT=2525
    MAIL_USERNAME=null
    MAIL_PASSWORD=null
    MAIL_ADDRESS=null
    MAIL_NAME=null
    MAIL_ENCRYPTION=tls

    REDIS_HOST=null
    REDIS_DATABASE=null
    REDIS_PORT=null

    GITHUB_TOKEN=null

## Installation de composer:

    composer install --no-dev -o
    php artisan key:generate
    a2enmod rewrite
    service apache2 restart
    chown -R www-data:www-data /var/www/Cachet
    chmod -R guo+w /var/www/Cachet/storage/

## Intégration avec apache

    /etc/apache2/sites-enabled/000-default.conf

    <VirtualHost *:80>
        ServerName cachet.dev # Or whatever you want to use
        ServerAlias cachet.dev # Make this the same as ServerName
        DocumentRoot "/var/www/Cachet/public"
        <Directory "/var/www/Cachet/public">
            Require all granted # Used by Apache 2.4
            Options Indexes FollowSymLinks
            AllowOverride All
            Order allow,deny
            Allow from all
        </Directory>
    </VirtualHost>
    
## Mise à jour de Cachet

Mettre cachet en mode maintenance

    php artisan down

Récupération de la dernière version

    git fetch origin
    git tag -l
    git checkout LATEST_TAG

Mise à jour des dépendances

    composer install --no-dev -o --no-scripts

Mise à jour de Cachet

    php artisan app:update

Redémarrage de Cachet

    php artisan up

## Eviter les liens externes vers Google et Cloudflare

La dernière version de Cachet permet de désactiver les dépendances externes (Google Fonts, Trackers..) depuis 
l'interface d'administration, il suffit de décocher:

    Enable Third Party Dependencies (Google Fonts, Trackers, etc...) 

Pour Cloudflare:
    
    wget 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.8.0/codemirror.min.js' -O /var/www/Cachet/public/codemirror.min.js
    wget 'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.8.0/codemirror.js' -O /var/www/Cachet/public/codemirror.js
    wget https://cdnjs.cloudflare.com/ajax/libs/zxcvbn/2.0.2/zxcvbn.min.js -O /var/www/Cachet/public/zxcvbn.min.js
    sed -i 's|https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.8.0/codemirror.css|codemirror.css|g' /var/www/Cachet/resources/views/dashboard/templates/*.php
    sed -i 's|https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.8.0/mode/twig/twig.min.js|twig.min.js|g'  /var/www/Cachet/resources/views/dashboard/templates/*.php
    sed -i 's|https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.8.0/codemirror.min.js|codemirror.min.js|g' /var/www/Cachet/resources/views/dashboard/templates/*.php
    sed -i 's|https://cdnjs.cloudflare.com/ajax/libs/zxcvbn/2.0.2/zxcvbn.min.js|zxcvbn.min.js|g' Cachet/public/build/dist/js/*.js
    sed -i 's|https://cdnjs.cloudflare.com/ajax/libs/zxcvbn/2.0.2/zxcvbn.min.js|zxcvbn.min.js|g' Cachet/resources/assets/js/*.js

Ne pas oublier de refaire l'opération après une mise à jour de Cachet.

## Cachet & Nagios together

L'objectif est d'alimenter les Incidents Cachet via les alertes Nagios pour permettre un affichage user-friendly pour les utilisateurs, pour une 
vision bien plus claire de l'historique des incidents envoyés par Nagios et pour la suite d'utiliser les alertes mail de 
Cachet.

Utilisation du plugin [nagios-eventhandler-cachet](https://github.com/mpellegrin/nagios-eventhandler-cachet)

Créer un utilisateur dans [Cachet dashboard](http://isengard.fdn.fr/dashboard), se connecter avec l'utilisateur et récupérer la clef API

Cloner le plugin et copier cachet_notify dans /usr/local/nagios/plugins

    git clone https://github.com/mpellegrin/nagios-eventhandler-cachet.git

Le script est cassé, plusieurs typos et erreurs voici le script modifié pour réference: [[cachet/cachet_notify]]

Modifier l'url et l'API dans cachet_notify

    $cachet_url = 'https://isengard.fdn.fr/api/v1/';
    $api_key = '*****************';

Pour tester le script

Simuler un incident

    ./cachet_notify 'neviani.fr' 'disponibilite' FAILED HARD 'test service casse' -m=true

Simuler une reprise à la normale

    ./cachet_notify 'neviani.fr' 'disponibilite' OK HARD 'test service casse' -m=true


Ajouter une fonction auto-refresh pour la page de Status des services FDN afin de mettre à jout automatiquement la page en cas d'incident.

Ajouter

     <meta http-equiv="refresh" content="120">

dans [Custom Footer HTML](http://isengard.fdn.fr/dashboard/settings/customization)

# Tests effectués

* [PASS] Test de la chaine complète (Nagios->EventHandler->Cachet) en cas de problème Vert->Rouge
* [PASS] Test de la chaine complète (Nagios->EventHandler->Cachet) retour à la normale Rouge->Vert

* ICMPv4 & ICMPv6
  - [PASS] test icmp_ipv4: OK -> KO PARTIAL  
  - [PASS] test icmp_ipv4: KO PARTIAL -> KO CRITICAL
  - [PASS] test icmp_ipv4: KO PARTIAL -> OK
  - [PASS] test icmp_ipv4: KO CRITICAL -> OK
  - [PASS] test icmp_ipv6: OK -> KO PARTIAL
  - [PASS] test icmp_ipv6: KO PARTIAL -> KO CRITICAL
  - [PASS] test icmp_ipv6: KO PARTIAL -> OK
  - [PASS] test icmp_ipv6: KO CRITICAL -> OK
  - **[FAIL] test icmp_ipv6: open.fdn.fr,vpn1-rw.fdn.fr et vpn2-rw.fdn.fr (MAJ kernel pour support DNAT IPv6)**

* TCP Sockets ICMPv4 & ICMPv6
  - [PASS] test web_ipv4: TCP 80 
  - [PASS] test web_ipv6: TCP 80 
  - [PASS] test web_ipv4: TCP 443  
  - [PASS] test web_ipv6: TCP 443 
  - [PASS] test jabber_ipv4: TCP 5222
  - [PASS] test jabber_ipv6: TCP 5222
  - [PASS] test jabber_ipv4: TCP 5223
  - **[FAIL] test jabber_ipv6: TCP 5223 (à discuter)**      
  - [PASS] test mail_ipv4: TCP 25
  - [PASS] test mail_ipv6: TCP 25
  - [PASS] test mail_ipv4: TCP 587 
  - [PASS] test mail_ipv6: TCP 587 

* Test DNS par nos résolveurs
  - [PASS] test dns_ipv4: www.gnu.org!208.118.235.148 (IPv4 depuis DNSv4)
  - [PASS] test dns_ipv6: www.gnu.org!208.118.235.148 (IPv4 depuis DNSv6)
  - **[FAIL] test dns_ipv6: (IPv6 depuis DNSv6) [attente MAJ 
plugin](https://github.com/nagios-plugins/nagios-plugins/issues/154)**

* Test SMTP
  - [PASS] test st25_ipv4: 220 Service ready
  - [PASS] test st25_ipv6: 220 Service ready
  - [PASS] test st587_ipv4: 220 Service ready
  - [PASS] test st587_ipv6: 220 Service ready

* Test SSH
  - [PASS] test ssh_ipv4: r4p17.fdn.fr protocol 2.0 
  - [PASS] test ssh_ipv6: c3px.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: lns01.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: lns01.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: lns02.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: lns02.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: 80.67.169.12 protocol 2.0
  - [PASS] test ssh_ipv6: 80.67.169.12 protocol 2.0
  - [PASS] test ssh_ipv4: 80.67.169.40 protocol 2.0
  - [PASS] test ssh_ipv6: 80.67.169.40 protocol 2.0
  - [PASS] test ssh_ipv4: 2001:910:800::12 protocol 2.0
  - [PASS] test ssh_ipv6: 2001:910:800::40 protocol 2.0
  - [PASS] test ssh_ipv4: fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: adminsys.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: adminsys.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: lists.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: lists.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: webmail.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: webmail.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: git.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: git.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: mail.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: mail.fdn.fr protocol 2.0
  - **[FAIL] test ssh_ipv4: smtp.fdn.fr protocol 2.0**
  - **[FAIL] test ssh_ipv6: smtp.fdn.fr protocol 2.0**
  - [PASS] test ssh_ipv4: jabber.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: jabber.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv4: rsf.fdn.fr protocol 2.0
  - [PASS] test ssh_ipv6: rsf.fdn.fr protocol 2.0

* Test HTTPS
  - [PASS] test web_ipv4: fdn.fr 301 -> 200 OK
  - [PASS] test web_ipv6: fdn.fr 301 -> 200 OK
  - [PASS] test web_ipv4: adminsys.fdn.fr 401 Unauthorized
  - [PASS] test web_ipv6: adminsys.fdn.fr 401 Unauthorized
  - [PASS] test web_ipv4: lists.fdn.fr 302 Found -> 200 OK
  - [PASS] test web_ipv6: lists.fdn.fr 302 Found -> 200 OK
  - **[FAIL] test web_ipv4: webmail.fdn.fr certifcat lists.fdn.fr (à discuter)**
  - **[FAIL] test web_ipv6: webmail.fdn.fr certificat lists.fdn.fr (à discuter)**
  - [PASS] test web_ipv4: git.fdn.fr 302 Found -> 200 OK
  - [PASS] test web_ipv6: git.fdn.fr 302 Found -> 200 OK

* Test validité certificats X.509
**  - [FAIL] test certificats: fdn.fr KO Certificate 'blog-devel.fdn.fr' expired on 2016-06-18 (à discuter)**
  - [PASS] test certificats: adminsys.fdn.fr OK < 30 days  
  - [PASS] test certificats: lists.fdn.fr OK < 30 days
  - [PASS] test certificats: webmail.fdn.fr OK < 30 days
  - [PASS] test certificats: git.fdn.fr OK < 30 days

* Test montée de tunnels OpenVPN
  - [PASS] test OpenVPN vpn-open1.fdn.fr TCP 1194
  - [PASS] test OpenVPN vpn-open1.fdn.fr UDP 1194
  - [PASS] test OpenVPN open.fdn.fr TCP 443
  - [PASS] test OpenVPN open.fdn.fr UDP 53
  - [PASS] test OpenVPN vpn-rw.fdn.fr TCP 22
  - [PASS] test OpenVPN vpn-rw.fdn.fr UDP 53
  - [PASS] test OpenVPN vpn1-rw.fdn.fr TCP 22
  - [PASS] test OpenVPN vpn1-rw.fdn.fr UDP 53
  - [PASS] test OpenVPN vpn2-rw.fdn.fr TCP 22
  - [PASS] test OpenVPN vpn2-rw.fdn.fr UDP 53
  - [PASS] test OpenVPN vpn.fdn.fr TCP 1194
  - [PASS] test OpenVPN vpn.fdn.fr UDP 1194
  - [PASS] test OpenVPN vpn1.fdn.fr TCP 1194
  - [PASS] test OpenVPN vpn1.fdn.fr UDP 1194
  - [PASS] test OpenVPN vpn2.fdn.fr TCP 1194
  - [PASS] test OpenVPN vpn2.fdn.fr UDP 1194
  - [PASS] test OpenVPN vpn3.fdn.fr TCP 1194
  - [PASS] test OpenVPN vpn3.fdn.fr UDP 1194

# Changelog
## Versions précédentes
### Version 1.0

* ICMPv4
* ICMPv6

### Version 1.1 

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6

### Version 1.2

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs

### Version 1.3

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs
* Test SMTP

### Version 1.4

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs
* Test SMTP
* Test SSH

### Version 1.5

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs
* Test SMTP
* Test SSH
* Test HTTPS

### Version 1.6

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs
* Test SMTP
* Test SSH
* Test HTTPS
* Test validité certificats X.509

### Version 1.7

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs
* Test SMTP
* Test SSH
* Test HTTPS
* Test validité certificats X.509
* Alertes par mail
* Let's encrypt

## Version en service
### Version 1.8

* ICMPv4
* ICMPv6
* TCP Sockets IPv4 & IPv6
* Test DNS par nos résolveurs
* Test SMTP
* Test SSH
* Test HTTPS
* Test validité certificats X.509
* Alertes par mail
* Let's encrypt
* Test de montée de tunnels OpenVPN

## Roadmap / Investigation

* Test pppoe: écrire un plugin (ça n'a pas l'air d'exister) et demander credential et étudier faisabilité car LNS écoutent sur des interfaces particulières
* mettre un nom plus parlant pour nos adhérents, statut.fdn.fr?
