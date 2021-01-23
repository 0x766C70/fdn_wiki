Machine virtuelle pour le service [Invidious](https://github.com/omarroth/invidious) permettant d'accéder à Youtube.

[[!toc levels=2]]

# Caractéristiques

- machine virtuelle (proxmox)
- distribution : Debian Buster

# Administration

- service : `systemctl [status|start|stop|restart] invidious.service`
- logs : `/var/log/syslog`, `/var/log/nginx/[access|error].log`, `/srv/invidious/app/invidious.log`

# FAQ

- Erreur `Too many open files` : augmenter le nombre en root, ex `ulimit -n 4096`

# Buildbook

Cf. doc [projet](https://github.com/omarroth/invidious/blob/61150c74d21bc98e4b819602bbca67ca23b82dc0/README.md)

Notes:

- le dépôt crystal est dans puppet
- le *home* de l'utilisateur invidious est dans `/srv`
- le dépôt est cloné dans `/srv/invidious/app`
- la conf spécifique pour fdn est dans la branche **fdn**
- rotation des logs en place : `/etc/logrotate.d/invidious.logrotate`
- TLS via certbot : `apt install certbot`
- derrière un proxy nginx : `/etc/nginx/sites-enabled/invidious`

	server {
		listen 80;
		listen [::]:80;
		listen 443 ssl http2;
		listen [::]:443 ssl http2;

		server_name invidious.fdn.fr;

		access_log off;
		error_log /var/log/nginx/error.log crit;

		ssl_certificate /etc/letsencrypt/live/invidious.fdn.fr/fullchain.pem;
		ssl_certificate_key /etc/letsencrypt/live/invidious.fdn.fr/privkey.pem;
		ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
		ssl_session_timeout 1d;
		ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
		ssl_session_tickets off;
		ssl_protocols TLSv1.2 TLSv1.3;
		ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
		ssl_prefer_server_ciphers off;
		ssl_stapling on;
		ssl_stapling_verify on;
		ssl_trusted_certificate /etc/letsencrypt/live/invidious.fdn.fr/chain.pem;

		location / {
			proxy_pass http://127.0.0.1:3000/;
			proxy_set_header X-Forwarded-For $remote_addr;
			proxy_set_header Host $host;    # so invidious knows domain
			proxy_http_version 1.1;         # to keep alive
			proxy_set_header Connection ""; # to keep alive
		}

		if ($https = '') { return 301 https://$host$request_uri; }      # if not connected to https, perma redirect to https
	}
