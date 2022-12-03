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
une machine il faut lui appliquer la classe 'acme'. Exemple pour jira :

    hieradata/hosts/jira.fdn.fr.yaml
      classes:
        - acme

Les variables suivantes sont de plus disponibles:
 - `acme::mode: 'acmesh'` (ou `acmetiny` pour l'ancien mode)
 - `acme::standalone: false` (pour mode webroot, mettre à true
pour activer la redirection de port)
 - `acme::services: ['apache2', 'nginx', 'lighttpd']` (pour les
règles sudoer de l'user acme)

La classe acme crée l'utilisateur et le groupe acme, installe les scripts
nécessaires, install une cron.

## Installation d'un nouveau certificat avec acme.sh

 0. configuration

   acme.sh tourne sous l'user 'acme'; utiliser sudo -u acme ou similaire comme dans les exemples.

   Il faut s'enregistrer un compte pour utiliser acme avec zeroSSL, mais on préfère LE,
   donc pas besoin de `acme.sh --register-acount` et on passe directement au certif

 1. Création de clé & demande de certif:

   En mode webroot (à noter que la conf du serveur web n'est PAS automatique:
   il faut créer un lien dans le vrai webroot vers /var/lib/acme/challenges/.well-known/acme
   comme avant!)

   ```
   sudo -u acme acme.sh --issue \
        --webroot /var/lib/acme/challenges \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --renew-hook "sudo systemctl restart foo" \
        --domain mamachine.fdn.fr \
        [--domain alias...]
   ```

   pour le mode standalone (bien avoir mis acme::standalone à true dans puppet!)

   ```
   sudo -u acme acme.sh --issue \
        --standalone --httpport 44380 \
        --server https://acme-v02.api.letsencrypt.org/directory \
        --renew-hook "sudo systemctl restart foo" \
        --domain mamachine.fdn.fr \
        [--domain alias...]
   ```

   pour ecc: ajouter `--keylength ec-384`

   On peut tester avec https://acme-staging-v02.api.letsencrypt.org/directory en premier
   dans le doute ; c'est particulièrement utile pour le mode webroot quand on n'est pas
   certain de la conf parce que LE est radin en retry...

 2. Faire utiliser les nouveaux certifs/clés au service que l'on veut configurer.

   La clé `/etc/acme/<domain>[_ecc]/<domain>.key` est en 600 donc il faut la passer en
   640 + changer de groupe, ou bien simplement la copier pour le service elle ne devrait
   pas être regénérée.

   Le certif est lisible par tout le monde: faire un lien du service vers
   `/etc/acme/<domain>[_ecc]/fullchain.cer` et laisser ça où c'est pour que le script
   puisse rafraîchir le fichier.

   https://ssl-config.mozilla.org a de bons exemples de configurations avec paramètres TLS
   pour la partie config.

 3. Tester que le service marche bien.

   Verifier que `sudo -u acme acme.sh --cron` retrouve bien ses petits ;
   s'il y a un service à redémarrer rajouter `--force` pour tester le redémarrage du service.

## Installation d'un nouveau certificat avec les anciens scripts acme_create (acmetiny)

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

Supprimer la requête CSR existante pour pouvoir la recréer avec `acme_create` puis forcer un renew, exemple :

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

