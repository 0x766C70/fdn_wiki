# Généralités

Nous disposons de deux nagios chez FDN.
Un premier non maintenu (voir le ticket [#5 de monitoring2.0](https://git.fdn.fr/adminsys/monitoring2.0/-/issues/5)) hébergé en interne (sur cecinestpasleia, voir [page dédiée](./outils_internes/supervision/intra_monitoring.md)) et un second gentiment hébergé à l'extérieur de l'infra de FDN sur skytop, une VM hébergée chez Grenode.

Cette VM fait tourner un [Nagios](https://www.nagios.org/) couplé à un [Cachet](https://cachethq.io/)
afin de présenter une mire de l'état de nos services depuis l'extérieur.

Cachet est accessible sur [https://skytop.fdn.fr/](https://skytop.fdn.fr/).
Nagios pour les checks remote est accessible sur [https://skytop.fdn.fr/nagios4](https://skytop.fdn.fr/nagios4).

# Sensors

Pour commencer nous choisissons de monitorer :

* ICMP
* Ports TCP/UDP pour vérifier l'ouverture des sockets (TCP 25, TCP 80, TCP 443...)
* Applications (HTTP 200 OK, Résolutions DNS, Bannières SSH, Codes SMTP valides, Validation de certificats X.509...)
* Montée de plusieurs VPN (vpn-open1.fdn.fr, open.fdn.fr, vpn.fdn.fr, vpn1.fdn.fr, vpn2.fdn.fr, vpn3.fdn.fr, vpn-rw.fdn.fr, vpn1-rw.fdn.fr, vpn2-rw.fdn.fr) à la fois en TCP & UDP
* Montée de liaisons PPPoE sur nos LNS 

# Préliminaires

* machine sous debian Bullseye
* module puppet afin de passer les modules de bases de FDN

# Connexions

* ssh skytop.fdn.fr

# Installation de Nagios 4

## Installation des dépendances

    apt install apache2 nagios4-common nagios4-cgi nagios-nrpe-plugin nagios-plugins nagios-plugins-basic nagios-plugins-contrib nagios-plugins-standard php-gd mariadb-server php-curl php-apcu curl php-simplexml php-mbstring php-mysql

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

    /etc/apache2/sites-available/cachet.conf

    <VirtualHost *:80>
        DocumentRoot "/var/www/"
        ServerName skytop.fdn.fr
        ServerAlias	status.fdn.fr statut.fdn.fr isengard.fdn.fr isengard.fdn.org status.fdn.org statut.fdn.org skytop.fdn.org
        LogLevel warn
        Include /etc/apache2/include/acme-challenge.conf
        Include /etc/apache2/include/redirect-to-https.conf

    <Directory "/var/www/Cachet/public">
        Require all granted 
        Options Indexes FollowSymLinks
        AllowOverride All
    </Directory>

    <Directory "/var/www/vpn/">
    	Require ip 80.67.0.0/16
    	Require ip 2001:910::/32
        DirectoryIndex index.html
    </Directory>

    <Directory "/.well-known/acme-challenge/">
        Require all granted
    </Directory>
    </VirtualHost>

    <VirtualHost *:443>
      ServerName skytop.fdn.fr
      ServerAlias	status.fdn.fr statut.fdn.fr isengard.fdn.fr isengard.fdn.org status.fdn.org statut.fdn.org skytop.fdn.org
      DocumentRoot "/var/www/Cachet/public"
      SSLEngine on
      SSLCertificateFile      /etc/apache2/ssl/isengard.fdn.fr/isengard.fdn.fr.chained
      SSLCertificateChainFile /etc/apache2/ssl/isengard.fdn.fr/isengard.fdn.fr.chained
      SSLCertificateKeyFile   /etc/apache2/ssl/isengard.fdn.fr/isengard.fdn.fr.key

    <Directory "/var/www/Cachet/public">
        Require all granted 
        Options Indexes FollowSymLinks
        AllowOverride All
    </Directory>
    </VirtualHost>

    sudo a2enmod rewrite auth_digest authz_groupfile ssl

On redémarre (c'est bien mieux !)

    systemctl start nagios
    systemctl reload apache2

Configuration pour ACME

    mkdir /etc/apache2/include

    Dans /etc/apache2/include/acme-challenge.conf
    Alias /.well-known/acme-challenge /var/lib/acme/challenges/.well-known/acme-challenge
    <Directory /var/lib/acme/challenges>
      Require all granted
    </Directory>

    Dans /etc/apache2/include/redirect-to-https.conf :
    <ifmodule mod_rewrite.c>
        RewriteEngine On
        RewriteCond %{REQUEST_URI} !^/\.well\-known/acme\-challenge/
	RewriteCond %{REQUEST_URI} !vpn/?$
        RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
    </ifmodule>

## Configuration des machines FDN pour le monitoring

Ajouter à /etc/nagios4/nagios.cfg :

    cfg_dir=/etc/nagios4/objects/hosts
    cfg_dir=/etc/nagios4/objects/groups

Ajouter à /etc/nagios4/objects/commands.cfg :

    define command {
        command_name    irc_cachet_notify
	command_line	$USER2$/cagios/ircbot_cachet.sh "$HOSTNAME$" "$SERVICEDESC$" "$SERVICESTATE$" "$SERVICESTATETYPE$"
    }

Puis on reload

    systemctl reload nagios

Pour références, les fichiers de configuration utilisés sont ici :

* [[./nagios/commands.cfg]]
* [[./nagios/contacts.cfg]]
* [[./nagios/templates.cfg]]

# Installation de Cachet

Voir https://docs.cachethq.io/docs/installing-cachet

    cd /var/www
    git clone https://github.com/cachethq/Cachet.git
    cd Cachet

## Configuration

    cp -a .env.example .env
    editor .env

    curl -sS https://getcomposer.org/installer -o composer.installer
    php composer.installer --install-dir=/usr/local/bin --filename=composer
    chown -R www-data: /var/www/Cachet
    sudo -u www-data composer install --no-dev -o --no-scripts
    sudo -u www-data php artisan key:generate
    mysql_secure_installation
    sudo -u www-data php artisan route:cache

Contournement non support > PHP5.6 :

    cat <<EOF | sudo tee -a bootstrap/cache/routes.php
    // Workaround, see https://github.com/CachetHQ/Cachet/issues/4132
    if(version_compare(PHP_VERSION, '7.0.0', '>=')) {
        error_reporting(E_ALL ^ E_NOTICE ^ E_WARNING);
    }
    EOF


Se connecter sur https://skytop.fdn.fr/
Suivre l'intallateur
cd /var/www/Cachet
sudo -u www-data php artisan down
sudo -u www-data php artisan config:cache
sudo -u www-data php artisan app:update
sudo -u www-data php artisan optimize
sudo rm -rf /var/www/Cachet/bootstrap/cache/*
sudo -u www-data php artisan up

## Création et Configuration de la base de données

    mysql -u -p
    mysql> CREATE DATABASE cachet;
    mysql> GRANT ALL PRIVILEGES ON cachet.* To 'cachetdb'@'localhost' IDENTIFIED BY '********';

## Pour référence: supprimer toutes les entrées

    mysql -u -p
    mysql> use cachet;
    mysql> truncate incidents;

## Configuration de Cachet 

    /var/www/Cachet/.env

    APP_ENV=production
    APP_DEBUG=false
    APP_URL=http://skytop.fdn.fr
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

Les logs Cachet Laravel sont ici : /var/www/Cachet/storage/logs/laravel.log

## Eviter les liens externes vers Google et Cloudflare

La dernière version de Cachet permet de désactiver les dépendances externes (Google Fonts, Trackers..) depuis 
l'interface d'administration, il suffit de décocher :

    Enable Third Party Dependencies (Google Fonts, Trackers, etc...) 

## Cachet & Nagios together

L'objectif est d'alimenter les incidents Cachet via les alertes Nagios pour permettre un affichage user-friendly pour les utilisateurs, pour une 
vision bien plus claire de l'historique des incidents envoyés par Nagios et pour la suite d'utiliser les alertes mail de 
Cachet.

Créer un utilisateur dans [Cachet dashboard](https://skytop.fdn.fr/dashboard), se connecter avec l'utilisateur et récupérer la clef API

Pour tester le script

Simuler un incident (l'hôte doit déjà exister sur Cachet)

    ./usr/lib/nagios/plugins/cagios/ircbot_cachet.sh 'neviani.fr' 'disponibilite' FAILED HARD 'test service casse'

Simuler une reprise à la normale

    ./usr/lib/nagios/plugins/cagios/ircbot_cachet.sh 'neviani.fr' 'disponibilite' OK HARD 'test service casse'

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

* TCP Sockets ICMPv4 & ICMPv6
  - [PASS] test web_ipv4: TCP 80 
  - [PASS] test web_ipv6: TCP 80 
  - [PASS] test web_ipv4: TCP 443  
  - [PASS] test web_ipv6: TCP 443 
  - [PASS] test jabber_ipv4: TCP 5222
  - [PASS] test jabber_ipv6: TCP 5222
  - [PASS] test jabber_ipv4: TCP 5223
  - [PASS] test mail_ipv4: TCP 25
  - [PASS] test mail_ipv6: TCP 25
  - [PASS] test mail_ipv4: TCP 587 
  - [PASS] test mail_ipv6: TCP 587 

* Test DNS par nos résolveurs
  - [PASS] test dns_ipv4: www.gnu.org!208.118.235.148 (IPv4 depuis DNSv4)
  - [PASS] test dns_ipv6: www.gnu.org!208.118.235.148 (IPv4 depuis DNSv6)

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

* Test HTTPS
  - [PASS] test web_ipv4: fdn.fr 301 -> 200 OK
  - [PASS] test web_ipv6: fdn.fr 301 -> 200 OK
  - [PASS] test web_ipv4: adminsys.fdn.fr 401 Unauthorized
  - [PASS] test web_ipv6: adminsys.fdn.fr 401 Unauthorized
  - [PASS] test web_ipv4: lists.fdn.fr 302 Found -> 200 OK
  - [PASS] test web_ipv6: lists.fdn.fr 302 Found -> 200 OK
  - [PASS] test web_ipv4: git.fdn.fr 302 Found -> 200 OK
  - [PASS] test web_ipv6: git.fdn.fr 302 Found -> 200 OK

* Test validité certificats X.509
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

## Version en service
### Version 1.9

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
* Migration de LDN (Isengard) vers Skytop (Grenode)
* Passage en Debian 11 Bullseye

## Roadmap / Investigation

* Test pppoe: écrire un plugin (ça n'a pas l'air d'exister) et demander credential et étudier faisabilité car LNS écoutent sur des interfaces particulières
