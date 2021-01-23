Machine virtuelle pour l'hébergement mutualisé de sites web des adhérents. Remplacera à terme [[infra/machines/yoda]].

[[!toc levels=2]]

# Caractéristiques

- machine virtuelle
- distribution : Debian Stretch
- noyau : 4.9.0-8-amd64
- processeurs : 2
- RAM : 2 Go
- partitions :
  - `/` : 30 Go
  - `/srv` : 30 Go
  - `/var/log` : 30 Go

# Buildbook

## Système

	apt update
	apt upgrade
	apt install ca-certificates apt-transport-https whois
	mkdir -p /etc/skel/sites

## PHP-fpm

Cf. [article](https://tecadmin.net/install-multiple-php-version-with-apache-on-debian/)

	echo "deb https://packages.sury.org/php/ stretch main" | tee /etc/apt/sources.list.d/php-fpm.list
	wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add -
	apt update
	apt upgrade
	apt install php7.2 php7.2-fpm

## Apache2

	apt install apache2 libapache2-mod-fcgid
	a2enmod actions fcgid alias proxy_fcgi userdir
	systemctl restart apache2
Memo : conf de mutu.fdn.fr finale

	<VirtualHost *:80>
		Include /etc/apache2/include/redirect-to-https.conf
	</VirtualHost>

	<VirtualHost *:443>
		ServerAdmin adminsys@fdn.fr
		ServerName mutu.fdn.fr
		DocumentRoot /var/www/html

		<IfModule mod_userdir.c>
			UserDir /srv/webusers/*/sites/
			UserDir disabled
			UserDir enabled afriquet amagnouat jpalbert mherinx sascoet
			<Directory /srv/webusers/*/sites/>
				Require all granted
				Options Indexes FollowSymLinks
				AllowOverride All
			</Directory>
		</IfModule>

		Alias /adminer /var/www/adminer
		<Directory /var/www/adminer>
			Require all granted
			<FilesMatch \.php$>
				SetHandler "proxy:unix:/var/run/php/php7.2-fpm-fdn.sock|fcgi://localhost/"
			</FilesMatch>
		</Directory>

		Include /etc/apache2/include/acme-challenge.conf

		SSLEngine on
		SSLCertificateFile      /etc/apache2/ssl/mutu.fdn.fr/mutu.fdn.fr.chained
		SSLCertificateKeyFile   /etc/apache2/ssl/mutu.fdn.fr/mutu.fdn.fr.key

		ErrorLog ${APACHE_LOG_DIR}/mutu.fdn.fr/error.log
		CustomLog ${APACHE_LOG_DIR}/mutu.fdn.fr/access.log combined
	</VirtualHost>

	# vim: syntax=apache ts=4 sw=4 sts=4 sr noet

## MariaDB

	apt install mariadb-server
	mysql_secure_installation
	systemctl stop mariadb
	mkdir -p /srv/db
	chmod o+rx /srv/db
	rsync -av /var/lib/mysql /srv/db
	rm -rf /var/lib/mysql
	vi /etc/mysql/mariadb.conf.d/50-server.cnf
	===> change datadir to /srv/db/mysql
	systemct start mariadb

## Adminer

	wget https://www.adminer.org/latest.php
	mkdir -p /var/www/adminer
	mv latest.php /var/www/adminer/index.php
	vi /etc/apache2/sites-enabled/mutu.fdn.fr.conf
rajouter le bloc

	Alias /adminer /var/www/adminer
	<Directory /var/www/adminer>
		Require all granted
		<FilesMatch \.php$>
			SetHandler "proxy:unix:/var/run/php/php7.2-fpm-fdn.sock|fcgi://localhost/"
		</FilesMatch>
	</Directory>
puis

	systemctl reload apache2
	apt install php7.2-mysql

## TLS

Suivre la procédure [[outils/letsencrypt]] pour mettre en place un certificat TLS pour Apache 2.4 et le domaine **mutu.fdn.fr**.

## Logs Apache2

	mkdir -p /var/log/apache2/webusers/
	chmod o+x /var/log/apache2
	chmod o+x /var/log/apache2/webusers/

Memo : exemple de conf logrotate par utilisateur (`/etc/logrotate.d/apache2-username`)

	/var/log/apache2/webusers/<username>/*/*.log {
	        daily
	        missingok
	        rotate 366
	        compress
	        delaycompress
	        notifempty
	        create 640 root <username>
	        sharedscripts
	        postrotate
	                if /etc/init.d/apache2 status > /dev/null ; then \
	                    /etc/init.d/apache2 reload > /dev/null; \
	                fi;
	        endscript
	        prerotate
	                if [ -d /etc/logrotate.d/httpd-prerotate ]; then \
	                        run-parts /etc/logrotate.d/httpd-prerotate; \
	                fi; \
	        endscript
	}

## DNS

	apt install bind9

	$ cat /etc/bind/named.conf.local
	//
	// Do any local configuration here
	//

	// Consider adding the 1918 zones here, if they are not used in your
	// organization
	//include "/etc/bind/zones.rfc1918";

	zone "mutu.fdn.fr" {
		type master;
		file "/etc/bind/db.mutu";
	};

	$ cat /etc/bind/db.mutu
	;
	; BIND data file for mutu.fdn.fr
	;
	$TTL    604800
	$ORIGIN mutu.fdn.fr.

	@               IN      SOA     ns.mutu.fdn.fr. adminsys.fdn.fr. (
			     2019012804         ; Serial
				 604800         ; Refresh
				  86400         ; Retry
				2419200         ; Expire
				 604800 )       ; Negative Cache TTL

	@               IN      NS      ns.mutu.fdn.fr.
	ns              IN      A       80.67.169.95
	ns              IN      AAAA    2001:910:800::95
	@               IN      A       80.67.169.95
	@               IN      AAAA    2001:910:800::95

	; webusers
	username        IN      CNAME   ns
