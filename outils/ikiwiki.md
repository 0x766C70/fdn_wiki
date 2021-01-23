[[!meta title="Wiki adminsys: Y accéder et y contribuer"]]
*Remarque:* Il faudrait diviser cette page en plusieurs dans le dossier `ikiwiki` pour plus de lisibilité.
Le wiki adminsys est hébergé sur la machine [[infra/machines/obiwan]]. Tous les
membres de FDN peuvent lire ce wiki, en revanche, seulement l'équipe adminsys
peut l'éditer.

Le wiki adminsys est rédigé en Markdown. Voir les bases sur le site officiel à
l'adresse <https://daringfireball.net/projects/markdown/basics>.

[[!toc levels=2]]

Procédures
==========

Accéder à adminsys.fdn.fr
-------------------------

Simplement en allant à l'adresse <https://adminsys.fdn.fr/> avec votre
navigateur préféré. Un couple login/mot de passe est demandé ; il s'agit du
couple addhac-xxxxxxx / secret .

Contribuer au wiki
------------------
Ce wiki fonctionne avec ikiwiki branché sur le dépôt git `obiwan.fdn.fr:/srv/repositories/adminsys.git`. Explications dans [[git_tuto]]
# via ssh

## Gestion des comptes ssh

Les membres du groupe adminsys sur obiwan ont les droits en lecture/ecriture.

## Gestion des comptes web

### Authentifications

  - via radius (login adhacc-42)
  - `/srv/ikiwiki/htpassd`

### Authorisations

Par défaut, toutes les pages sont protégées en écriture, seuls les admin du
wiki ou les utilisateurs spécifiés dans la conf peuvent modifier le wiki.

  - variable `adminuser` dans le fichier `/srv/ikiwiki/wiki.setup`.

  - variable `locked_page` dans le fichier `/srv/ikiwiki/wiki.setup`

    Exemple :

        locked_page: '* and !user(adhac-334)'

## Installation web locale

### <a name="copie_depot"></a>Copie du dépôt

Les membres du groupe adminsys sur la machine [[infra/machines/obiwan]] peuvent
contribuer au site. Ils ont en effet les droits sur le dépôt
`/srv/repositories/adminsys.git`.

On commence par cloner le dépôt :

    git clone login@obiwan.fdn.fr:/srv/repositories/adminsys.git fdn-adminsys

Les sources du wiki sont dans le répertoire *wiki* du dépôt `fdn-adminsys`.

Pour de l'aide sur les commandes git voir:
[[!map pages="howto/git*" show="title"]]


### Installation de paquets Debian nécessaires

À coup de ligne de commande :

    aptitude install --without-recommends \
        ikiwiki libtext-markdown-perl libimage-magick-perl git-core \
        libsearch-xapian-perl

Cette documentation part du principe que Apache est déjà installé. Si ce n'est
pas le cas, vous avez le choix entre installer apache ou utiliser un autre
serveur web. Cette documentation explique comment faire avec apache ou nginx.

### Configuration d'Apache

Première étape, on installe apache :

    aptitude install --without-recommends apache2

Cette documentation utilise la fonction « userdir » :

    a2enmod userdir

Cela rend le dossier `public_html` accessible à l'adresse
`http://localhost/~user/`.

Il est également nécessaire de modifier
`/etc/apache2/mods-available/userdir.conf` pour y lire :

    <Directory /home/*/public_html>
        AllowOverride All

Cela permet de configurer le répertoire dans lequel se trouvera le wiki plus
facilement, sans avoir à devenir _root_.

### Configuration avec nginx

Si vous avez fait la section précédente, il n'est pas nécessaire de suivre
celle-là, c'est juste une alternative. De plus, nginx ne sait pas fonctionner
avec des fichiers d'autoristation `.htaccess`, il faut donc impérativement
limiter l'accès via la conf de nginx aux IPs voulues (typiquement, 127.0.0.1 et
::1).

Premièrement, installer les paquets nécessaires :

    apt-get install nginx fcgiwrap

Deuxièmement, configurer le VirtualHost, par exemple dans
`/etc/nginx/sites-available/fdn-adminsys` :

        server {
            listen   127.0.0.1:80; ## listen for ipv4; this line is default and implied
            listen   [::1]:80;
            include /etc/nginx/fcgiwrap.conf;
            server_name localhost;
            root /home/<USER>/public_html;
            autoindex on;
            location /nginx_status {
                stub_status on;
                access_log   off;
                allow 127.0.0.1;
                deny all;
            }
            location / {
            }
            location /images {
                root /usr/share;
                autoindex off;
            }
            location ~ ikiwiki\.cgi$ {
                fastcgi_pass   unix:/var/run/fcgiwrap.socket;
                fastcgi_param  SCRIPT_FILENAME  /home/<USER>/public_html/fdn-adminsys$fastcgi_script_name;
            }
            location ~ /\.ht {
                deny all;
            }
        }

Puis faire un lien vers ce fichier dans `/etc/nginx/sites-enabled/fdn-adminsys` :

        # ln -s /etc/nginx/sites-available/fdn-adminsys /etc/nginx/sites-enabled/fdn-adminsys

Enfin, configurer fcgiwrap pour servir les pages ikiwiki, selon la
[documentation sur le site de nginx](http://wiki.nginx.org/Fcgiwrap).

Redémarrer nginx.


### Configuration d'ikiwiki en local

Afin d'avoir une version locale « _compilée_ » du wiki (donc sous forme de
pages web, que le serveur web que nous avons installé pourra servir), il est
nécessaire d'utiliser un fichier de configuration propre à ikiwiki. Le fichier
`doc.setup` peut normalement servir tel quel, sauf si les répertoires sont
différents.

Si tout va bien, il suffit ensuite d'effectuer les commandes suivantes pour
compiler le wiki :

    ~/fdn/adminsys$ mkdir -p ~/public_html/fdn-adminsys
    ~/fdn/adminsys$ eval "echo \"$(cat wiki.setup.template)\"" > wiki.setup
    ~/fdn/adminsys$ ikiwiki --setup wiki.setup

En visitant l'adresse http://localhost/~USER/fdn-adminsys/ on doit déjà pouvoir
naviguer dans le wiki.

### Protection et configuration du site

Il est ensuite nécessaire de configurer :

 * l'exécution du CGI
 * la protection de l'accès au site à des personnes extérieurs (via le réseau,
   vu qu'il est sur un serveur web).

Grâce à la directive `AllowOverride All` de tout à l'heure, cela se fait par
l'intermédiaire d'un fichier `~/public_html/fdn-adminsys/.htaccess`.
Son contenu se trouve dans le fichier [[htaccess]]. Il est nécessaire de
remplacer `USER` par le _login_ utilisé (impossible avec nginx).

Pour la création des comptes, on fait :

    ~/fdn-adminsys$ htpasswd -c ~/public_html/fdn-adminsys/htpasswd USER


# Mise en place

- `/srv/ikiwiki/html` : build html du wiki servi par apache
- `/srv/ikiwiki/repo` : clone ikiwiki du dépôt git

## ikiwiki

Installation des paquets

    sudo aptitude install --with-recommends ikiwiki
    sudo aptitude install libsearch-xapian-perl xapian-omega libhtml-tree-perl \
        perlmagick liblocale-gettext-perl libtext-typography-perl \
        libsort-naturally-perl libhighlight-perl po4a gettext \
        libtext-multimarkdown-perl libxml-writer-perl libmagickcore-extra

On a un utilisateur spécifique pour ikiwiki

    sudo adduser ikiwiki --home /srv/web/ikiwiki --disabled-password
    sudo adduser ikiwiki adminsys

Ikiwiki travaille dans un clone du dépôt adminsys

    sudo -u ikiwiki git clone /srv/repositories/adminsys.git /srv/web/ikiwiki/repo

Le fichier de conf du wiki de trouve dans `/srv/ikiwiki/wiki.setup`. La racine
d'ikiwiki se trouve dans le répertoire `wiki` du dépôt git adminsys.

    cp /etc/ikiwiki/auto.setup /srv/web/ikiwiki/wiki.setup
    vim /srv/web/ikiwiki/wiki.setup

## apache2

Points clés : itk, auth radius, ssl, cgi. Cf
`/etc/apache2/site-available/adminsys.fdn.fr.conf` sur obiwan.

## authentification radius

Pour l'authentification radius, on utilise le module
`libapache2-mod-auth-radius`. Il se trouve qu'il n'existe pas dans la version
jessie de Debian. Nous l'avons donc
[[backporté|howto/backporter_un_paquet_debian]].

L'authentification est donc faite contre le [[outils/si]] qui a été modifié
pour l'occasion.

# Remarques sur la syntaxe Markdown : #
* Il y a des explications specifiques à Ikiwiki [ici](http://ikiwiki.info/ikiwiki/);
* [Une page détaillée sur la syntaxe Markdown](https://daringfireball.net/projects/markdown/syntax);
* Il y a deux façons de faire les titres: `Setext` ou `atx`. Très étrange, le second, qui permet six niveaux, ne fonctionne pas toujours... Déjà que Markdown est plutôt limité(notamment concernant les listes)...
