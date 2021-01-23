# Gestion de l'accès UUCP d'un adhérent

Tout se passe sur *uucp.fdn.fr* (*[[adminsys:serveurs:solo]]*).
## Création

Les informations suivantes sont nécessaires avant d'aller plus loin :
  * le numéro d'adhérent
  * le nom de site UUCP choisi (sur le bulletin d'adhésion), exemple : ''pern''
  * le mot de passe de connexion UUCP (pour un adhérent ADSL on prend le même que la connexion ADSL)
  * le sous-domaine de fdn.fr à router pour le mail (par défaut, prendre *nomdesiteuucp*.fdn.fr, exemple : ''pern.fdn.fr'')

Créer un utilisateur *Unomdesiteuucp* en ajoutant manuellement une ligne de ce type dans ''/etc/passwd'' (utiliser ''vipw'') :

    Upern:x:10:10:Thomas Parmelan:/var/spool/uucppublic:/usr/lib/uucp/uucico

(seuls le login et le champ GECOS sont à modifier).Utiliser ensuite ''vipw -s'' pour ajouter une ligne pour cet utilisateur (recopier la ligne d'un autre site UUCP et modifier le login), puis mettre le bon mot de passe : ''passwd Upern''.

Il faut ensuite ajouter ce site dans la configuration UUCP, pour cela il suffit d'ajouter les lignes suivantes au fichier ''/etc/uucp/sys'' :

    <code>
    # 411, Thomas Parmelan (tom28)
    system        pern
    called-login  Upern
    port TCP
    protocol t
    </code>


(le numéro est le numéro d'adhérent). Les lignes port TCP et protocol t ont été nécessaires pour que l’UUCP over SSH marchent pour moi (vb). Sans ces lignes, mon uucico me disait qu’il trouvait pas de protocole compatible pour discuter.

## Configuration pour accès UUCP over SSH

Il y a deux variantes, sensiblement proches. Chacune a son lot d'avantage et d'inconvénient qui sont listés ci-après :

### Avec mot de passe en clair

Après avoir complété la création comme ci-dessus, il faut de plus ajouter le login et le mot de passe **en clair** au fichier ''/etc/uucp/passwd'' (car ''uucico'' ne pourra pas aller le chercher dans ''/etc/shadow'') et ajouter la clef publique fournie par l'adhérent au fichier ''~uucp/.ssh/authorized_keys'' en ajoutant en début de ligne ''<nowiki>command="/usr/lib/uucp/uucico -D -l</nowiki>"'' et en modifiant éventuellement le champ commentaire pour qu'il permette d'identifier à quel adhérent appartient cette clef (par exemple en y mettant son nom de domaine).

Exemple :

    <code>
    command="/usr/lib/uucp/uucico -D -l" ssh-rsa AAAB3Nza[...etc...]bUCNlOJqsQ== uucp@morpork.renevier.fdn.fr
    </code>


**Avantages** :
  * (pour l'admin) on peut passer des arguments pour le debug (''-x ''*level*) à uucico directement sans toucher à la conf inetd


### Avec PAM pour le mot de passe

Pour ne pas aller entrer le mot de passe en clair dans ''/etc/uucp/passwd'', on va utiliser netcat pour rediriger la connexion UUCP établie à travers SSH sur le port 540 de la machine. Pour ce faire, comme précédemment pour la clef SSH, sauf qu'on utilise la commande ''<nowiki>command="/bin/nc -w 2 localhost 540"</nowiki>''. Ce qui donne une configuration de la forme :


    <code>
    command="/bin/nc -w localhost 540" ssh-rsa AAAB3Nza[...etc...]bUCNlOJqsQ== uucp@morpork.renevier.fdn.fr
    </code>


**Avantages** :
  * Pas de mot de passe en clair dans la conf
  * Une fois la clef ssh déposée, configuration identique pour TCP et SSH

**Inconvénients** :
  * (pour l'admin) pas de gestion fine du debug pour un login donné

## Routage du mail

On part du principe qu'on va router le mail du sous-domaine ''pern.fdn.fr'' vers le site UUCP ''pern'' (le principe reste valable pour un domaine indépendant de la zone fdn.fr, et doit être appliqué pour chaque domaine supplémentaire à router vers le même site).

Ajouter à ''/etc/postfix/transport'' les deux lignes suivantes :

    <code>
    pern.fdn.fr                         uucp:pern
    .pern.fdn.fr                        uucp:pern
    </code>


puis ''postmap /etc/postfix/transport''.

Remarques :
  * la deuxième ligne ne sert que si l'on souhaite gérer des sous-domaines de ''pern.fdn.fr'', ce n'est pas forcément le cas pour tout le monde.
  * faire de même avec ''pern.fdn.org'' si besoin.
  * IMPORTANT : dans le cas d'un domaine en dehors de fdn.{net,org} (exemple: ''dugenou.info''), il faut rajouter le domaine dans ''/etc/postfix/relay_domains'' (puis ''postmap /etc/postfix/relay_domains'')
  * si besoin, ne pas oublier de créer un enregistrement MX pour ''pern.fdn.fr'' ... (sur *[[adminsys:serveurs:leia]]*, éditer ''/etc/bind/fdn.subdomains'' puis ''./update_serial.pl db.fdn.fr'' et ''./update_serial.pl db.fdn.org'' et enfin ''rndc reload fdn.fr && rndc reload fdn.org'') FIXME: cela devra faire l'objet d'une autre page !

## Côté adhérent...

Deux liens intéressants :
  * sur le site FDN : http://www.fdn.fr/Connexion-PPP-UUCP.html
  * un petit topo écrit par Arno : http://www.fdn.fr/~arenevier/fdn/uucp_postfix.php
