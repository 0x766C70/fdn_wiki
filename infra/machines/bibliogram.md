Machine virtuelle pour le service [Bibliogram](https://git.sr.ht/~cadence/bibliogram) permettant d'accéder à Instagram.


# Caractéristiques

- machine virtuelle (proxmox)
- distribution : Debian Buster

# Administration

- service : `systemctl [status|start|stop|restart] bibliogram.service`
- logs : `/var/log/daemon.log`, `/var/log/syslog`, `/var/log/nginx/[access|error].log`


# Buildbook

Cf. doc [projet](https://git.sr.ht/~cadence/bibliogram-docs/tree/master/docs/Configuring.md)

Notes:

- le dépôt nodejs est dans puppet
- le *home* de l'utilisateur bibliogram est dans `/srv`
- le dépôt est cloné dans `/srv/bibliogram/app`
- la conf spécifique pour fdn est dans la branche **fdn-custom**
- TLS via certbot : `apt install certbot`
- derrière un proxy nginx : `/etc/nginx/sites-enabled/bibliogram`

	server {
	        listen 80 default_server;
	        listen [::]:80 default_server;
	        server_name bibliogram.fdn.fr;
	
	        include snippets/letsencrypt.conf;
	        return 301 https://$host$request_uri;
	}
	server {
	        listen 443 ssl http2 default_server;
	        listen [::]:443 ssl http2 default_server;
	        server_name bibliogram.fdn.fr;
	
	        include snippets/letsencrypt.conf;
	        ssl_certificate /etc/letsencrypt/live/bibliogram.fdn.fr/fullchain.pem;
	        ssl_certificate_key /etc/letsencrypt/live/bibliogram.fdn.fr/privkey.pem;
	        include snippets/ssl.conf;
	        ssl_trusted_certificate /etc/letsencrypt/live/bibliogram.fdn.fr/chain.pem;
	
	        client_max_body_size 5M;
	
	        location / {
	                proxy_set_header X-Real-IP $remote_addr;
	                proxy_pass http://localhost:10407;
	        }
	}
