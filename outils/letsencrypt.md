
# Let's encrypt

Nous utilisons [Let's encrypt](https://letsencrypt.org)  pour nos
certificats X.509, et plus spécifiquenent le client [[acme_tiny/acme_tiny.py]],
disponible sur [github](https://github.com/diafygi/acme-tiny), dont la
documentation est [[acme_tiny/README]].

Les certificats Let's encrypt ont besoin d'être renouvelés au minimum tous les
90 jours.

Le script de renouvellement tourne chaque jour et vérifie que les certificats
expirent dans plus de 45 jours. Si ce n'est pas le cas les certificats concernés
sont renouvelés. Ce script est exécuté par l'utilisateur acme qui doit avoir le
droit de lire les clés privées et d'écrire le certificat.

Ce fonctionnement est une adaptation de ce qui a été mis en place [chez
Grenode](https://www.grenode.net/Documentation_technique/SSL/).

## Mise en place Let's Encrypt sur une nouvelle machine

L'installation d'une machine est prise en charge par puppet. Pour configurer
une machine il faut lui appliquer la classe 'acme'. Exemple pour obiwan :

    node "obiwan.fdn.fr" {
      include base
      include ntp
      include acme
      include users::admins
      include apt_dater::host
    }

La classe acme crée l'utilisateur et le groupe acme, installe les scripts
nécessaires, install un cron.

## Installation d'un nouveau certificat

 0. configuration

    L'idée est de mettre dans le repertoire `/etc/acme`, un fichier décrivant les
    chemins des certificats et clés associées. Exemple du fichier
    `www.fdn.fr.conf` :

        DOMAINS="www.fdn.fr fdn.fr www.fdn.org fdn.org"
        _UNAME="www.fdn.fr"
        _DIR="/etc/apache2/ssl/www.fdn.fr"
        
        KEY="$_DIR/$_UNAME.key"
        CRT="$_DIR/$_UNAME.crt"
        CSR="$_DIR/$_UNAME.csr"
        CHAINED="$_DIR/$_UNAME.chained"
        INTERMEDIATE="$_DIR/$_UNAME.intermediate"
        ACME_KEY="$_DIR/$_UNAME.acme.key"
        ACME_CHALLENGE_ROOT=~acme/challenges
        ACME_CHALLENGE_URL=/.well-known/acme-challenge
        ACME_CHALLENGE_DIR="${ACME_CHALLENGE_ROOT}/${ACME_CHALLENGE_URL}"
        RELOAD_SERVICE=apache2

    On crée le répertoire où l'on va stocker les certificats :

        mkdir -p /etc/apache2/ssl/www.fdn.fr

    note : pour que acme_renew puisse relancer les service (variable RESTART_SERVICE) ou les recharger (variable RELOAD_SERVICE) lorsque les certificats sont renouvelés, il est nécessaire de donner à l'utilisateur unix "acme" les droits de sudo pour cette commande. Puppet ajouter ces autorisations pour les services les plus utilisés ; dans le cas où votre service n'est pas configuré par puppet : soit changer la config de puppet pour votre machine, soit ajouter une ligne dans /etc/sudoers du type :

    ```
    acme ALL=(root) NOPASSWD: /usr/sbin/service gitlab-runsvdir restart
    ```

 1. Création des clés et demande de certification
    
    On lance le script [[acme_create]] en tant que root en lui passant le fichier de conf concerné :

        sudo /usr/local/bin/acme_create --config /etc/acme/www.fdn.fr.conf

> (belette: si erreur de type "Can't load /root/.rnd into RNG" cela provient probablement de la version OpenSSL 1.1.1  11 Sep 2018, coutournement possible -> touch /root/.rnd)

 2. Configuration du serveur web pour acme

    Il est nécessaire de faire en sorte que le serveur web réponde sur l'url
    `/.well-known/acme-challenge` pour tous les domaine concernés et renvoie vers
    `$ACME_CHALLENGE_ROOT/.well-known/acme-challenge`.  Pour simplifier, tous
    les virtualhosts utilisent le même répertoire pour stocker les challenges,
    `/var/lib/acme/challenges/`.

    Pour éviter de se répéter sur tous les vhosts, on crée un répertoire de conf partagée : 

        mkdir /etc/apache2/include/

    Et on applique au vhost une configuration qui ressemble à ça :

        <VirtualHost *:80>
                ServerName adminsys.fdn.fr
                LogLevel warn
                Include /etc/apache2/include/acme-challenge.conf
                #Include /etc/apache2/include/redirect-to-https.conf
        </VirtualHost>

    Avec la config `acme-challenge` définie par : (**configuration pour apache 2.4**)
     
        tee /etc/apache2/include/acme-challenge.conf  <<EOF
        Alias /.well-known/acme-challenge /var/lib/acme/challenges/.well-known/acme-challenge
        <Directory /var/lib/acme/challenges>
            Require all granted
        </Directory>
        EOF

    Ou la configuration pour apache 2.2 :
     
        tee /etc/apache2/include/acme-challenge.conf  <<EOF
        Alias /.well-known/acme-challenge /var/lib/acme/challenges/.well-known/acme-challenge
        EOF

    On peut aussi, éventuellement, rediriger automatiquement http sur https. La conf ressemble à ça :

        tee /etc/apache2/include/redirect-to-https.conf  <<EOF
        <ifmodule mod_rewrite.c>
                RewriteEngine On
                RewriteCond %{REQUEST_URI} !^/\.well\-known/acme\-challenge/
                RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
        </ifmodule>
        EOF

    Dans ce cas, ne pas oublier d'activer le module `rewrite` :

        a2enmod rewrite

    Et bien sur, on relance apache :

        service apache2 restart

 3. Génération des certificats

    Pour créer le certificat nous utilisons le script [[acme_renew]], comme si on voulait le renouveler :

        sudo -u acme /usr/local/bin/acme_renew --config /etc/acme/www.fdn.fr.conf

 4. Configuration du serveur web pour ce certificat

    On ajoute les chemins des certificats dans la configuration du vhost. La configuration d'un virtualhost typique ressemble à ça :

        <VirtualHost *:80>
                ServerName adminsys.fdn.fr
                LogLevel warn
                Include /etc/apache2/include/acme-challenge.conf
                Include /etc/apache2/include/redirect-to-https.conf
        </VirtualHost>

        <VirtualHost *:443>
            ServerName adminsys.fdn.fr

            SSLEngine on
            SSLCertificateFile    	/etc/apache2/ssl/www.fdn.fr/www.fdn.fr.chained
            SSLCertificateChainFile	/etc/apache2/ssl/www.fdn.fr/www.fdn.fr.chained 	# Nécessaire sous apache 2.2
            SSLCertificateKeyFile 	/etc/apache2/ssl/www.fdn.fr/www.fdn.fr.key

            # Configuration spécifique au virtualhost
            # ...

        </VirtualHost>

  5. On relit la configuration d'apache :

        service apache2 reload

## Pour tester le fingerprint à partir du certificat

    openssl x509 -in /etc/apache2/sites/adminsys.fdn.fr/adminsys.fdn.fr.crt -fingerprint

## Pour ajouter un altname, nouveau domaine à un certificat existant

- Supprimer la requête CSR existante pour pouvoir la recréer avec
  `acme_create`, puis forcer un renew, ex:

	sudo rm /etc/apache2/sites/lists.fdn.fr/lists.fdn.fr.csr
	sudo /usr/local/bin/acme_create --config /etc/acme/lists.fdn.fr.conf
	sudo -u acme /usr/local/bin/acme_renew --force --config /etc/acme/lists.fdn.fr.conf

## Liste des domaines certifiés par Let's Encrypt

 - www.fdn.fr / www.fdn.org
 - adminsys.fdn.fr
 - secure.fdn2.org
 - vador.fdn.fr
 - git.fdn.fr
 - support.fdn.fr
 - isengard.fr
 - lists.fdn.fr
 - lists.fdn.org
 - webmail.fdn.fr / .org

## Liste des domaines à passer sur du Let's Encrypt

 - wiki-adh.fdn.fr
 - munin.fdn.fr
 - leia.fdn.fr/nagios3 -> à passer en ssl/tls
 - blog.fdn.fr -> à passer en ssl/tls quand sera sur chewie
 - media.fdn.fr -> quand sera en prod. À voir si on laisse la version http only pour les appels web des fichiers.
 - www.open.fdn.fr (quand sera en prod)

