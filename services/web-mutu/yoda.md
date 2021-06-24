[[_TOC_]]

FDN fournissait historiquement à ses membres de l'hébergement de site web sur yoda.
Ce service a été migré vers une nouvelle machine, rey, et le processus de migration est en cours. Il est donc possible de trouver des sites sur les deux machines.

[yoda](./infra/machines/yoda.md) correspond au domaine web.fdn.fr.

Les technos supportées sont :

- Languages : PHP / Perl et autre CGI
- SGBD : mysql

Si le membre n'a pas de domaine, il est possible d'héberger un site sur http(s)://web.fdn.fr/~user/ ou http(s)://login.fdn.fr/.

FDN fourni également un outil de statistiques.


# Procédures

## Création d'un espace web

Les règles de création sont les suivantes :

  * *login* formé de la première lettre du prénom et du nom complet. Exemple:
    le login de *Marcel Dugenou* sera ``mdugenou``
  * *uid* de la forme 10000 + numéro d'adhérent
  * *groupe* www-data
  * *mot de passe* : le même que pour accéder à la section des adhérents sur
    vador

Il faut donc se connecter au [SI de FDN](https://vador.fdn.fr/private) pour
récupérer le numéro d'adhérent et le mot de passe puis, sur yoda, créer le
compte correspondant. Reprenons l'exemple de notre ami Marcel, si son numéro
d'adhérent est 666 ça donne ceci :

    yoda$ sudo adduser --ingroup www-data --uid 10666 --gecos "Marcel Dugenou" mdugenou

Après nous avoir demandé le mot de passe, ``adduser`` va créer le compte et
copier dedans le contenu de ``/etc/skel`` (donc on n'a rien d'autre à faire).

Les répertoires ``~mdugenou/WWW`` et ``~mdugenou/WWWS`` correspondent respectivement à http://www.fdn.fr/~mdugenou/ et https://www.fdn.fr/~mdugenou/.

Une fois le compte créé, retourner dans le [SI](https://vador.fdn.fr/private)
et ajouter le compte Unix ("afficher un client", "infos techniques", puis
"ajouter" à côté de "Utilisateurs Unix"). Un jour, l'ajout dans le SI
provoquera la création réelle du compte, pour l'instant c'est juste à titre
d'information.

## Changement de mot de passe

L'adhérent peut changer lui-même son mot de passe : ``ssh web.fdn.fr`` et
``passwd``, tout simplement. Cela nécessite que la clé SSH de la personne en
question ait été rajouté dans son compte.

## Pour héberger un ou plusieurs domaines

Pour chaque domaine, il faut :

  * créer un répertoire ``~mdugenou/WWW-domaine``
  * créer (ou modifier) le fichier ``/etc/apache2/sites-available/membres/mdugenou/domaine``
  * faire un lien symbolique et faire en sorte qu'apache relise la configuration. 

Par exemple, pour héberger le domaine ``www.dugenou.fr``

    sudo -u mdugenou mkdir WWW-dugenou.fr
    cd /etc/apache2
    sudo mkdir -p sites-available/membres/mdugenou
    sudo mkdir -p sites-enabled/membres/mdugenou
    sudo vim sites-available/membres/mdugenou/www.dugenou.fr
    sudo ln -s /etc/apache2/sites-available/membres/mdugenou/www.dugenou.fr /etc/apache2/sites-enabled/membres/mdugenou/www.dugenou.fr


Le fichier sites-available/membres/mdugenou/www.dugenou.fr contiendra
quelquechose de ce genre :

    <VirtualHost *:80>
        ServerAdmin marcel@dugenou.fr
        DocumentRoot /home/mdugenou/WWW-dugenou.fr
        AssignUserId mdugenou www-data
        
        ServerName www.dugenou.fr
        ServerAlias dugenou.fr
        
        RewriteEngine on
        RewriteCond %{SERVERNAME} !^www\.dugenou\.fr$
        RewriteRule (.*) http://www.dugenou.fr$1
        
        ErrorLog /home/mdugenou/log/errors-www.dugenou.fr.log
        CustomLog /home/mdugenou/log/access-www.dugenou.fr.log combined
    </VirtualHost>


## Les différents accès

### FTP

L'utilisateur peut accéder à son compte via le protocole ftp. Néanmoins ce
n'est pas conseillé pour des raisons de sécurité (à moins qu'il utilise le mode
tls).

### SSH

Si le compte a été configuré pour permettre l'authentification par clé
(~/.ssh/authorized_keys), la personne peut accéder à sont compte via SSH ou
sftp.

### Statistiques

TODO: à documenter


# Mise en place initiale

## Répertoires utilisés

### Configuration globale

  * **/etc/apache2/conf.d/** : ce répertoire contient des fichiers de configuration qui sont appliquées à l'ensemble du service apache.

### Gestion des sites

répertoire racine de l'ensemble des sites disponibles 

  * **/etc/apache2/sites-available/** : répertoire contenant l'ensemble des site disponibles pour le service apache.
  * **/etc/apache2/sites-available/autres/** : répertoire contenant les fichiers de configuration de sites "autres" :)
  * **/etc/apache2/sites-available/fdn/** : répertoire dédié aux fichiers de configuration des sites de l'association (et également des sites en www.fdn.fr/~user/)
  * **/etc/apache2/sites-available/membres/** : répertoire dédié aux fichiers de configuration des sites des membres ayant un VirtualHost dédié. Chaque membre dispose d'un répertoire nominatif contenant les différents VirtualHost qu'il gère.

        /etc/apache2/sites-available/membres/
        ├── username
        │   └── www.domain.net

Pour activer un site il faut utiliser la commande a2ensite (a2dissite pour désactiver) puis recharger le service apache2. Une fois le site activé on observe qu'un lien symbolique est créé dans le répertoire **/etc/apache2/sites-enabled/** :

    yoda:~$ ls -l /etc/apache2/sites-enabled/fdn/
    lrwxrwxrwx 1 root root 37  8 mai    2011 blog -> /etc/apache2/sites-available/fdn/blog
    lrwxrwxrwx 1 root root 39  8 mai    2011 compta -> /etc/apache2/sites-available/fdn/compta
    lrwxrwxrwx 1 root root 37  8 mai    2011 fdn2 -> /etc/apache2/sites-available/fdn/fdn2
    ...


## Gestion des modules

L'ensemble des modules disponibles est présent dans le répertoire **/etc/apache2/mods-available/**

Pour activer un module on utilise a2enmod (a2dismod pour désactiver) puis recharger le service apache2. Une fois le site activé on observe qu'un lien symbolique est créé dans le repertoire /etc/apache2/mods-enabled/ :

## Gestion des logs

Les logs relatifs aux sites FDN sont stockés ici :

    /var/log/apache2/

On trouve également les traces des sites n'ayant pas fixés leur propre gestion de logs. ces dernières sont stockées dans des fichiers ``other_vhosts_access.log``.

la rotation de l'ensemble des fichiers *.log contenue dans le repertoire ``/var/log/apache2/`` est assurée ici :

    yoda:~$ cat /etc/logrotate.d/apache2
    /var/log/apache2/*.log {
        daily
        missingok
        rotate 370
        compress
        delaycompress
        notifempty
        create 640 root www-data
        sharedscripts
        postrotate
            /etc/init.d/apache2 reload > /dev/null
        endscript
    }
