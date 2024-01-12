# Administration du service

[[_TOC_]]

## Création d'un dépôt (nouvel utilisateur)

La création d'un dépôt pour gérer une ou plusieurs zones DNS est soumis à un certain nombre de contrainte.

Pour commencer, créez un projet vierge dans le groupe [dns](https://git.fdn.fr/dns).

Allez ensuite dans les paramètres généraux du projet et désactivez toutes les fonctionnalités à l'exception des suivantes:
  - Repository (Dépôt)
    - CI/CD (CI/CD)
  - Environments (Environnements)

Dans les paramètres de la fonctionnalité « Repository » (Dépôt), il faut s'assurer que les développeurs peuvent pousser et fusionner sur la branche par défaut.

Dans les paramètres CI/CD, dans la catégorie « General pipelines » (Pipelines généraux), s'assurer que toutes les cases sont cochées et changez le paramètre « CI/CD configuration file » (Fichier de configuration CI/CD), qui est normalement vide, par `compile.gitlab-ci.yml@dns/utils`.

Pour permettre un accès suffisamment fonctionnel mais sécurisé, il faut donner à l'adhérent les rôles suivants:
  - `Reporter` sur le projet [dns/utils](https://git.fdn.fr/dns/utils/-/project_members). Le rôle `guest` aurait pu suffir si le dépôt avait été public ou interne.
  - `Developer` sur le projet nouvellement créé

<font color="red">**Attention** Accorder des droits supplémentaires reviendrai à donner les mêmes capacités que ceux possédés par les admins DNS</font>

## Fermeture d'un dépôt

Pour supprimer un dépôt, il faut d'abord s'assurer qu'il n'y a plus aucune donnée de ce dernier sur le serveur DNS.

Lors du déploiement, le pipeline crée un nouvel environnement et enregistre la procédure de suppression de ces données.
Par conséquent, avant de supprimer le dépôt il faut arrêter l'environnement présent dans le dépôt au risque de devoir effectuer la suppression manuellement.

Lorsque cela est fait le dépôt peut être supprimer sans problème.

## Ajout d'une zone secondaire

Pour ajouter une nouvelle zone secondaire, il faut ajouter les entrées DNS nécessaire dans le catalogue.

Pour ce faire, il faut avoir les informations suivantes:
- Le nom de la zone
- La liste des serveurs primaires en IPv4 et/ou en IPv6

Chaque zone du catalogue a un identifiant unique. Pour faire simple, nous allons le générer en se basant sur le nom de la zone **sans** le point final en utilisant l'algorithme SHA1. Voici un exemple avec la zone `example.com`:

```console
$ sha1sum <<<"example.com" | cut -d' ' -f1
97612fdad3f6b17f61d6912994b66ea7b7bacc99
```

Voici maintenant les entrées à ajouter au catalogue qui se trouve dans le fichier `/var/cache/bind/db.fdn.catalog` du serveur `dgsi.fdn.fr` à adapter en fonction des informations de la zone:

```bind
97612fdad3f6b17f61d6912994b66ea7b7bacc99.zones	IN	PTR	example.com. ; Ne pas oublier le point final ici
primaries.ext.97612fdad3f6b17f61d6912994b66ea7b7bacc99.zones	IN	A	127.0.0.1
primaries.ext.97612fdad3f6b17f61d6912994b66ea7b7bacc99.zones	IN	A	127.0.0.2
primaries.ext.97612fdad3f6b17f61d6912994b66ea7b7bacc99.zones	IN	AAAA	::1
```

:warning: Il faut bien penser à incrémenter le `serial` du catalogue.

Lorsque les modification ont été fait lancez les commande suivante pour la prise en compte des modifications et vérifier l'état du catalogue:
```
# rndc reload fdn.catalog
# rndc zonestatus fdn.catalog
```

:information: Un script sera écrit afin de faciliter cette manipulation.

## Suppression d'une zone secondaire

La suppression d'une zone secondaire n'est pour le moment faisable que par la modification manuelle de la zone catalogue.

## Autoriser le transfert de zone

Les autorisations de transfert n'est pour le moment faisable que par la modification manuelle de la zone catalogue.
