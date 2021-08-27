
[Pass](http://zx2c4.com/projects/password-store/) (password-store) est un
gestionnaire de mot de passe se basant sur GPG. Les mots de passe sont
tous dans un fichier différent, et classés en suivant une arborescence,
l'utilitaire *pass* permet d'opérer dessus.

# Installation client

Les mots de passe sont stockés dans le depot GIT du wiki dans ``password``

Les clés GPG utilisé sont stockés dans le keyring ``password/.gnupg``

Il faut installer l'utilitaire pass, (sur debian-like, jessie ou wheezy-backports mini)

     apt-get install pass

Ou voir sur la [page du projet](http://zx2c4.com/projects/password-store/) pour
les autres distribs.

Il faut utiliser le script bin/fdn_pass (vous pouvez par exemple ajouter
dans votre PATH le répertoire bin pour pouvoir utliiser ce script plus
facilement)

     export PATH=<mondepot>/bin;$PATH

     fdn_pass help

Afficher le trousseau

     fdn_pass
     Password Store
     └── gandi
        ├── RRC27-GANDI

Mettre un mdp dans le presse papier

     fdn_pass -c gandi/RRC27-GANDI

Afficher un mot de passe dans le terminal

     fdn_pass show gandi/RRC27-GANDI

Ajouter un mdp

     fdn_pass insert toto/fdn-supersecret

# Ajout d'un admin

Afin d'ajouter la clé GPG de l'admin aux personnes autorisées à consulter les
mots de passe, il suffit de :

## Ajouter la cle gpg admin

Si la cle n'est pas sur un keyserver

     bin/fdn_pass_gpg2 --import <admin_pubkey_file>

Sinon depuis le keyserver

     bin/fdn_pass_gpg2 --keyserver hkp://pgp.mit.edu --search-keys '<admin name>'

Si gpg2 se plaint sur les droits :

     chmod go-rx passwords/.gnupg/

Avant d'aller plus loin, il faut avoir récupéré la clé par un moyen sur avoir
vérifié son empreinte.

## Ajout de l'indentifiant au groupe fdn

Et ajouter l'identifiant au group fdn

     vi password/.gnupg/gpg.conf

Et re-chiffrement du keyring

     bin/fdn_pass init fdn

# Liens

- [homepage](http://zx2c4.com/projects/password-store/)
- [{z,ba}sh completion](http://git.zx2c4.com/password-store/tree/contrib)

