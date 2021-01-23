# Usenet chez FDN

Tout se passe sur *news.fdn.fr*, qui est un alias de *[[adminsys:serveurs:solo]]* (et pour éviter de difficiles contorsions il faut impérativement que ce soit la même machine que *uucp.fdn.fr*, et donc par transitivité que *mail.fdn.fr*).

Adminsys plus ou moins compétents sur INN: fulax, nono, tom.

## Installation et configuration système

''apt-get install inn2'' puis édition des fichiers dans ''/etc/news/''.

### SSL/TLS

INN est un peu débile et exige que la clef du certificat soit en 600 avec news comme seul owner du fichier, et de façon similaire pour le certificat. Les fichiers .crt et .key sont donc copiés dans /etc/news/ssl. Les chemins sont spécifiés dans /etc/news/inn.conf à la fin.

### CleanFeed

Usenet, comme une bonne partie de l'internet est assez pollué par des spams. Il existe un ensemble de scripts perl d'application forcée de bonnes pratiques appelé CleanFeed. L'installation suit documentation détaillée ici : http://www.mixmin.net/cleanfeed/index.html.
Cleanfeed est installée sur le serveur dans ''/etc/news/filter''. La configuration est celle par défaut, hormis la correction des paths qui vont bien. Le fichier de config est dispo dans ''/etc/news/filter/cleanfeed/etc/cleanfeed.local'',

Un Daily report est généré et accessible ici http://news.fdn.fr/status/cleanfeed.stats.html

## Ajout d'un feed NNTP

  * Éditer ''/etc/news/newsfeeds'' pour ajouter le feed sortant (prendre exemple sur les feeds existants). Ne pas oublier d'ajouter en commentaire les informations de contact, et qui a fait la configuration côté FDN.
  * Éditer ''/etc/news/innfeed.conf'' pour le hostname du feed sortant
  * Éditer ''/etc/news/incoming.conf'' pour le hostname du feed entrant
  * ''ctlinnd reload newsfeeds "message de log (juste le nom du feed c'est bien comme message)"''
  * ''ctlinnd reload incoming.conf *nom-du-feed*''

## Ajout d'un feed UUCP

  * Éditer ''/etc/news/newsfeeds'' pour ajouter le feed (prendre exemple sur un feed existant et réellement utilisé, par exemple ''pern''). Ne pas oublier d'ajouter les infos utiles en commentaire.
  * Éditer ''/etc/news/send-uucp.cf'' pour ajouter le site concerné (prendre exemple sur ''pern'' ou ''edgard'', bref un site avec ''nom-du-site::BUFFCHAN!'' dans la première colonne)
  * ''ctlinnd reload newsfeeds *nom-du-site*''

## Modification d'un feed

Pour modifier la liste des groupes envoyés à un site particulier, il faut simplement éditer ''/etc/news/newsfeeds'' et faire un ''ctlinnd reload newsfeeds *nom-du-site*''. Un outil de mise à jour automatisé de feed (par mail ou en interface Web) serait assez facilement réalisable si le besoin s'en faisait vraiment sentir (ce n'est pas du tout le cas actuellement, très peu voire aucune demande...)

## Statistiques

Un rapport quotidien est envoyé à <usenet@fdn.fr> (donc au groupe ''adminsys''). La version "jolie" de ce rapport (et avec des archives) est disponible sur http://news.fdn.fr/status/ sans login ni mot de passe pour l'instant (c'est pour celà que cette URL n'est "linkée" nulle part, si elle le devenait il faudrait mettre un login/pass pour éviter que des logins de connexion des adhérents soient aspirés par Google et compagnie). Du coup, pour faire simple, http://news.fdn.fr/ redirige sur http://www.fdn.fr/News.html.
