# Ajouter ou modifier un reverse dns pour un adhérent

# Exemple et connexion

On se base sur la demande de reverses suivante :

  * ''2001:910:10ce::42'' => mail.example.com
  * ''80.67.176.42'' => mail.example.com

Se connecter en SSH sur ''leia.fdn.fr''.

# Reverse IPv6

L'IP de l'adhérent est ''2001:910:10ce::42''.

Commencer par récupérer l'équivalent PTR de l'IPv6 fournie (on peut également utiliser ''sipcalc -r'') :

    $ dig +noall +question -x 2001:910:10ce::42
    ;2.4.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.e.c.0.1.0.1.9.0.1.0.0.2.ip6.arpa. IN PTR

Modifier le fichier dans ''/etc/bind/'' qui commence par « db. » et qui est le plus proche du PTR trouvé en partant de la droite.

Dans notre cas, il s'agit de ''/etc/bind/db.0.1.0.1.9.0.1.0.0.2.ip6.arpa'' :

    $ sudo vim /etc/bind/db.0.1.0.1.9.0.1.0.0.2.ip6.arpa

On constate que les lignes du fichier débutent presque toutes avec la syntaxe « x.x ». Dans notre cas, le « x.x » qui suit (en partant de la droite) notre PTR, après ce qui a été utilisé pour le nom du fichier, est « e.c ». Nous allons donc nous positionner, dans le fichier, entre la ligne qui commence par « d.x » et celle commençant par « f.x » (ordre alphanumérique).

Entre ces deux lignes, on ajoute (en n'oubliant pas le point final, et en vérifiant avant si un PTR ou une délégation avec « NS » n'existe pas déjà dans ce coin-là) :

    ; Nom adherent
    2.4.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.e.c     IN      PTR     mail.example.com.
  
Si l'adhérent avait demandé une délégation complète de son préfixe IPv6 (avec son serveur DNS ''ns.example.com'') plutôt qu'un simple reverse, on aurait plutôt ajouté :

    ; Nom adherent
    e.c     IN      NS     ns.example.com.

Enregistrer le fichier et quitter ('':wq'').

Exécuter la commande suivante, avec le nom du fichier précédent en argument, pour mettre à jour le champ « SERIAL » qui indique qu'il y a eu une mise à jour de la zone :

    $ sudo /etc/bind/update_serial.pl /etc/bind/db.0.1.0.1.9.0.1.0.0.2.ip6.arpa

Enfin, exécuter la commande suivante (le dernier argument correspond au nom du fichier après « db. ») pour demander au serveur de prendre en compte la modification :

    $ sudo rndc reload 0.1.0.1.9.0.1.0.0.2.ip6.arpa

Tester depuis une tierce machine :

    $ dig +short -x 2001:910:10ce::42
    mail.example.com.
  
S'il n'y a pas de réponse (ou qu'il s'agit encore de l'ancien reverse), il peut être nécessaire d'attendre un peu que la propagation des DNS soit complète.


# Reverse IPv4

L'IP de l'adhérent est ''80.67.176.42''.

Modifier le fichier ''/etc/bind/db.80.67.176'' (les nombres après « db. » correspondant à l'IP sans sa dernière partie) :

    $ sudo vim /etc/bind/db.80.67.176

À la ligne débutant par « 42 » (''/^42''), si le reverse n'a jamais été modifié, on trouve :

    42      IN      PTR     reverse-42.fdn.fr.
  
Remplacer par (en n'oubliant pas le point final) :

    42      IN      PTR     mail.example.com.
  
Enregistrer le fichier et quitter ('':wq'').

Exécuter la commande suivante, avec le nom du fichier précédent en argument, pour mettre à jour le champ « SERIAL » qui indique qu'il y a eu une mise à jour de la zone :

    $ sudo /etc/bind/update_serial.pl /etc/bind/db.80.67.176

Enfin, exécuter la commande suivante (les nombres dans le dernier argument correspondent à ceux du fichier précédent, mais dans l'ordre inverse) pour demander au serveur de prendre en compte la modification :

    $ sudo rndc reload 176.67.80.in-addr.arpa
  
Tester depuis une tierce machine :

    $ dig +short -x 80.67.176.42
    mail.example.com.
  
S'il n'y a pas de réponse (ou qu'il s'agit de l'ancien reverse), il peut être nécessaire d'attendre un peu que la réjuvénation des DNS soit complète.
