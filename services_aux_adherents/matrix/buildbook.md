# Buildbook

## Installation Synapse

FDN est parti sur la mise en place d'une instance [Synapse](https://github.com/matrix-org/synapse/).

### Installation paquet

La conf puppet descend sur la machine le repo matrix automatiquement.

Néanmoins au cas où, voici le process proposé sur la page install du projet synapse

    sudo apt install -y lsb-release wget apt-transport-https
    sudo wget -O /usr/share/keyrings/matrix-org-archive-keyring.gpg https://packages.matrix.org/debian/matrix-org-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/matrix-org-archive-keyring.gpg] https://packages.matrix.org/debian/ $(lsb_release -cs) main" |
        sudo tee /etc/apt/sources.list.d/matrix-org.list
    sudo apt update
    sudo apt install matrix-synapse-py3


**en root**

### Certbot

    apt-get install certbot
    certbot certonly --standalone
    Enter email address (used for urgent renewal and security notices) (Enter 'c' to cancel): admin@fdn.fr
    (A)gree/(C)ancel: A
    (Y)es/(N)o: N
    Please enter in your domain name(s) (comma and/or space separated)  (Enter 'c' to cancel): matrix.fdn.fr

### Synapse PostgreSQL

    systemctl stop puppet
    deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    apt-get update
    apt install postgresql-9.6
    su - postgres
    createdb synapse
    createuser --pwprompt synapse_user
    psql
      CREATE DATABASE synapse ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' template=template0 OWNER synapse_user;
	  \q

Dans /etc/postgresql/9.6/main/pg_hba.conf ajout à la fin:

    host    synapse         synapse_user    ::1/128                 md5

### Creation du dh

    mkdir /etc/ssl/dh
    openssl dhparam -out /etc/ssl/dh/matrix.fdn.fr.pem -5 4096

### Demarage de synapse 

    systemctl start matrix-synapse

## Installation Bridge

Nous sommes parti sur le bridge [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc).

### Installation paquet

    curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
    apt-get install -y nodejs make gcc build-essential node-typescript
    adduser --system  matrix-bridge-irc
    mkdir -p /usr/lib/node_modules/matrix-appservice-irc/bin/matrix-appservice-irc
    ln -s /usr/lib/node_modules/matrix-appservice-irc/bin/matrix-appservice-irc /usr/bin/matrix-appservice-irc
    chown -R matrix-bridge-irc: /usr/lib/node_modules/ 

Dans /etc/passwd ajouter à la fin

    matrix-bridge-irc:x:116:65534::/home/matrix-bridge-irc:/bin/bash
    
    su - matrix-bridge-irc
	npm install matrix-appservice-irc --global
	cd /usr/lib/node_modules/matrix-appservice-irc
	npm install
	npm test

### IRC bridge PostgreSQL
	su - postgres
	createuser --pwprompt irc_bridge_db_user
	psql
	  CREATE DATABASE irc_bridge_db ENCODING 'UTF8'	LC_COLLATE='C' LC_CTYPE='C' template=template0 OWNER irc_bridge_db_user;
	  \q

Dans /etc/postgresql/9.6/main/pg_hba.conf ajout à la fin:

    host    irc_bridge_db   irc_bridge_db_user    ::1/128                 md5 

### IRC bridge log
	mkdir /var/log/matrix-appservice-irc
	chown matrix-bridge-irc:nogroup /var/log/matrix-appservice-irc

### IRC systemd bridge service

    vim/etc/systemd/system/matrix-appservice-irc.service

    [Unit]
    Description=Matrix AppService IRC
    [Service]
    WorkingDirectory=/usr/lib/node_modules/matrix-appservice-irc
    ExecStart=node app.js -c /etc/matrix-appservice-irc/config.yaml -f /etc/matrix-appservice-irc/my_registration_file.yaml -p 9999
    User=matrix-bridge-irc
    [Install]
    WantedBy=multi-user.target


### Pour federer: ajout des DNS (CNAME interdit) 

    matrix                 IN      A       80.67.169.98
                           IN	   AAAA	   2001:910:800::98
    _matrix._tcp.matrix    IN      SRV     10 0 443 matrix
    
### Reverse proxy nginx

    apt install nginx
    
Dans /etc/nginx/sites-enabled/synapse

    server {
    	listen 443 ssl;
    	listen [::]:443 ssl;
    	server_name matrix.fdn.fr;
    	ssl_certificate /etc/letsencrypt/live/matrix.fdn.fr/fullchain.pem;
    	ssl_certificate_key /etc/letsencrypt/live/matrix.fdn.fr/privkey.pem;
    	location /_matrix {
    		proxy_pass http://localhost:8008;
    		proxy_set_header X-Forwarded-For $remote_addr;
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
    	location / {
    		proxy_pass http://localhost:8008;
    		proxy_set_header X-Forwarded-For $remote_addr;
    	}

    	access_log /var/log/nginx/matrix-federation.access.log;
    	error_log /var/log/nginx/matrix-federation.error.log;
    }

    systemctl restart nginx

### Lier le bridge à l'instance synapse

Ajouter dans /etc/matrix-synapse/homeserver.yaml

    app_service_config_files: ["/etc/matrix-appservice-irc/my_registration_file.yaml"]

### Generation du my_registration_file.yaml

Ce fichier "compile" la config du bridge pour la donner en lecture à synapse
 
	node /usr/lib/node_modules/matrix-appservice-irc/app.js -r -f /etc/matrix-appservice-irc/my_registration_file.yaml -u "http://matrix.fdn.fr:9999" -c /etc/matrix-appservice-irc/config.yaml -l neo
