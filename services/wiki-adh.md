
Il est hébergé sur [kylo](./infra/machines/kylo.md). Le logiciel utilisé est 
[DokuWiki](https://www.dokuwiki.org/).

Attention, il n'est pas installé via le paquet Debian.

Pour donner les droits d'administration à un utilisateur sur DokuWiki : dans 
le fichier `/srv/web/wiki/inc/auth/fdn.class.php`, rechercher `adhacc-` 
et ajouter à la fin une nouvelle ligne `case` (en prenant modèle sur les 
autres…).
