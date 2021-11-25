# Buildbook

FDN est parti sur la mise en place d'une instance [Synapse](https://github.com/matrix-org/synapse/) avec un bridge [IRC](https://github.com/matrix-org/matrix-appservice-irc).

** en root **

## Préparation Postgrès

Postgrès 14 est installé par puppet: il reste à créer les users et les bases:

    su - postgres
    createdb synapse
    createdb irc_bridge_db
    createuser --pwprompt synapse_user
    createuser --pwprompt irc_bridge_db_user
    psql                                                                                                         
      CREATE DATABASE synapse       ENCODING 'UTF8' LC_COLLATE='C' LC_CTYPE='C' template=template0 OWNER synapse_user;
      CREATE DATABASE irc_bridge_db ENCODING 'UTF8' :C_COLLATE='C' LC_CTYPE='C' template=template0 OWNER irc_bridge_db_user;
    \q

## Installations paquets

Puppet descend sur la machine l'application synapse, le bridge ainsi que les fichiers de conf

## Finalisation conf Synapse

### Mise en place de certbot pour le https

    apt-get install certbot
    certbot certonly --standalone
    Enter email address (used for urgent renewal and security notices) (Enter 'c' to cancel): admin@fdn.fr
    (A)gree/(C)ancel: A
    (Y)es/(N)o: N
    Please enter in your domain name(s) (comma and/or space separated)  (Enter 'c' to cancel): matrix.fdn.fr

### Creation du dh

    mkdir /etc/ssl/dh
    openssl dhparam -out /etc/ssl/dh/matrix.fdn.fr.pem -5 4096

### Pour federer: ajout des DNS (CNAME interdit) 

    matrix                 IN      A       80.67.169.98
                           IN      AAAA    2001:910:800::98
    _matrix._tcp.matrix    IN      SRV     10 0 443 matrix

## Finalisation conf bridge

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

### IRC bridge log
	mkdir /var/log/matrix-appservice-irc
	chown matrix-bridge-irc:nogroup /var/log/matrix-appservice-irc

## Generation du my_registration_file.yaml

Ce fichier "compile" la config du bridge pour la donner en lecture à synapse
 
	node /usr/lib/node_modules/matrix-appservice-irc/app.js -r -f /etc/matrix-appservice-irc/my_registration_file.yaml -u "http://matrix.fdn.fr:9999" -c /etc/matrix-appservice-irc/config.yaml -l neo

## restart

Redémarrer synapse puis le bridge
