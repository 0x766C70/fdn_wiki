Machine virtuelle pour le service [Nitter](https://github.com/zedeus/nitter) permettant d'accéder à Twitter.


# Caractéristiques

- machine virtuelle (proxmox)
- distribution : Debian Bullseye

# Administration

- service : `systemctl [status|start|stop|restart] nitter.service`
- logs : `/var/log/syslog`, `/var/log/apache2/nitter-[access|error].log`

## Mise à jour

1. créer un snapshot de la VM (ex : `maj_nitter`)
1. se connecter en SSH sur la VM
1. `sudo systemctl stop redis-server` # Pour avoir de la RAM libre pour pouvoir compiler
1. `sudo su - nitter`
1. `cd app`
1. `git stash` # On met de côté nos modifs locales¹
1. `git pull`
1. `git stash pop` # On applique nos modifs mises de côté
1. `nimble build -d:release`
1. `nimble scss`
1. `nimble md`
1. `exit`
1. `sudo systemctl restart nitter.service`
1. `sudo systemctl start redis-server`

[¹] Le fichier _/srv/nitter/app/src/views/general.nim_ a été modifié afin de pouvoir afficher un message personalisé sur chaque page (pour les demandes légales).

# Buildbook

Cf. doc [projet](https://github.com/zedeus/nitter/tree/a8d99cc6857f7f8e38023d9a5e8cf77333153291)

Notes:

- installation de [nim](https://nim-lang.org) via `apt`
- le *home* de l'utilisateur nitter est dans `/srv/nitter`
- le dépôt est cloné dans `/srv/nitter/app`
- TLS via acme_tiny
- derrière un proxy Apache (port **8080**) : `/etc/apache2/sites-enabled/nitter.fdn.fr.conf`
```
<VirtualHost *:80>
	ServerName nitter.fdn.f
	
	Redirect / https://nitter.fdn.fr
	
	Include /etc/apache2/include/acme-challenge.conf
	
	# logging
	ErrorLog ${APACHE_LOG_DIR}/nitter-error.log
	CustomLog ${APACHE_LOG_DIR}/nitter-access.log combined
</VirtualHost>

<IfModule mod_ssl.c>
<VirtualHost *:443>
	ServerName nitter.fdn.fr
	
	# Logging
	ErrorLog ${APACHE_LOG_DIR}/nitter-error.log
	CustomLog ${APACHE_LOG_DIR}/nitter-access.log combined
	
	# Nitter Proxy Configuration
	ProxyPreserveHost On
	ProxyPass / http://127.0.0.1:8080/ nocanon
	ProxyPassReverse / http://127.0.0.1:8080/
	AllowEncodedSlashes On
	
	# Lets Encrypt TLS Settings
	SSLEngine on
	SSLCertificateFile /etc/apache2/ssl/nitter.fdn.fr/nitter.fdn.fr.chained
	SSLCertificateKeyFile /etc/apache2/ssl/nitter.fdn.fr/nitter.fdn.fr.key
</VirtualHost>
</IfModule>

# https://ssl-config.mozilla.org/#server=apache&version=2.4.41&config=intermediate&openssl=1.1.1d&guideline=5.4
SSLProtocol             all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite          ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384
SSLHonorCipherOrder     off
SSLSessionTickets       off

SSLUseStapling On
SSLStaplingCache "shmcb:logs/ssl_stapling(32768)"
