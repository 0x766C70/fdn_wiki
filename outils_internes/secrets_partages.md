[Pass](http://zx2c4.com/projects/password-store/) (password-store) est un
gestionnaire de mots de passe se basant sur GPG. Les mots de passe sont
tous dans un fichier différent, et classés en suivant une arborescence,
l'utilitaire *pass* permet d'opérer dessus.

# Installation du client

Les mots de passe sont stockés dans le dépôt Git [passwords](https://git.fdn.fr/adminsys/passwords).

Les clés GPG utilisées sont stockées dans le keyring ``password/.gnupg``

Il faut installer l'utilitaire ``pass`` (sur Debian-like, Jessie ou Wheezy-backports minimum) :

     # apt-get install pass

Ou voir sur la [page du projet](https://www.passwordstore.org/) pour
les autres distribs.

Il faut utiliser le script ```bin/fdn_pass``` (vous pouvez par exemple ajouter
dans votre PATH le répertoire bin pour pouvoir utliiser ce script plus
facilement)

     $ export PATH=<mondepot>/bin;$PATH

     $ fdn_pass help

Afficher le trousseau

     $ fdn_pass
     Password Store
     └── gandi
        ├── fdn_adminsys

Mettre un mot de passe dans le presse-papier

     $ fdn_pass -c gandi/fdn_adminsys

Afficher un mot de passe dans le terminal

     $ fdn_pass show gandi/fdn_adminsys

Ajouter un nouveau mot de passe

     $ fdn_pass insert toto/fdn-supersecret

# Ajout d'un admin

Afin d'ajouter la clé GPG de l'admin aux personnes autorisées à consulter les
mots de passe, il suffit de :

## Ajouter sa clé GPG

Si la clé n'est pas sur un serveur de clé :

     $ bin/fdn_pass_gpg --import <admin_pubkey_file>

Sinon depuis le serveur de clef OpenPGP :

     $ bin/fdn_pass_gpg --keyserver hkps://keys.openpgp.org --search-keys <fingerprint>

Si GPG2 se plaint sur les droits :

     $ chmod go-rx passwords/.gnupg/

Avant d'aller plus loin, il faut avoir récupéré la clé par un moyen sûr afin d'avoir
vérifié son empreinte.

## Ajout de l'identifiant au groupe fdn

Et ajouter l'identifiant au group fdn :

     $ vi password/.gnupg/gpg.conf
     group fdn=<email@example.org>

Et re-chiffrement du keyring :

     $ fdn_pass init fdn

# Liens

- [homepage](http://zx2c4.com/projects/password-store/)
- [{z,ba}sh completion](http://git.zx2c4.com/password-store/tree/contrib)

