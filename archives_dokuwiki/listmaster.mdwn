Ne pas oublier de compléter aussi [[support:faq:listes_diffusion|la version]] "grand public" de cette page 8-o
## Les listmasters, qui fait quoi ?
  - Pour [[https://lists.fdn.fr/wws/|FDN]] : [[benevoles:stephaneascoet]],  [[benevoles:taziden]] et [[benevoles:Scara]] 8-)\\
  - Pour FFDN : [[benevoles:taziden]] (Julien Rabier).\\
  - Le grand manitou de sympa : [[benevoles:jcd]] (Jean-Charles Delepine).

### L'adresse listmaster@fdn.fr renvoie au 3/4/2015 sur :

  * scarabeille@free.fr
  * delepine@u-picardie.fr
  * bayartb@edgard.fdn.fr
  * mat@mat.cc
  * stephaneascoet@free.fr
  * taziden@flexiden.org

  * Pour ajouter ou enlever une adresse de cette liste, éditer le fichier /etc/mail/aliases sur solo (la ligne qui commence par "listmaster:") puis faire "sudo newaliases".
  * Une autre technique est d'ajouter le compte d'abonné de l'administrateur dans le groupe ''listmaster'' dans ''/etc/sympa/sympa.conf'' sur [[adminsys:serveurs:Solo]] ou de lui créer un second compte dans ce but, mais Mat n'est pas  favorable à cette solution 8-O
  * Le mot de passe d'accès à la base Mysql est dans ''/etc/sympa/sympa.conf'' sur [[adminsys:serveurs:Solo]], ce n'est pas nécessairement le même que celui du compte ''listmaster@fdn.fr'' 8-O
### Qui est-ce qui gère les abonnements à la liste des membres de la fédération ?
  - [[http://www.ffdn.org/wiki/doku.php?id=documentation:sympa_membres|Explications]] de qui gère les abonnements à la liste membres@ffdn et comment.
#### Les adhérents FDN en mesure de le faire sont :
  - Cyprien/Fulax : cyp@fulax.fr
  - Vivien : vpm@serengetty.fr
  - Valérie/Nawa : bellefeegore@follepensee.net
  - Fabien : fsirjean@eddie.fdn.fr
  - les listmasters FDN

### Quand l'un d'entre-eux écrit :
  - Pour transférer un message de Sympa a quelqu'un d'autre, répondre au courriel plutôt que de faire un transfert 8-O
  - En plus des ajustements dans les destinataires, mettre "repondre a: listmaster@fdn.fr" 8-o
## Les catégories de listes :
Elles sont définies dans /etc/sympa/topics.conf 8-) Une fois ce fichier modifié (si besoin de toucher aux catégories proposées), l'interface graphique tiendra compte des modifications immédiatement 8-O Par contre, il semble qu'un bug de cette dernière empêche de mettre une liste dans la catégorie "autres", qui contient toutes les listes sans catégorie 8-o Dans ce cas, il faut enlever la ligne ''topics'' dans ''/var/lib/sympa/expl/{nomdelaliste}/config''
## Les listes
### tente_rouge :
La propriétaire de cette liste est la compagne d'Emmanuel Bourguin.

#### buro@fdn.fr
Communication entre les membres du bureau. Pour limiter le spam ne pas trop diffuser cette adresse. Liste modérée pour ceux qui sont pas abonnes, et pas non plus abonnes a la liste buro-in@fdn.fr .


#### bureau@fdn.fr
Liste historique de contact de l'asso. Très très spammée (300 spams par jour après passage dans plusieurs antispams). A cause du spam seuls quelques geeks y sont abonnes, charge a eux de transférer sur buro@fdn.fr ce qui n'est pas du spam.

#### adminsys@fdn.fr
Communication entre les membres du groupe adminsys.

#### admin@fdn.fr
Liste qui reçoit les messages automatiques du genre les changements dans les fichiers de changelog, les messages d'erreur, mais aussi pas mal de spam envoyé a des adresses plus ou moins probables genre docmaster@fdn.fr, webmaster@fdn.fr, niahe40dd@fdn.fr et autres. Charge a ceux qui y sont abonnes de transférer ce qui est important sur adminsys@fdn.fr .

FDN ne respecte pas une règle édictée dans la documentation de Sympa: "en revanche, les listmasters ne sont pas censés se substituer aux modérateurs." :-(
### Listes d'envoi d'informations du bureau FDN vers les membres :
#### adsl@fdn.fr :
Liste d'envoi de messages concernant les lignes ADSL fournies aux abonnés FDN ADSL (souvent pour signaler des risques de perturbations) :-( La règle d'envoi est:
    <code>
    title.gettext Envoi uniquement pour membres des listes d'admin, de support et buro
    match([header->Content-Type],/multipart/)      smtp,dkim,md5,smime    -> reject(reason='send_multipart')
    is_subscriber('buro@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('adminsys@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('noyau-adminsys@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('support@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('suivi-adsl@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('admin@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('bureau@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_subscriber('bureau-tech@fdn.fr',[sender]) smtp,smime,md5    -> do_it
    is_editor([listname],[sender])                 smtp,dkim,smime,md5    -> do_it
    is_editor([listname],[header->X-sender])       smtp,dkim,smime,md5    -> do_it
    true()                             smtp,smime,md5    -> reject
    </code>



#### ag@fdn.fr
  - Liste créée le 24 Août 2004 :-)
  - sont abonnés de force tous les adhérents à l'association, de façon automatique par le SI lors de la procédure d'inscription. Pas de suppression automatique quand quelqu'un quitte l'association.

### geix@fdn.fr :
  - [[https://lists.fdn.fr/wws/info/geix|Liste]] qui n'a semble t-il jamais été utilisée
  - ''Listmaster'' en est propriétaire 8-)
### gixe@fdn.fr :
[[https://lists.fdn.fr/wws/info/gixe|Liste supprimée]] 8-O
### Les listes qui régissent qui a le droit de poster :
#### buro-in@fdn.fr
Liste qui sert juste a définir qui a le droit de poster sur ''buro@fdn.fr'', ''tresorier@fdn2.org'', etc. sans être modéré. Pour cela, définir la règle d'envoi/réception de la liste souhaitée sur la règle ''Private, moderated for non buro-in subscribers or fdn members'' 8-)
== Adresses à y mettre : ==
  - Toutes les adresses qu'on trouve utile d'y ajouter :-( Pour cela, les proprietaires peuvent envoyer un courriel à ''sympa@fdn.fr'' avec comme sujet ''ADD buro-in courriel prenom nom'' 8-O
  - Les anciennes adresses des personnes ci-dessus :-/
  - Sauf demande expresse ou dans le cas d'adresse spammeuse, il n'y a sans doute jamais de raison valable de supprimer une de ces adresses :-\
  - Les membres de ag@fdn.fr, les adresses en @nerim :-) et en @fdn sont acceptées par la règle ''Private, moderated for non buro-in subscribers or fdn members'', il est donc inutile de les ajouter à ''buro-in'' =)
#### peniblesamoderer@fdn.fr :
Liste ayant exactement le rôle inverse de buro-in : les abonnés à celle-ci seront systématiquement modérés, même s'ils écrivent à une liste à laquelle ils sont abonnés, grâce à la présence de cette ligne dans le scénario :
''is_subscriber('peniblesamoderer@fdn.fr',[sender]) smtp,dkim,md5,smime    -> editorkey''
### Les listes de débats concernant FDN :
#### bistro@fdn.fr :
  - Liste "poubelle", publique, créée en Octobre 2010, dont le rôle n'est pas clair (son [[https://lists.fdn.fr/wws/info/bistro|objet]] indique "Discussions et trolls non liés aux activités de l'association", or on y parle quand même beaucoup de FDN)
  - Listmaster en est modérateur en remplacement de Lulu
#### ri2014@fdn.fr :
  - discussions sur le projet de règlement intérieur 2014 8-O
  - ''listmaster'' en est propriétaire 8-o
## Exemple de courrier pour ceux qui n'arrivent pas à s'abonner/se désabonner :
Pour s'abonner à une liste de diffusion, envoyez un message vide
à l'adresse |/nom_de_la_liste/-subscribe@fdn.fr|. Par exemple, pour la
liste /ag/, l'adresse est |ag-subscribe@fdn.fr|.

Pour se désabonner, le principe est le même, mais l'adresse est
|/nom_de_la_liste/-unsubscribe@fdn.fr|.

Le gabarit par défaut des messages de rejet d'un courriel comprend un lien vers la page de présentation de la liste, sur laquelle doivent figurer les règles de fonctionnement de celle-ci 8-)

## Plantage lors des recherches longues dans les archives :
Il semblerait que ce soit dû à une expiration du temps dans Apache :-\

## Les utilisateurs :
Pour éviter de mettre ces informations ici, il faudrait trouver comment ajouter facilement des champs de commentaires dans la base des utilisateurs.

^ id SI ^ adresse courriel ^ problème ^ action menée ^
| 545 | erik.gimbert@fantome-dev.net | Adresse en erreur | carte postale envoyée fin Octobre 2015 | 
