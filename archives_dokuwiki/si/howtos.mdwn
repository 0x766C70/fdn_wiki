
Quelques recettes pour faire faire ce qu'on veut au SI de FDN.

Le SI est installe sur [[adminsys:serveurs:vador]].

<del>https://vador.fdn.fr/private/</del> https://vador.fdn.fr/adsl/

### Gérer les accès authentifiés

Le virtualhost définit que les urls sous ''/adsl'' sont à accès restreint.

La liste des utilisateurs est dans ''/var/www/users/htpasswd'' (format htpasswd d'Apache), et des groupes (pour FDN et les FAI utilisateurs en collecte ou marque blanche) sont dans ''/var/www/users/htgroup''. Il y a un groupe par FAI associatif et un groupe FDN ayant accès à la totalité du SI.

Quand on ajoute un utilisateur, il faut donc également renseigner le(s) groupe(s) au(x)quel(s) il appartient.

Chaque FAI en collecte dispose:
  * un trigramme pour qu'on le reconnaisse
  * d'une URL ''/adsl/subs-<trigramme>.cgi'' pour passer ses commandes (le script en question est ajouté dans les sources du SI)
  * d'un groupe d'utilisateurs
  * cette URL n'est accessible qu'aux utilisateurs de sont groupe

### Accès "commandes" pour un FAI client

Il y a plusieurs étapes :

  * il faut que le FAI soit enregistré comme client dans le SI
    * le plus simple, c'est de leur faire remplir le formulaire comme pour une adhésion (puisqu'on a besoin des mêmes infos), sans attribuer de nouveau numéro d'adhérent (donc ne pas valider l'adhesion dans le SI) Ca se passe ici : https://vador.fdn.fr/souscription/adhesion.cgi
  * il faut un cgi de commande -> ces fichiers sont dans le CVS FDN
    * ''subs-trg.cgi'' dans ''FDN-Adsl/cgi/subscribe'' (''trg'' étant le trigramme du FAI), sera installé sur vador dans ''/var/www/souscription''
    * la section ''trg'' dans ''FDN-Adsl/config/subs.cfg'' (il faut le ''client-id''), sera installé sur vador dans le fichier ''/etc/fdn/adsl/subs.cfg''
    * la section ''formglob-substrg'' dans ''FDN-Adsl/config/subs/subs.cfg'', sera installé sur vador dans le fichier ''/etc/fdn/adsl/subs/subs.cfg''
  * gérer les autorisations d'accès vers ''subs-trg.cgi''
    * créer des accès (groupe et utilisateurs) dans les fichiers ''htgroup'' et ''htpasswd'' (voir le howto concerné)
    * insérer les lignes autorisant l'accès au groupe dans ''/etc/apache2/conf.d/adsl.conf''

