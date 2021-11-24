# Buildbook

## Installation Synapse

FDN est parti sur la mise en place d'une instance [Synapse](https://github.com/matrix-org/synapse/).

### Installation paquet

Puppet descend sur la machine le repo matrix automatiquement ainsi que son install & fichier de conf.

**en root**

### Certbot

    apt-get install certbot
    certbot certonly --standalone
    Enter email address (used for urgent renewal and security notices) (Enter 'c' to cancel): admin@fdn.fr
    (A)gree/(C)ancel: A
    (Y)es/(N)o: N
    Please enter in your domain name(s) (comma and/or space separated)  (Enter 'c' to cancel): matrix.fdn.fr

### Postgres

Puppet descend sur la machine le repo Postgres et install Postgres 14. Il reste à créer le user et la table synapse:

    su - postgres
    createdb synapse
    createuser --pwprompt synapse_user
    psql
      CREATE DATABASE synapse ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' template=template0 OWNER synapse_user;
	  \q

Dans /etc/postgresql/14/main/pg_hba.conf ajout à la fin:

    host    synapse         synapse_user    ::1/128                 md5

### Creation du dh

    mkdir /etc/ssl/dh
    openssl dhparam -out /etc/ssl/dh/matrix.fdn.fr.pem -5 4096

### Demarage de synapse 

    systemctl start matrix-synapse

## Installation Bridge

Nous sommes parti sur le bridge [matrix-appservice-irc](https://github.com/matrix-org/matrix-appservice-irc).

### Installation paquet

Pupper descend les paquets necessaires au bridge et l'installe. On va créer un user pour le bridge:

    adduser --system  matrix-bridge-irc
    mkdir -p /usr/lib/node_modules/matrix-appservice-irc/bin/matrix-appservice-irc
    ln -s /usr/lib/node_modules/matrix-appservice-irc/bin/matrix-appservice-irc /usr/bin/matrix-appservice-irc
    chown -R matrix-bridge-irc: /usr/lib/node_modules/ 

Dans /etc/passwd ajouter à la fin

    matrix-bridge-irc:x:116:65534::/home/matrix-bridge-irc:/bin/bash
    
    su - matrix-bridge-irc
    cd /usr/lib/node_modules/matrix-appservice-irc
    npm install
    npm test

### Postgres

On crée le user et la table pour le bridge:

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

(à mettre dans Puppet ?)

### Pour federer: ajout des DNS (CNAME interdit) 

    matrix                 IN      A       80.67.169.98
                           IN	   AAAA	   2001:910:800::98
    _matrix._tcp.matrix    IN      SRV     10 0 443 matrix
    
### Reverse proxy nginx

*Puppet descend l'install de nginx et son fichier de conf*

Il faut néanmoins ajouter dans /srv/http/.well-known/synapse/

* un fichier: client

    {
      "m.homeserver": {
        "base_url": "https://matrix.fdn.fr"
      }
    }

* un fichier: server

    {
      "m.server": "matrix.fdn.fr:443"
    }


### Generation du my_registration_file.yaml

Ce fichier "compile" la config du bridge pour la donner en lecture à synapse
 
	node /usr/lib/node_modules/matrix-appservice-irc/app.js -r -f /etc/matrix-appservice-irc/my_registration_file.yaml -u "http://matrix.fdn.fr:9999" -c /etc/matrix-appservice-irc/config.yaml -l neo

### restart

Redémarrer synapse puis le bridge
