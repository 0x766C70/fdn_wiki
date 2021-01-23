====== Gestion de l'espace Web d'un abonné (apache2)======

Tout se passe sur //<nowiki>www.fdn.fr</nowiki>* (*[[adminsys:serveurs:yoda]]//).

## Création

Les règles de création sont les suivantes :
  * *login* formé de la première lettre du prénom et du nom complet. Exemple: le login de *Marcel Dugenou* sera ''mdugenou''
  * *uid* de la forme 10000 + numéro d'adhérent
  * *groupe* www-data
  * *mot de passe* : le même que pour accéder à la section des adhérents sur vador

Il faut donc se connecter au [[https://vador.fdn.fr/private|SI de FDN]] pour récupérer le numéro d'adhérent et le mot de passe puis, sur yoda, créer le compte correspondant. Reprenons l'exemple de notre ami Marcel, si son numéro d'adhérent est 666 ça donne ceci :

    <code>yoda$ sudo adduser --ingroup www-data --uid 10666 --gecos "Marcel Dugenou" mdugenou</code>


Après nous avoir demandé le mot de passe, ''adduser'' va créer le compte et copier dedans le contenu de ''/etc/skel'' (donc on n'a rien d'autre à faire).

Les répertoires ''~mdugenou/WWW'' et ''~mdugenou/WWWS'' correspondent respectivement à http://www.fdn.fr/~mdugenou/ et https://www.fdn.fr/~mdugenou/.

Une fois le compte créé, retourner dans le [[https://vador.fdn.fr/private|SI]] et ajouter le compte Unix ("afficher un client", "infos techniques", puis "ajouter" à côté de "Utilisateurs Unix"). Un jour, l'ajout dans le SI provoquera la création réelle du compte, pour l'instant c'est juste à titre d'information.

## Changement de mot de passe

L'adhérent peut changer lui-même son mot de passe : ''ssh yoda'' et ''passwd'', tout simplement.

> L'authentification par mot de passe pour ssh est désactivée donc à moins que l'on ai configuré le compte de la personne avec sa clé publique... ça ne marchera pas.
> --- //[[olb@nebkha.net|Olivier Le Brouster]] 02/07/2011 15:12//

## Pour héberger un ou plusieurs domaines

Pour chaque domaine, il faut :
  * créer un répertoire ''~mdugenou/WWW-domaine''
  * créer (ou modifier) le fichier ''/etc/apache2/sites-available/membres/mdugenou/domaine''
  * faire un lien symbolique et faire en sorte qu'apache relise la configuration. 

Par exemple, pour héberger le domaine ''www.dugenou.fr''

    <code>sudo -u mdugenou mkdir WWW-dugenou.fr
    cd /etc/apache2
    sudo mkdir -p sites-available/membres/mdugenou
    sudo mkdir -p sites-enabled/membres/mdugenou
    sudo vim sites-available/membres/mdugenou/www.dugenou.fr
    sudo ln -s /etc/apache2/sites-available/membres/mdugenou/www.dugenou.fr /etc/apache2/sites-enabled/membres/mdugenou/www.dugenou.fr
    </code>


Le fichier sites-available/membres/mdugenou/www.dugenou.fr contiendra quelquechose de ce genre :

    <code><VirtualHost *:80>
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
    </VirtualHost></code>


## Les différents accès

#### FTP

L'utilisateur peut accéder à son compte via le protocole ftp. Néanmoins ce n'est pas conseillé pour des raisons de sécurité (à moins qu'il utilise le mode tls).

#### SSH

Si le compte a été configuré pour permettre l'authentification par clé (~/.ssh/authorized_keys), la personne peut accéder à sont compte via SSH ou sftp.

