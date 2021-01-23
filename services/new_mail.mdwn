[[!meta title="[DRAFT] new email infra"]]

Mise en place d'une nouvelle infra email

Linux guri.fdn.fr 4.9.0-8-amd64 #1 SMP Debian 4.9.130-2 (2018-10-27) x86_64 GNU/Linux

# Installation des paquets Debian
## Update du system
	sudo apt update
	sudo apt upgrade

## Installation du serveur web et de la base de donnée
	# install le server web, la db et ses dépendance
	sudo apt install build-essential apache2 php7.0 mariadb-server php7.0-sql
	# sécuriser mariaDB en bloquant l'accès à root
	sudo mysql_secure_installation

## Préparation de la DB
	sudo mysql
	# Création du SUPERUSER de mariaDB
	sql> CREATE USER 'adminDB'@'localhost' IDENTIFIED BY 'my_admin_DB_passwd';
	sql> GRANT ALL PRIVILEGES ON *.* TO 'adminDB'@'localhost' WITH GRANT OPTION;
	# Création de la DB postfix
	sql> CREATE DATABASE postfix;
	# Création du user postfix en full accès sur la DB posfix. C'est le user qui sera utilisé par postfixadmin pour la gestion globale des domaines et mailbox virtuelles.
	sql> CREATE USER 'postfix'@'localhost' IDENTIFIED BY 'postfix_DB_passwd';
	sql> GRANT ALL PRIVILEGES ON postfix.* TO 'postfix'@'localhost';
	# Création du user mailuser en lecture seul sur postfix
	sql> CREATE USER 'mailuser'@'localhost' IDENTIFIED BY 'mailuser_DB_passwd';
	sql> GRANT SELECT ON postfix.* TO 'mailuser'@'localhost';
	sql> FLUSH PRIVILEGES;
	sql> exit

## Installation du MTA postfix + postifix-mysql + sasl2
	sudo apt install postfix postfix-mysql libsasl2-modules sasl2-bin
	
Répondre: "Internet Site" - "guri.fdn.fr"

>ouvrir port 25: inter MTA


>ouvrir port 597: SMTP via TLS

## Mise en place certificats:

Si machine fdn, trouver les certifs:
    /etc/apache2/ssl/guri.fdn.fr/
Si machine non fdn, générer les certifs:
    openssl req -new -x509 -days 3650 -nodes -newkey rsa:4096 -out /etc/ssl/certs/mailserver.pem -keyout /etc/ssl/private/mailserver.pem

## Installation Postfixadmin pour gérer les domaines et users
	cd /srv
	sudo git clone https://github.com/postfixadmin/postfixadmin.git
	sudo ln -s /srv/postfixadmin/public /var/www/postfixadmin
	sudo nano /srv/postfixadmin/config.local.php
		<?php
			$CONF['database_type'] = 'mysqli';
			$CONF['database_user'] = 'postfix';
			$CONF['database_password'] = 'postfix_DB_passwd';
			$CONF['database_name'] = 'postfix';
			$CONF['configured'] = true;
		?>
	# Création du répertoire de config postfixadmin
	sudo mkdir -p /srv/postfixadmin/templates_c
	sudo chown -R www-data /srv/postfixadmin/templates_c
	# Activer le module apache https
	sudo a2enmod ssl
	sudo nano /etc/apache2/sites-available/postfixadmin-ssl.conf
		<IfModule mod_ssl.c>
			<VirtualHost *:443>
				ServerAdmin vlp@guri.fdn.fr
				ServerName postfixadmin.guri.fdn.fr
				DocumentRoot /var/www/postfixadmin/
				SSLEngine on
				SSLCertificateFile /etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.crt
				SSLCertificateKeyFile /etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.key
			</VirtualHost>
		</IfModule>
	# Activer le fichier de conf postfixadmon
	sudo a2ensite postfixadmin-ssl.conf
	sudo systemctl restart apache2

go to http://postfixadmin.guri.fdn.fr/setup.php *note: peut être un peu long (5mn)*

* Insérer un setup_passwd pour en générer un hash qui sera à copier dans /srv/postfixadmin/config.local.php (la lignes à copier est affichée directement par postfixadmin)
* Créer Superuser Postfix admin (setup_passwd nécessaire)

Postfixadmin accessible sur http://postfixadmin.guri.fdn.fr

## Installation du server IMAP Dovecot

> ouvrir port 143: IMAP via TLS

	sudo apt install dovecot-mysql dovecot-pop3d dovecot-imapd dovecot-managesieved

# Paramétrage
## DNS
	Ajouter champs:
	@   			IN  MX  10  guri.fdn.fr
	mail    		IN  CNAME   guri.fdn.fr
	postfixadmin    IN  CNAME   guri.fdn.fr
	
## Activation de saslauthd pour mettre en place l'auth du smtp
	sudo nano /etc/default/saslauthd
	START=no => START=yes
	sudo systemctl restart saslauthd

## Ajouter un user vmail qui va gérer les emails
	sudo groupadd -g 5000 vmail
	sudo useradd -g vmail -u 5000 vmail -d /var/vmail -m

## Config Postfixadmin

go to https://postfixadmin.guri.fdn.fr

Créer domaine virtuelle: domain list>New Domain

	Domaine: 					guri.fdn.fr
	Descriptions:				fdn email server
	Aliases:					0
	Mailboxes:					0
	Mail server is backup MX: 	unchecked
	Active:						checked
	Add default mail aliases:	checked
	Pass expires:				-1
	
Créer mailbox: virtual List> créer contact@guri.fdn.fr

## Pour que postfix ait accès aux domaines virtuels on lui donne accès à la db

	sudo nano /etc/postfix/mysql-virtual-mailbox-domains.cf
		user = mailuser
		password = mailuser_DB_passwd
		hosts = 127.0.0.1
		dbname = postfix
		query = SELECT 1 FROM domain WHERE domain='%s'
	# activer config:
	sudo postconf -e virtual_mailbox_domains=mysql:/etc/postfix/mysql-virtual-mailbox-domains.cf

Pour tester si OK:

	sudo postmap -q guri.fdn.fr mysql:/etc/postfix/mysql-virtual-mailbox-domains.cf
	
Si retour = 1 => domaine trouvé => config ok

## Même travail sur les boite emails virtuelles

	sudo nano /etc/postfix/mysql-virtual-mailbox-maps.cf
		user = mailuser
		password = mailuser_DB_passwd
		hosts = 127.0.0.1
		dbname = postfix
		query = SELECT 1 FROM mailbox WHERE username='%s'
	# activer config:
	sudo postconf -e virtual_mailbox_maps=mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf

Pour tester si OK:

	sudo postmap -q contact@guri.fdn.fr mysql:/etc/postfix/mysql-virtual-mailbox-maps.cf

Si retour = 1 => mailbox trouvée => config ok

## Même travail sur les alias

	sudo nano /etc/postfix/mysql-virtual-alias-maps.cf
		user = mailuser
		password = mailuser_DB_passwd
		hosts = 127.0.0.1
		dbname = postfix     
		query = SELECT goto FROM alias WHERE address='%s'
	# activer config:
	sudo postconf -e virtual_alias_maps=mysql:/etc/postfix/mysql-virtual-alias-maps.cf

Pour tester si OK:

	sudo postmap -q abuse@guri.fdn.fr mysql:/etc/postfix/mysql-virtual-alias-maps.cf

Le retour doit donner le mail de destination de l'alias

Changer les droits des 3 fichiers car ils contiennent le passwd de mailuser:

	sudo chgrp postfix /etc/postfix/mysql-*.cf
	sudo chmod u=rw,g=r,o= /etc/postfix/mysql-*.cf
	
## Activation du port 587

Dans /etc/postfix/master.cf, décommenter la ligne :

	submission inet n       -       -       -       -       smtpd
	
## Activation de SASL

Dans /etc/postfix/main.cf, ajouter/modifier:

	# Config smtpd
	smtpd_use_tls = yes
	smtpd_tls_security_level = may
	smtpd_tls_cert_file=/etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.crt
	smtpd_tls_key_file=/etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.key
	#smtpd_tls_CAfile              = /etc/apache2/ssl/guri.fdn.fr/
	#smtpd_tls_dh1024_param_file   = /etc/apache2/ssl/guri.fdn.fr/
	#smtpd_tls_dh512_param_file    = /etc/apache2/ssl/guri.fdn.fr/
	smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache
	smtpd_tls_mandatory_protocols = !SSLv3, !TLSv1, !TLSv1.1
	smtpd_tls_protocols = !SSLv3, !TLSv1, !TLSv1.1
	smtpd_sasl_type = dovecot
	smtpd_sasl_path = private/auth
	smtpd_sasl_auth_enable = yes
	smtpd_tls_auth_only = yes
	smtpd_tls_received_header = yes
	disable_vrfy_command = yes
	message_size_limit = 32000000
	# HELO restrictions: HELO dommand
	# Retarde l'evaluation des entrée postix
	smtpd_delay_reject = yes
	# Rejette les emails des clients qui ne se présentent pas correctement
	smtpd_helo_required = yes 
	smtpd_helo_restrictions =
		# Accepte les connexion de notre réseau 127.0.0.0/8
		permit_mynetworks,
		# Rejet si l'hostname n'est pas un fqdn
		reject_non_fqdn_helo_hostname,
		# Rejet si hostname non conforme
		reject_invalid_helo_hostname,
		permit
	# Sender restrictions: FROM command
	smtpd_sender_restrictions =
		# Accepte les connexion de notre réseau 127.0.0.0/8
		permit_mynetworks,
		# Rejet si le domaine du from email n'est pas un fqdn
		reject_non_fqdn_sender,
		# rejet si le domaine du from email n'existe pas
		reject_unknown_sender_domain,
		permit
	# Recipien restrictions: TO command
	smtpd_recipient_restrictions =
		# Sécurité pour couper spam en bulk
		reject_unauth_pipelining,
		# Rejet si le domaine du TO email n'est pas un fqdn
		reject_non_fqdn_recipient,
		# Rejet si le domaine du TO email n'existe pas
		reject_unknown_recipient_domain,
		# Accepte les connexion de notre réseau 127.0.0.0/8
		permit_mynetworks,
		# Accepte les connexion authentifiées
		permit_sasl_authenticated,
		# Rejet sauf si c'est un message livré sur notre réseau
		reject_unauth_destination,
		# Filtre spamhaus
		reject_rbl_client zen.spamhaus.org,
		reject_rhsbl_reverse_client dbl.spamhaus.org ,
		reject_rhsbl_helo dbl.spamhaus.org,	
		reject_rhsbl_sender dbl.spamhaus.org	
	# Data restrictions:
	smtpd_data_restrictions = reject_unauth_pipelining # coupe les clients qui parlent trop tôt.
	# Config smtp
	smtp_use_tls = yes
	smtp_tls_security_level = may	
	smtp_tls_cert_file=/etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.crt
	smtp_tls_key_file=/etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.key
	smtp_tls_session_cache_database = btree:${data_directory}/smtp_scac$
	smtp_tls_mandatory_protocols = !SSLv3, !TLSv1, !TLSv1.1
	smtp_tls_protocols = !SSLv3, !TLSv1, !TLSv1.1
	smtp_tls_note_starttls_offer = yes
	smtp_tls_enforce_peername = no
	



## Config auth pour Dovecot ##

Dans /etc/dovecot/conf.d/10-auth.conf modifier la ligne suivante en:
	
	disable_plaintext_auth = yes
	auth_mechanisms = plain login
	
et changer les includes en 

	#!include auth-system.conf.ext
	!include auth-sql.conf.ext
	#!include auth-ldap.conf.ext
	#!include auth-passwdfile.conf.ext
	#!include auth-checkpassword.conf.ext
	#!include auth-vpopmail.conf.ext
	#!include auth-static.conf.ext

afin de spécifier que nous utilisons des utilisateurs virtuel dans la db SQL

##Configuration SQL pour Dovecot

Dans /etc/dovecot/conf.d/auth-sql.conf.ext commentez les autres userdb pour ajouter uniquement:

    userdb {
        driver = static
        args = uid=vmail gid=vmail home=/var/vmail/%d/%n
    }

C'est vmail. créé plus haut qui va gérer les emails

## Configuration mail Dovecot

Dans /etc/dovecot/conf.d/10-mail.conf, modifiez le paramètre mail_location:

	mail_location = maildir:/var/vmail/%d/%n/Maildir

## Configuration master Dovecot

Dans /etc/dovecot/conf.d/10-master.conf, dans le bloc service auth, spécifiez le smtp-auth de postfix

	# Postfix smtp-auth
	unix_listener /var/spool/postfix/private/auth {
		mode = 0660
		user = postfix
		group = postfix
	}

## Config SSL

Dans /etc/dovecot/conf.d/10-ssl.conf:

	ssl = yes
	ssl_cert = </etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.crt
	ssl_key = </etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.key
	ssl_protocols = !SSLv3, !TLSv1, !TLSv1.1
	ssl_cipher_list = ALL:!kRSA:!SRP:!kDHd:!DSS:!aNULL:!eNULL:!EXPORT:!DES:!3DES:!MD5:!PSK:!RC4:!ADH:!LOW@STRENGTH 
	ssl_prefer_server_ciphers = yes # Dovecot > 2.2.x
	ssl_dh_parameters_length = 2048 # Dovecot > 2.2.x


## Config du LDA

Dans /etc/dovecot/conf.d/15-lda.conf, ajouter:

	protocol lda {
		# Space separated list of plugins to load (default is global mail_plugins).
		mail_plugins = $mail_plugins sieve
	}

## Connexion SQL pour Dovecot

Dans /etc/dovecot/dovecot-sql.conf.ext, ajouter/modifier:

	driver = mysql
	connect = host=127.0.0.1 dbname=postfix user=mailuser password=mailuser_DB_passwd
	password_query = SELECT username,domain,password FROM mailbox WHERE username='%u';

on change les droits de ce fichier vu qu'il contient un mot de passe :

	sudo chown root:root /etc/dovecot/dovecot-sql.conf.ext
	sudo chmod go= /etc/dovecot/dovecot-sql.conf.ext

## Finalisation Dovecot

Dans /etc/postfix/main.cf, modifier:

	mydestination = localhost.info, localhost

Puis:

	sudo chgrp vmail /etc/dovecot/dovecot.conf
	sudo chmod g+r /etc/dovecot/dovecot.conf
	sudo systemctl restart dovecot
	
Note:

	When Dovecot starts up for the first time, it generates new 512bit and 1024bit Diffie Hellman parameters and saves them into /var/lib/dovecot/ssl-parameters.ssl. After the initial creation they are by default regenerated every week. With newer computers the generation shouldn't take more than a few seconds

##  Connecter Postfix à Dovecot

Dans /etc/postfix/master.cf, modifier:

	dovecot   unix  -       n       n       -       -       pipe
	  flags=DRhu user=vmail:vmail argv=/usr/lib/dovecot/dovecot-lda -f ${sender} -d ${recipient}

Note: la deuxième ligne est indentée par deux espaces

	sudo systemctl restart postfix
	sudo postconf -e virtual_transport=dovecot
    sudo postconf -e dovecot_destination_recipient_limit=1
    sudo chmod 755 /etc/mailname

# Spamassassin

## Install

	sudo apt install spamassassin spamc

## link spamassassin à Postfix
	
Dans nano /etc/postfix/master.cf, modifier:

	smtp      inet  n       -       n       -       -       smtpd
	To:
	smtp      inet  n       -       n       -       -       smtpd -o content_filter=spamassassin

	#submission     inet  n       -       n       -       -       smtpd
	To:
	submission     inet  n       -       n       -       -       smtpd -o content_filter=spamassassin

ajouter à la fin:

	spamassassin unix - n n - - pipe
	  flags=R user=debian-spamd argv=/usr/bin/spamc -e /usr/sbin/sendmail -oi -f ${sender} ${recipient}
  
Note: la deuxième ligne est indentée par deux espaces

## config spamassassin

Dans /etc/spamassassin/local.cf, ajouter:

	rewrite_header Subject [***** SPAM _SCORE_ *****]	
	required_score 5.0
	use_bayes 1
	bayes_auto_learn 1

Dans /etc/default/spamassassin, modifier:

	CRON=1

Puis 
	sudo systemctl enable spamassassin
	sudo systemctl start spamassassin

## Razor

> ouvrir port 2703

	sudo apt install razor
	cd /etc/spamassassin
	sudo mkdir razor
	sudo razor-admin -home=/etc/spamassassin/razor -register
	sudo razor-admin -home=/etc/spamassassin/razor -create
	sudo razor-admin -home=/etc/spamassassin/razor -discover
	
Ajouter dans /etc/spamassassin/local.cf:

	razor_config /etc/spamassassin/razor/razor-agent.conf
	#surtout utile au debug
	add_header all Report _REPORT_
	add_header spam Flag _YESNOCAPS_
	add_header all Status _YESNO_, score=_SCORE_ required=_REQD_ tests=_TESTS_ autolearn=_AUTOLEARN_ version=_VERSION_
	add_header all Level _STARS(*)_
	add_header all Checker-Version SpamAssassin _VERSION_ (_SUBVERSION_) on _HOSTNAME_

Ajouter  /etc/mail/spamassassin/razor/razor-agent.conf

	razorhome = /etc/mail/spamassassin/razor	

	sudo systemctl restart spamassassin
	
Test:

	echo "test" | spamassassin -D razor2 2>&1 | less

## Pyzor

> ouvrir port 24441
	
	sudo apt install pyzor
	sudo chmod 755 /etc/spamassassin/pyzor/

Ajouter dans /etc/spamassassin/local.cf

	pyzor_options --homedir /etc/mail/spamassassin/pyzor
	
Puis

	sudo systemctl restart spamassassin

# Sieve

> ouvrir port 4190

	sudo apt install dovecot-sieve dovecot-managesieved

Dans /etc/dovecot/conf.d/20-lmtp.conf, ajouter:

	protocol lmtp {
		postmaster_address = vlp@guri.fdn.fr
		mail_plugins = $mail_plugins sieve
	}
	
Dans nano /etc/dovecot/conf.d/90-sieve.conf:

	plugin {
		sieve = ~/.dovecot.sieve
		sieve_global_path = /var/lib/dovecot/sieve/default.sieve
		sieve_dir = ~/sieve
		sieve_global_dir = /var/lib/dovecot/sieve/
	}
	
	sudo systemctl restart dovecot

# Rainloop

> ouvrir port 443

	cd /srv
	sudo apt install php7.0-curl
	sudo -i
	mkdir rainloop
	wget -qO- https://repository.rainloop.net/installer.php | php
	exit
	cd rainloop
	sudo find . -type d -exec chmod 755 {} \;
	sudo find . -type f -exec chmod 644 {} \;
	sudo chown -R www-data:www-data .
	sudo ln -s /srv/rainloop/ /var/www/rainloop
	sudo nano /etc/apache2/sites-available/rainloop-ssl.conf
		<IfModule mod_ssl.c>
			<VirtualHost *:443>
				ServerAdmin vlp@guri.fdn.fr
				ServerName webmail.guri.fdn.fr
				DocumentRoot /var/www/rainloop/
				<Directory /var/www/rainloop/data/>
					Order deny,allow
					deny from all
				</Directory>
				SSLEngine on
				SSLCertificateFile /etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.crt
				SSLCertificateKeyFile /etc/apache2/ssl/guri.fdn.fr/guri.fdn.fr.key
			</VirtualHost>
		</IfModule>
	sudo a2ensite rainloop-ssl.conf
	sudo systemctl restart apache2 
	
Accès à l'admin: https://webmail.guri.fdn.fr/?admin

	Default login is "admin", password is "12345".
	
Dans la config:

  * changer le pass admin
  * ajouter le domaine guri.fdn.fr en starttls + active sieve (tout se préconfigure tout seul pour les ports)
  * go !!

# DKIM, SPF, DMARC

## DKIM

## SPF

Le champ SPF est un enregistrement de type TXT, qui précise les noms de domaine ou les adresses IP ayant le droit d’expédier des e-mails au nom du domaine

Ajouter le champs:

	@		IN TXT    "v=spf1 ?all" 
	
option:

  * v=spf1:		indique la version de SPF utilisée.
  * a:			autorise l’envoi depuis toutes les adresses IP répertoriées dans l’enregistrement A de votre zone DNS
  * mx:			autorise l’envoi depuis toutes les adresses IP répertoriées dans l’enregistrement MX de votre zone DNS
  * ?all:		     des serveurs supplémentaires qui peuvent faire des envois	
  * -all:		n’autorise strictement aucun envoi autrement que par l’un des éléments listés

## DMARC
