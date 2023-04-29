# Préambule

Quelques informations historiques sont disponibles [ici](./archives/archives_dokuwiki/listmaster.md).

# Adminsys

Le service de listes est hébergé sur [solo](./infra/machines/solo.md). Le logiciel utilisé est [SYMPA](https://www.sympa.org/). 

# Listmasters

Les personnes gérant le service de listes sont appelées les listmasters et sont joignables à l'adresse [listmaster@fdn.fr](mailto:listmaster@fdn.fr).

# Qui fait quoi ?

- Pour FDN : stephaneascoet et Scara ;
- Pour FFDN : taziden (Julien Rabier) ;
- Le grand manitou de sympa : jcd (Jean-Charles Delepine).

#### Les comptes avec droits de gestion du serveur sont, au 31/3/2019 :

- <listmaster@fdn.fr>,
- <fsirjean@eddie.fdn.fr>,
- <blackmoor+assos-ffdn@devys.org>

ça se met dans `/etc/sympa/sympa.conf` sur [solo](./infra/machines/solo.md). On peut y mettre le compte habituel ou en créer un spécialement pour que la personne soit maitre. Mat n'est favorable a aucune de ces solutions.

#### L'adresse <listmaster@fdn.fr> renvoie au 31/3/2019 sur : 

- <delepine@u-picardie.fr>,
- <mat@mat.cc>,
- <stephaneascoet@free.fr>,
- <scarabeille@free.fr>,
- <tom@pern.fdn.fr>

Pour ajouter ou enlever une adresse de cette liste, éditer le fichier `/etc/mail/aliases` sur [solo](./infra/machines/solo.md). (La ligne qui commence par "listmaster:") puis faire `sudo newaliases`.
Le mot de passe d'accès à la base Mysql est dans `/etc/sympa/sympa.conf` sur [solo](./infra/machines/solo.md), ce n'est pas nécessairement le même que celui du compte `listmaster@fdn.fr`

#### Quand l'un d'entre-eux écrit :

- Pour transférer un message de Sympa a quelqu'un d'autre, répondre au courriel plutôt que de faire un transfert ;
- En plus des ajustements dans les destinataires, mettre **repondre a: listmaster@fdn.fr**

### Qui gère les abonnements à la liste des membres de la fédération ? (chapitre sans doute pas à jour)

[Explications](http://www.ffdn.org/wiki/doku.php?id=documentation:sympa_membres) de qui gère les abonnements à la liste <membres@ffdn> et comment.

#### Les adhérents FDN en mesure de le faire sont :

- Cyprien/Fulax : <cyp@fulax.fr>
- Vivien : <vpm@serengetty.fr>
- Valérie/Nawa : <bellefeegore@follepensee.net>
- Fabien : <fsirjean@eddie.fdn.fr>
- les listmasters FDN

# Ajouter une liste

- Se connecter en listmaster sur l'interface de Sympa. 
- Aller dans le menu Administrateur des listes, puis Les utilisateurs. 
- Endosser l'identité du demandeur de la liste, et procéder à la demande de création de la liste. 
- Aller dans le menu utilisateur et cliquer sur `Restaurer l'identité` pour revenir à l'identité de listmaster. 
- Aller dans le menu Administrateur des listes puis Listes en attente pour valider la création de la liste. 
- Affiner ensuite si besoin les paramètres de la liste (par exemple en choisissant un scénario spécifique FDN).

# Howtos

### Desabonnements en masse d'une liste :

Apparemment aucune fonctionnalité toute faite n'existe dans Sympa pour cela, alors que c'est le cas pour la manipulation contraire. La seule possibilité restante est d'envoyer un courriel à <sympa@lists.fdn.fr>.

#### Modele :
        QUIET
        DEL ag contact@association.org
        DEL ag o.z@radiophare.net

#### Requêtes en base :

Les listes supprimées dans Sympa ne le sont pas techniquement, elles passent en status `closed`. La plupart du temps il faudra donc filtrer les résultats sur les listes en status `open`.

### Pour trouver les informations de connexion à la BDD de Sympa :

`grep ^db_ /etc/sympa/sympa/sympa.conf`

### Exporter les listes ouvertes dans un fichier:

`select distinct  name_list, robot_list from list_table WHERE list_table.status_list='open' INTO OUTFILE '/tmp/listedeslistes';`
Si l'on veut cette liste dans le but d'avoir une connaissance exhaustive de toutes les adresses utilisees par Sympa, penser aux points suivants:

- Chacun des noms obtenus ainsi se déclinent en au moins deux adresses ("nomliste" est la valeur du premier champ exporte, "robot" celle du deuxième):
  1. nomliste@robot
  2. nomliste-request@robot


- Il y a des adresses utilisées par le serveur et ses administrateurs qui ne sont pas des listes (ou ne sont pas visibles comme telles, mais il est probable que de toutes facons elles soient gerées en direct par le service général de courriel), chacune déclinée pour chaque robot:
  1. sympa
  2. sympa-request
  3. listmaster

**Attention!!! Il manque sûrement des adresses, penser a complèter ce chapitre!**

**Une meilleure solution est très certainement de consulter la liste des alias de Sympa (voir "Fichiers utilisés par Sympa" ci-dessous)**

### Liens utilisateurs/listes :

#### À quelle(s) liste(s) un responsable est-il lié :

`select distinct robot_admin, list_admin from admin_table  where user_admin='listmaster@fdn.fr';`

* Seulement les listes ouvertes :
`select distinct robot_admin, list_admin from admin_table INNER JOIN list_table ON admin_table.list_admin = list_table.name_list WHERE list_table.status_list='open' and user_admin='listmaster@fdn.fr';`

#### A quelle(s) liste(s) un utilisateur est-il abonne :

`select list_subscriber, user_subscriber from subscriber_table WHERE user_subscriber='clangon@mailoo.org';`

### Listes avec quelques caractéristiques, triées par état (conversion de date trouvée sur [ce site](https://www.epochconverter.com)) :

`describe list_table; select name_list, robot_list, FROM_UNIXTIME(creation_epoch_list) as "date de creation", creation_email_list, status_list as status from list_table order by status_list, name_list;

### Obtention des propriétaires et modérateurs :

- Classes par robot avec état :
`select distinct robot_admin, role_admin, user_admin from admin_table order by robot_admin;`

- Sans afficher le rôle (diminue les doublons) :
`select distinct robot_admin, user_admin from admin_table order by robot_admin;`

- Enlever la colonne robot_admin n'est à faire que si on est sûr de vouloir faire la même chose sur toutes les adresses sans distiction de robot :
`select distinct user_admin from admin_table order by robot_admin;`

- Exporter la liste unique des utilisateurs avec les robots sur lesquels ils ont des responsabilités concaténés (bien penser à supprimer les fichiers ensuite!):
`select user_admin, GROUP_CONCAT(DISTINCT robot_admin) INTO OUTFILE '/tmp/acontactersympa' from admin_table GROUP BY user_admin order by robot_admin;`

-	Dont au moins une de ces listes est ouverte:
`select user_admin, list_admin, GROUP_CONCAT(DISTINCT robot_admin) INTO OUTFILE '/tmp/acontactersympa0' from admin_table INNER JOIN list_table ON admin_table.list_admin = list_table.name_list WHERE list_table.status_list='open' GROUP BY user_admin ORDER BY robot_admin;`

# Fichiers utilisés par Sympa:

La liste de (presque?) toutes les adresses utilisées par Sympa semblent être dans `/etc/mail/sympa/aliases`

#### Classer les listes :

Les catégories disponibles sont définies dans `/etc/sympa/topics.conf`.
Ensuite, chaque liste peut être classée dans une ou plusieurs catégories via sa configuration individuelle.
