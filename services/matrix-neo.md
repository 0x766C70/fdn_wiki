FDN fournit une instance Synapse.

# Synapse
## Installation depuis les paquets backports (Buster en Mai 2020)
	sudo apt -t buster-backports install matrix-synapse

## Debconf
	Name of the server: matrix.fdn.fr
	Report anonymous statistics? [yes/no] no

## Let's encrypt
[Deprecation of ACME v1](https://github.com/matrix-org/synapse/blob/develop/docs/ACME.md)

- for existing installs, Synapse's built-in ACME support will continue to work until June 2020
- for new installs, this feature will not work at all.

## Certbot
	sudo apt-get install certbot
	sudo certbot certonly --standalone
	Enter email address (used for urgent renewal and security notices) (Enter 'c' to cancel): admin@fdn.fr
	(A)gree/(C)ancel: A
	(Y)es/(N)o: N
	Please enter in your domain name(s) (comma and/or space separated)  (Enter 'c' to cancel): matrix.fdn.fr

## Import de l'ancienne base sur le nouveau serveur (doc au cas où dans le futur l'opération devra être reproduite)
### PostgreSQL (neo.fdn.fr)
	systemctl stop puppet
	deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
	apt-get update
	apt install postgresql-9.6

### PostgreSQL (pz4co.fdn.fr)
	su - postgres
	pg_dump -Fc synapse > /data/t/synapse_pz4co.dump

### Depuis neo.fdn.fr
	scp pz4co@jabba.fdn.fr:synapse_pz4co.dump /var/lib/postgresql/dump.pz4co
	createdb synapse
	createuser --pwprompt synapse_user
	psql
	CREATE DATABASE synapse
	ENCODING 'UTF8'
	LC_COLLATE='C'
	LC_CTYPE='C'
	template=template0
	OWNER synapse_user;
	\q

	/etc/postgresql/9.6/main/pg_hba.conf
	host    synapse         synapse_user    ::1/128                 md5

### Import de la base sur neo.fdn.fr
	 su - postgres
	 pg_restore -d synapse /var/lib/postgresql/dump.pz4co/synapse_pz4co.dump

### copy de media_store
	mkdir lib/synapse
	scp -r pz4co@jabba.fdn.fr:media_store /var/lib/synapse

## Creation du dh
	mkdir /etc/ssl/dh
	openssl dhparam -out /etc/ssl/dh/matrix.fdn.fr.pem -5 4096

## Demarage de synapse 
	systemctl start matrix-synapse

## Installation Nodejs
    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    sudo apt-get install -y nodejs

## Génération du passkey.pem
    openssl genpkey -out passkey.pem -outform PEM -algorithm RSA -pkeyopt rsa_keygen_bits:2048

## IRC bridge install + conf
	apt install make gcc build-essential node-typescript
	sudo adduser --system  matrix-bridge-irc
	sudo mkdir -p /usr/lib/node_modules/matrix-appservice-irc/bin/matrix-appservice-irc
	ln -s /usr/lib/node_modules/matrix-appservice-irc/bin/matrix-appservice-irc /usr/bin/matrix-appservice-irc
	chown -R matrix-bridge-irc: /usr/lib/node_modules/ 

	/etc/passwd
	matrix-bridge-irc:x:116:65534::/home/matrix-bridge-irc:/bin/bash

	su - matrix-bridge-irc
	npm install matrix-appservice-irc --global
	cd /usr/lib/node_modules/matrix-appservice-irc
	npm install
	npm test

## IRC bridge PostgreSQL
	su - postgres
	createuser --pwprompt irc_bridge_db_user
	psql
	CREATE DATABASE irc_bridge_db
	ENCODING 'UTF8'
	LC_COLLATE='C'
	LC_CTYPE='C'
	template=template0
	OWNER irc_bridge_db_user;

	/etc/postgresql/11/main/pg_hba.conf
	host    irc_bridge_db   irc_bridge_db_user    ::1/128                 md5     

## IRC bridge log
	mkdir /var/log/matrix-appservice-irc
	chown matrix-bridge-irc:nogroup /var/log/matrix-appservice-irc

## IRC systemd bridge service
	sudo editor /etc/systemd/system/matrix-appservice-irc.service
	[Unit]
	Description=Matrix AppService IRC

	[Service]
	WorkingDirectory=/usr/lib/node_modules/matrix-appservice-irc
	ExecStart=node app.js -c /etc/matrix-appservice-irc/config.yaml -f /etc/matrix-appservice-irc/my_registration_file.yaml -p 9999
	User=matrix-bridge-irc

	[Install]
	WantedBy=multi-user.target

## modif du /etc/matrix-synapse/homeserver.yaml
	app_service_config_files: ["/etc/matrix-appservice-irc/my_registration_file.yaml"]

## generation du my_registration_file.yaml
	node /usr/lib/node_modules/matrix-appservice-irc/app.js -r -f /etc/matrix-appservice-irc/my_registration_file.yaml -u "http://matrix.fdn.fr:9999" -c /etc/matrix-appservice-irc/config.yaml -l neo

## Pour federer: ajout des DNS (CNAME interdit) 

    matrix                 IN      A       80.67.169.98
                           IN	   AAAA	   2001:910:800::98
    _matrix._tcp.matrix    IN      SRV     10 0 443 matrix

## Script ajout nouvel utilisateur:
	#!/bin/bash
	register_new_matrix_user -c /etc/matrix-synapse/homeserver.yaml http://localhost:8008

## Ajout nouvel utilisateur :
	$matrix_new

## TURN (homeserver.yaml)
	turn_uris: [ "turn:turn.fdn.fr:3478?transport=udp", "turn:turn.fdn.fr:3478?transport=tcp" ]
	turn_shared_secret: "*******************************"

## Reverse proxy (nginx)
	/etc/nginx/sites-enabled/synapse
	server {
		listen 443 ssl;
		listen [::]:443 ssl;
		server_name matrix.fdn.fr;
	
		ssl_certificate /etc/letsencrypt/live/matrix.fdn.fr/fullchain.pem;
		ssl_certificate_key /etc/letsencrypt/live/matrix.fdn.fr/privkey.pem;
		include /etc/ssl/nginx.conf;
	
		location /_matrix {
			proxy_pass http://localhost:8008;
			proxy_set_header X-Forwarded-For $remote_addr;
	# Nginx by default only allows file uploads up to 1M in size
	# Increase client_max_body_size to match max_upload_size defined in homeserver.yaml
			client_max_body_size 50M;
		}
	
		access_log /var/log/nginx/matrix-clients.access.log;
		error_log /var/log/nginx/matrix-clients.error.log;
	}
	
	server {
		listen 8448 ssl default_server;
		listen [::]:8448 ssl default_server;
		server_name matrix.fdn.fr;
	
		ssl_certificate /etc/letsencrypt/live/matrix.fdn.fr/fullchain.pem;
		ssl_certificate_key /etc/letsencrypt/live/matrix.fdn.fr/privkey.pem;
		include /etc/ssl/nginx.conf;
	
		location / {
			proxy_pass http://localhost:8008;
			proxy_set_header X-Forwarded-For $remote_addr;
		}
	
		access_log /var/log/nginx/matrix-federation.access.log;
		error_log /var/log/nginx/matrix-federation.error.log;
	}
	
### Misc
## Test validité certificat depuis client    
	echo | openssl s_client -showcerts -servername matrix.fdn.fr -connect matrix.fdn.fr:443 2>/dev/null | openssl x509 -inform pem -noout -text

Validity Not Before & Not After doivent changer

## Test version depuis client
	curl -kv https://matrix.fdn.fr/_matrix/client/versions 2>&1 | grep "Server:"

# IRC
## users

Il faut bien penser à register + identifier vos 2 users : IRC & Matrix.
Exemple : user blt IRC / user blt[m] matrix

### register un utilisateur IRC (depuis client IRC, ici irssi)
Ouvrir une conversation avec C : /msg C hello

	nick register password email
	Si tout se passe bien vous recevrez : "You are now registered."

### identifier un utilisateur IRC (depuis client IRC, ici irssi)

Ouvrir une conversation avec C : /msg C hello

	nick identify password
	Si tout se passe bien vous recevrez : "You are now identified"

### register un utilisateur matrix[m]

Aller dans un salon bridgé IRC et cliquer sur C dans la liste des membres à droite, puis démarrer un 'Direct Chat'

	nick register password email
	Si tout se passe bien vous recevrez : "You are now registered."

### identifier un utilisateur matrix[m]
Aller dans un salon bridgé IRC et cliquer sur C dans la liste des membres à droite, puis démarrer un 'Direct Chat'

	nick identify password
	Si tout se passe bien vous recevrez : "You are now identified"

### Donner les droits d'administration à un utilisateur (utile pour les requêtes API)
```bash
sudo su -c "psql -c \"UPDATE users SET admin = 1 WHERE name = '@user:matrix.fdn.fr'\" -d synapse" -l postgresu -c "psql -c \"UPDATE users SET admin = 0 WHERE name = '@user:matrix.fdn.fr'\" -d synapse" -l postgres
```

## #fdn-adminsys-internal (Register + Invite Only)
### creation (irssi)
	/join -geeknode #fdn-adminsys-internal

### register le salon
	chan REGISTER #fdn-adminsys-internal

### passer au Register & Invite Only en parlant a C (/msg C)
	chan SET #fdn-adminsys-internal MLOCK +Ri

### admin only : inviter un pseudo ou pseudo[m]
	/invite pseudo #fdn-adminsys-internal
	/invite pseudo[m] #fdn-adminsys-internal

## #fdn-adminsys (Register Only)
### register le salon
	chan REGISTER #fdn-adminsys

### passer au Register Only en parlant a C (/msg C)
	chan SET #fdn-adminsys MLOCK +R

## Bridger une nouvelle room

### Créer/choisir la room IRC: #fdn-name

	/join -geeknode #fdn-name

### Créer/choisir la room matrix (choisir le même nom)

### Nommer la room avec le même nom que le nom IRC dans :
	
	Settings>General>Main address : #fdn-name:matrix.fdn.fr

### Récupérer 'l'Internal room ID' de la room dans :

	Settings>Advanced: !chaineAlphaNum:matrix.fdn.fr

### Changer le paramètre de la room dans Security & Privacy:

	Who can access this room ? anyone who know the room's links inluding guest

### Changer le paramètre de la room dans Security & Privacy :

	Who can read history -> Members only (since they joined)

### Éditer le fichier: /etc/matrix-appservice-irc/config.yaml y ajouter dans la section "mappings:" du serveur irc voulu:

	"#fdn-name":
	roomIds: ["!chaineAlphaNum:matrix.fdn.fr"]

### Regénérer le my_registration_file.yaml:

	node /usr/lib/node_modules/matrix-appservice-irc/app.js -r -f /etc/matrix-appservice-irc/my_registration_file.yaml -u "http://matrix.fdn.fr:9999" -c /etc/matrix-appservice-irc/config.yaml -l matrixbot

### Relancer matrix:

	systemctl restart matrix-synapse.service

### Relancer le bridge

	systemctl restart matrix-appservice-irc

### Réinitialisation du mot de passe

Pour effectuer un _reset_ de mot de passe d'un utilisateur manuellement :

- se connecter à neo.fdn.fr
- calculer le hash du mot de passe
```bash
$ sudo hash_password
Password:
Confirm password:
$2a$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
- mettre à jour la base de données
```bash
$ sudo su - postgres
$ psql
postgres=# \c synapse
postgres=# UPDATE users SET password_hash='$2a$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' WHERE name='@nick:matrix.fdn.fr';
postgres=# \q
```

- ou avec une méthode directe de requête sur la table :
```bash
su -c "psql -c \"UPDATE users SET password_hash='$2a$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' WHERE name='@nick:matrix.fdn.fr'\" -d synapse" -l postgres
```

- ou avec une requête API
être utilisateur "admin" > créer un token > modifier le mot de passe > vérification
```bash
user_url="@admin_user:matrix.fdn.fr"
token=$(curl -k -XPOST -d '{"type":"m.login.password", "user":"$user_url", "password":"'xxxxxxxx'"}' "https://localhost:8448/_matrix/client/r0/login" | jq -r ".access_token")
curl -XPOST -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d '{"new_password":"xxxxxxxx"}' "https://localhost:8448/_matrix/client/r0/admin/reset_password/$user_url"
curl --insecure -XGET -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d '{}' "https://localhost:8448/_synapse/admin/v2/users/$user_url"
```
