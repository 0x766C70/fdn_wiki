[[_TOC_]]

FDN fournit à ses membres de l'hébergement de site web sur [rey](./infra/machines/rey.md) correspond au domaine mutu.fdn.fr.

Les technos supportées sont :

- Langages :
  - PHP : 5.6, 7.0, 7.1, 7.2, 7.3, 7.4, 8.0, 8.1 via php-fpm
  - Perl et autre CGI
- SGBD :
  - MariaDB

Cette liste est appelée à évoluer en fonction des besoins des adhérents.

Si le membre n'a pas de domaine, il est possible d'héberger un site sur **http(s)://username.mutu.fdn.fr**, la gestion du sous-domaine mutu.fdn.fr étant déléguée sur rey.


# Présentation

Voir la fiche de [rey](./infra/machines/rey.md) pour en savoir plus.

## Dossiers utilisateur

Pour les adminsys (ceux poussés par puppet), le *home* se situe à l'habituel `/home/username`.

Pour les adhérents qui souhaitent héberger un site, leur *home* se situe à `/srv/webusers/username`. À la création d'un utilisateur, est créé un dossier `sites` qui sera la racines de **tous** ses sites. Il pourra par exemple créer un répertoire `blog` pour y mettre son blog, un `cv` pour sa page d'informations, etc.

## Configurations Apache

Les configurations disponibles des sites webs sont stockées dans `/etc/apache2/sites-available` comme suit :

- à la racine : les configurations par défaut soit principalement la configuration du domaine mutu.fdn.fr
- dans `webusers/username` : un fichier de conf par domaine

Les configurations activées des sites webs sont visibles dans `/etc/apache2/sites-enabled` sans aucune arborescence pour retrouver facilement à quel utilisateur appartient un site/domaine.

## Fichiers de logs

Les fichiers de logs Apache sont tous situés dans `/var/log/apache2` comme suit :

- `mutu.fdn.fr` : fichiers d'accès et d'erreurs du site mutu.fdn.fr
- `webusers/username/domain` : fichiers d'accès et d'erreurs par domaine pour chaque utilisateur
- racine : logs qui vont nulle part ailleurs ;)

La rotation des logs est en place pour chaque utilisateur, voir `/etc/logrotate.d/apache2-username`. La rotation a lieu tous les jours et l'historique est conservé sur 366 jours.

Chaque utilisateur a accès aux logs de ses sites via `~/logs` qui est un lien symbolique vers le répertoire `/var/log/apache2/webusers/username`. Il n'a évidemment accès qu'en lecture.

## Bases de données

Actuellement seule une instance de MariaDB tourne, mais d'autres sont envisageables.

Pour simplifier l'administration par les utilisateurs, [Adminer](https://www.adminer.org/) a été installé et est accessible à l'adresse suivante : [accueil Adminer](https://mutu.fdn.fr/adminer/)

Les fichiers de données sont dans `/srv/db`

Pour l'instant, seuls les adminsys ont la possibilité de créer des bases de données.

# Mise en place d'un site

Afin de gagner du temps en adminsys et d'éviter des erreurs de typo, des scripts ont été mis en place. Ils se trouvent dans avec un dépôt sur [gitlab](https://git.fdn.fr/adminsys/fdn-mutu/-/tree/master/scripts).

> il faut être root (ou sudo) pour lancer les scripts

## Création de l'utilisateur

Avant de créer un utilisateur, vérifier qu'il n'existe pas déjà dans `/srv/webusers`. Pour pouvoir le créer, vous avez besoin de : son nom, son prénom, son numéro d'adhérent ainsi que sa clé publique SSH. Il vous suffit alors de suivre les instructions du script :

	cd /root/fdn-mutu/scripts
	./create_user.sh

Vérifier que le home de l'utilisateur a bien été créé.

## Mise en place d'un site PHP

Avant de mettre en place le site, vous aurez besoin de : utilisateur, version de PHP, répertoire du site, domaine du site, besoin de TLS(SSL).

### Installer la version de PHP si elle ne l'est pas déjà

Pour vérifier si une version de PHP est installé sur la machine :

	systemctl status php7.2-fpm

Si elle n'est pas installée :

	cd /root/fdn-mutu/scripts
	./install_php.sh

> Note : ce script contient également la liste des modules PHP à installer, il faut donc la mettre à jour au fur et à mesure qu'on en rajoute et relancer l'install pour **toutes** les versions de PHP déjà installées

### Mettre en place un pool PHP pour l'utilisateur

Grâce à php-fpm il est possible d'affecter des *pools* à chaque utilisateur ce qui permet de cloisonner les sites, ce qui a été fait ici. la procédure suivante permet de mettre en place ces pools s'ils ne le sont pas déjà.

Pour vérifier l'existence d'un pool pour un utilisateur (2 par défaut) et une version de PHP :

	systemctl status php7.2-fpm

Pour configurer un pool pour un utilisateur, vous aurez besoin de : utilisateur et version de PHP.

	cd /root/fdn-mutu/scripts
	./configure_php_for_user.sh

### Configurer le site pour utiliser la bonne version de PHP

Pour laisser la possibilité à l'utilisateur de modifier la version de PHP pour son site, à la condition qu'un pool existe, la version de PHP est configurée via le fichier `.htaccess`. Pour le configurer pour un site spécifique, vous avez besoin de : utilisateur, répertoire du site, version de PHP. Puis il suffit de suivre les instructions du site :

	cd /root/fdn-mutu/scripts
	./configure_php_for_site.sh

## Configuration Apache d'un site (statique ou avec PHP)

Pour mettre en place un nouveau site internet, vous avez besoin de : utilisateur, répertoire du site, adresse email, nom de domaine, TLS (oui/non).

Si le domaine est du style `username.mutu.fdn.fr`, il faut **préalablement** configurer le serveur DNS (bind9) qui se trouve su [rey](http://localhost/~alex/fdn-adminsys/infra/machines/rey/#index8h2), sans quoi tout ce qui suit ne servirait à rien. Pour cela :

1. éditer le fichier de la zone : `vi /etc/bind/db.mutu`
1. rajouter une ligne du style `username  IN CNAME ns` en dessous de celles déjà existantes, si elle n'existe pas déjà
1. modifier le *Serial* en début de fichier, qui correspond à la date sous la forme `YYYYMMDDXX` où `XX` correspond à un numéro incrémenté après chaque modification (si on change de date, le numéro redevient alors 01)
1. charger la nouvelle conf : `systemctl reload bind9`
1. vérifier qu'elle a bien été prise en compte : `systemctl status bind9`

Il suffit alors de lancer le script suivant :

	cd /root/fdn-mutu/scripts
	./configure_website_with_domain.sh

> Le script s'occupe de la génération des certificats TLS, il faut donc s'assurer avant que la propagation DNS a bien eu lieu.

## Création d'une base de données

Pour créer une base de données MySQL/MariaDB, vous avez besoin de : utilisateur, nom de la base, mot de passe de l'utilisateur mysql **root**. Il suffit alors de lancer le script suivant :

	cd /root/fdn-mutu/scripts
	./create_mysql_databse.sh

> Le script crée un utilisateur mysql du même nom s'il n'existe pas et renvoie à la fin le mot de passe qu'il faudra lui fournir. Le nom de la base de donnée est aussi préfixé par le nom de l'utilisateur pour éviter tout problème de collision de noms.
