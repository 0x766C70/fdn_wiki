Machine virtuelle hébergeant [gitlab](https://git.fdn.fr/)


# Caractéristiques

- machine virtuelle (proxmox)
- distribution : Debian
- [conf puppet](https://git.fdn.fr/adminsys/puppet/-/blob/production_gitlab/hieradata/hosts/coruscant.fdn.fr.yaml)

# Administration

## Logs

Les logs applicatifs se trouvent dans **/var/log/gitlab/gitlab-rails/**. Pour savoir à quoi correspond chaque fichier de logs, voir la doc [gitlab](https://docs.gitlab.com/ce/administration/logs.html).

Certains fichiers sont en format texte `*.log` pour lecture directe et en format json `*_json.log` pour pouvoir être utilisés par Elasticsearch par exemple.

## Backup/Restore

Source : [sauvegarder et restorer gitlab](https://docs.gitlab.com/ce/raketasks/backup_restore.html)

> Note : les sauvegardes sont stockées dans **/var/opt/gitlab/backups**

### Sauvegardes

Les sauvegardes contiennent toutes les données de l'application (export BDD, fichiers attachés, données dépôts git, logs CI, etc.) mais pas les informations de configuration vues plus haut. Il faudra prendre soin de sauvegarder également, a minima :

- **/etc/gitlab/gitlab.rb**
- **/etc/gitlab/gitlab-secrets.json**

Pour effectuer une sauvegarde :

	sudo gitlab-rake gitlab:backup:create

### Restauration

> Une restauration ne peut avoir lieu que sur une instance ayant **exactement** la même version de Gitlab sur laquelle la sauvegarde a été effectuée.

On part du principe ici qu'on est sur la même machine, que Gitlab tourne déjà et que la sauvegarde se nomme **2019_05_26-ce_gitlab_backup.tar** :

	sudo gitlab-ctl stop unicorn
	sudo gitlab-ctl stop sidekiq
	# Verify
	sudo gitlab-ctl status
	sudo gitlab-rake gitlab:backup:restore BACKUP=2019_05_26-ce
	sudo gitlab-ctl restart
	sudo gitlab-rake gitlab:check SANITIZE=true

## Mise à jour

Source : [maj via Omnibus](https://docs.gitlab.com/omnibus/update/README.html#updating-using-the-official-repositories)

:information_source: page des [*releases*](https://about.gitlab.com/releases/categories/releases)

:warning: penser à faire un snapshot sur PVE avant

### Mise à jour mineure (A.B.x)

	$ sudo apt clean
	$ sudo apt update
	$ sudo apt install gitlab-ce

### Mise à jour majeure (A.x.y)

    $ sudo puppet agent --disable "<pseudo> : maj gitlab"
    $ sudo vi /etc/apt/preferences.d/gitlab-ce.pref # modifier la version voulue, en général x+1
    $ sudo apt clean
    $ sudo apt update
    $ sudo apt install gitlab-ce
    # mettre à jour le dépôt puppet avec la nouvelle version de gitlab
    $ sudo puppet agent --enable
    $ sudo puppet agent -t [--noop]

# Buildbook

Gitlab est installé via le système Omnibus qui simplifie l'installation de tous les composants nécessaires à son utilisation.

Sources :

- [documentation omnibus](https://docs.gitlab.com/omnibus/)
- [installation Debian via omnibus](https://about.gitlab.com/install/#debian)

## Préparation du serveur

	sudo apt-get update
	sudo apt-get install -y curl openssh-server ca-certificates

## Service d'envoi de mails

Normalement les nouvelles machines de FDN sont configurées avec Postfix donc rien de particulier à faire pour ça.


## Installation de Gitlab

	curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
	sudo EXTERNAL_URL="https://git.fdn.fr" apt-get install gitlab-ce

> Lors de l'installation Gitlab met en place automatiquement l'accès TLS via Let's Encrypt. En cas de soucis, voir la [documentation](https://docs.gitlab.com/omnibus/settings/nginx.html#manually-configuring-https) de Gitlab pour utiliser son propre certificat TLS.

## Configuration de Gitlab

Se rendre à l'adresse [https://git.fdn.fr](https://git.fdn.fr), se connecter avec `root/password` et configurer l'instance Gitlab via l'IHM (création des utilisateurs, groupes, projets, etc.).

:warning: la configuration de gitlab est maintenant gérée dans puppet, les mises à jour faites dans les fichiers suivants seront écrasées.

La configuration de gitlab est disponible à plusieurs endroits :

- **/etc/gitlab** :
	- configuration de la solution complète (URI, TLS, paramètrage postgresql, nginx, ci, secrets, etc.)
	- certificats TLS
- **/var/opt/gitlab/gitlab-rails/etc** : configuration de l'application (accès base de données, secrets, paramétrages divers). Il **ne** faut **pas** éditer ces fichiers directement mais plutôt utiliser `sudo gitlab-ctl reconfigure` qui s'occupera d'y faire les modifications.
