
# Web public de FDN

L'hébergement Web FDN est effectué par [chewie](http://chewie.fdn.fr/) ([*](./infra/machines/chewie.md))

Les services actuellement hébergés sont :

  * Site Web de fdn ( [https://www.fdn.fr](https://www.fdn.fr) et [https://www-devel.fdn.fr](https://www-devel.fdn.fr))
  * Blog de fdn ([https://blog.fdn.fr](https://blog.fdn.fr) et [https://blog-devel.fdn.fr](https://blog-devel.fdn.fr))

L'équipe communication est autonome pour héberger la partie hébergement Web des sites Web de FDN.

Cette page a pour but de documenter l'hébergement des sites web [fdn.fr](https://www.fdn.fr/) et [blog.fdn.fr](https://blog.fdn.fr/) sur la machine virtuelle [chewie](http://chewie.fdn.fr/).

## Caractéristiques de l'hébergement

### Deux versions : développement (xxx-devel) et production (xxx-prod)

Chaque service est hébergé en deux instances : production (identifiée xxx-prod) / développement (identifiée xxx-devel) ; "xxx" représentant le nom du service (exemple www, blog, ...))

Chaque instance dispose de sa branche :

  * master - la branche stable censée être sur xxx.fdn.fr
  * develop - la branche sur laquelle on développe, censée être sur xxx-devel.fdn.fr

Arborescence choisie est la suivante :

    /srv/
    └── web
        ├── xxx-devel
        │   └── repo
        │       ├── examples
        │       ├── scripts
        │       └── www
        └── xxx-prod
            └── repo
                ├── examples
                ├── scripts
                └── www

Description des répertoires :

  * www/ (le répertoire servi par le serveur web)
  * scripts/ (des scripts pour récupérer les fichiers variables et la base de données
  * examples/ (exemples de configuration)

Exemple :

  * site Web de FDN en [production](https://www.fdn.fr/) ; est hébergé dans /srv/web/www-prod
  * site Web de FDN en [développement](https://www-devel.fdn.fr/) ; est hébergé dans /srv/web/www-devel

Les sites web en production sont calés sur la branche master.

Les sites web en développement sont calés sur la branche develop et protégés par un htaccess.

### Application en lecture seule autant que possible

Nous utilisons des outils ultra connus qui évoluent en permanence (wordpress et dotclear), et dont il est probable que nous n'arrivions pas à suivre les mises à jour de sécurité pour diverses raisons.
Une des manières de sécuriser l'hébergement de tels outils est de ne pas permettre à l'application de se modifier elle-même.

Cela se caractérise par l'utilisation de deux utilisateurs pour l'hébergement :

  * un utilisateur pour faire tourner le php, avec seulement le droit le lire/exécuter le code source, et d'écrire dans des répertoires variables donnés (dans lesquels le php n'est pas exécutable).
  * un utilisateur qui a les droits de modification du code source.

Cela ne nous dispense bien évidement pas de mettre à jour les appli...

Pour faire en sorte qu'un répertoire donné puisse être modifié par PHP, exécuter la commande suivante:

    $ sudo chmod g+w -R /srv/web/xxx-xxx/www/chemin/du/repertoire

Penser ensuite à désactiver l'exécution de php sur ce répertoire dans la configuration apache :

    <Directory /srv/web/xxx-xxx/www/chemin/du/repertoire>
        php_admin_value engine Off
    </Directory>

## Procédures

### Installer le site web sur sa machine

    REPO_URL=git@git.fdn.fr:communication/www.git
    REPO_DIR="$(pwd)/fdn-www"
    REPO_BRANCH="develop"    # ou "master"
    MYSQL_PASSWORD=secret
    MYSQL_USER=fdn-www
    MYSQL_DATABASE=fdn-www

    git clone "$REPO_URL" "$REPO_DIR"
    git checkout "$REPO_BRANCH"

    # Création de la base de donnée
    mysql -u root -p -c "CREATE DATABASE $MYSQL_DATABASE"
    mysql -u root -p -c "GRANT ALL ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'localhost' IDENTIFIED BY '$MYSQL_PASSWORD'"

    # Configuration de wordpress
    cp examples/wp-config.php www/wp-config.php
    editor www/wp-config.php

    # Configuration d'apache
    cp ./examples/apache2-vhost /etc/apache2/sites-available/fdn-www.conf
    editor /etc/apache2/sites-available/fdn-www.conf
    sudo a2ensite fdn-www.conf
    sudo apache2ctl contigtest
    sudo service apache2 restart


### Mettre à jour son instance à partir de chewie

    # Sources
    git pull

    # Récupérer la base de données
    ./scripts/fetch-db

    # Récupérer les fichiers variables
    ./scripts/fetch-files



## Installation

L'idée c'est d'avoir un utilisateur web-admin qui est propriétaire des sites web et un utilisateur par site pour le faire tourner.

### Créer un nouveau service

    WSERVICE_NAME="xxx-prod"
    sudo adduser --home /srv/web/$WSERVICE_NAME/ --disabled-password --gecos $WSERVICE_NAME $WSERVICE_NAME
    sudo adduser web-admin $WSERVICE_NAME
    sudo -u $WSERVICE_NAME mkdir /srv/web/$WSERVICE_NAME/repo/{examples,scripts,www}
    sudo chown -R web-admin /srv/web/$WSERVICE_NAME
    sudo chmod o-rwx /srv/web/$WSERVICE_NAME
    sudo adduser --home /srv/web/ --disabled-password --gecos web-admin web-admin
    sudo chown web-admin: -R /srv/web/
    sudo chmod o-rwx -Rf /srv/web/
    sudo adduser --home /srv/web/$WSERVICE_NAME --disabled-password --gecos $WSERVICE_NAME $WSERVICE_NAME
    sudo adduser www-data $WSERVICE_NAME
    sudo adduser web-admin $WSERVICE_NAME

### Détails pour les différents services
#### www.fdn.fr

    # Les utilisateurs
    sudo adduser --home /srv/web/www-prod/ --disabled-password --gecos www-prod www-prod
    sudo adduser web-admin www-prod
    sudo adduser www-data www-prod
    chown -R web-admin /srv/web/www-prod
    chmod o-rwx /srv/web/www-prod

    # Les sources
    sudo -u web-admin -g www-prod -i
    git clone git@git.fdn.fr:communication/www repo
    chmod g+rwxs repo/www/wp-content/uploads
    chmod g+rwxs repo/www/wp-content/cache
    exit

    # Configuration de la base de données
    DB_USER=www-prod
    DB_NAME=www-prod
    DB_PASS=secret
    mysql -u root -p -c "CREATE DATABASE $DB_NAME"
    mysql -u root -p -c "GRANT ALL ON $DB_NAME.* TO '$DB_USER'@'localhost' IDENTYFIED BY '$DB_PASS'"

    sudo -u web-admin -g www-prod -i
    cd /srv/web/www-prod
    echo '[client]
    user=$DB_USER
    host=localhost
    password=$DB_PASS
    ' > /srv/web/www-prod/.my.cnf
    exit


## Mettre à jour le site Wordpress

### Mettre à jour www.fdn.fr sur chewie

Son compte sur chewie doit être capable d'exécuter des commandes en tant que www-prod via sudo.

* Se connecter à chewie :

    sudo -u web-admin -g www-prod -i
    cd /srv/web/www-prod/repo
    git pull
    exit

* Ouvrir le site web dans son navigateur.

### Mettre à jour www-devel.fdn.fr sur chewie 
Son compte sur chewie doit être capable d'exécuter des commandes en tant que www-devel via sudo.

* Se connecter à chewie :

    sudo -u web-admin -g www-devel -i
    cd /srv/web/www-devel/repo
    git pull
    exit

* Ouvrir le site web dans son navigateur.
