## Comptes POP/IMAP
### Premier compte de la personne :
  - Pour avoir un courriel chez FDN, comme pour les autres services, l'adhésion simple ne suffit pas, il faut être abonné aux services 8-)
#### Il serait souhaitable de créer un formulaire de demande de création de boîte :
Informations qui seraient à collecter :
  - numéro adhérent :-),
  - abonnement(s),
  - adresse souhaitée,
  - cette nouvelle adresse est-elle à utiliser pour les listes de discussion ? le SI ?
  - Mettre un système de téléversement de clé publique SSH =)
#### 1-Création du compte sur le système :

Il faut avant tout créer un compte Unix sur *[[adminsys:serveurs:solo]]* (il servira pour gérer le mot de passe). Comme pour les autres services, on respecte quelques conventions pour mieux s'y retrouver :
  * Éviter les caractères non-ASCII, quel que soit le champ 8-O
  * *login* formé de la première lettre du prénom et du nom complet.
    *  Exemple: le login de *Marcel Dugenou* sera ''mdugenou''.
    *  En cas de prénom composé, une possibilité est de mettre l'initiale de chaque prénom 8-)
    * prenom.nom peut éventuellement se faire aussi, mais il n'y a pas de liste officielle des choses acceptées 8-O
  * *uid* de la forme 10000 + numéro d'adhérent
  * *groupe* users
  * *mot de passe* : un mot de passe choisi aléatoirement (par exemple avec *pwgen* ou *apg* ou *makepasswd*)

Reprenons l'exemple de ce brave Marcel, si son numéro d'adhérent est 666 ça donne ceci :
  - ''ssh gentiladmin@solo.fdn.fr'' :-/
  - Générer un mot de passe aléatoire si ce n'est pas déjà fait :-\
  - ''sudo su''
    <code>solo$ sudo adduser --ingroup users --uid 10666 --gecos "Marcel Dugenou" mdugenou</code>

== S'il a fourni sa clé : ==
pour la clef qui lui permettra de se connecter en ssh, il faut faire un dossier .ssh dans son ~ avec des permissions a 700 et appartenant a <son uid>:100 puis mettre dans ce dossier un fichier authorized_keys avec des permissions a 600 et appartenant aussi a <son uid>:100
#### 2-Création de la boîte :
Ensuite, on crée la boîte aux lettres proprement dite dans Cyrus (le mot de passe de l'admin étant le même que le root de MySQL, qui se trouve dans ''/root/.my.cnf'') :
== 1-Se connecter : ==
    <code>
    solo$ cyradm -user cyradm localhost
    IMAP Password:
    
    </code>

== 2-Vérifier que celle-ci n'existe pas déjà : ==
    <code>
    
    localhost> lm user.%
    
    </code>


== 3-Création : ==
    <code>
    localhost> createmailbox user.mdugenou
    localhost> quit
    </code>


*ATTENTION à ne pas oublier le préfixe "user." !* Le nom qui se situe derrière est le même que celui créé au niveau système 8-o

**Ressources d'aide sur Cyrus:**
  - http://cyrusimap.web.cmu.edu/docs/cyrus-imapd/ 8-O
  - http://cyrusimap.web.cmu.edu/docs/cyrus-sasl/ 8-o
== 3-Postfix : ==
Enfin, il faut aller expliquer à notre ami Postfix qu'il a de nouvelles adresses à gérer, en éditant le fichier ''/etc/mail/user.aliases'' comme suit :

    <code>
    # mdugenou aliases-start
    mdugenou: mdugenou@imap.fdn.fr #Il faut seulement remplacer "mdugenou" par le nom utilisé dans Cyrus dans le cas que l'on traite, elle sera accessible aussi bien en POP qu'en IMAP
    marcel.dugenou: mdugenou #Cette ligne, optionnelle, permet de créer un alias : elle signifie que l'adresse courriel marcel.dugenou@fdn.fr renverra vers mdugenou@fdn.fr
    # mdugenou aliases-stop
    </code>


Et, bien sûr, ne pas oublier de lancer la commande ''sudo newaliases'' pour que ces modifications soient prises en compte et le ''vim /root/Changelog'' qui va bien 8-)


#### 3-Message à la personne :
**Exemple de message envoyé par Hamster :** \\
Ton adresse est faite : \\
''mdugenou@fdn.fr'' \\
* Ton identifiant de connexion est : ''mdugenou'' \\
* Ton mot de passe est : ''toto'' \\
* Tu peux changer ton mot de passe avec la commande passwd en te connectant en ssh sur solo.fdn.fr. Les connexions ssh se font uniquement par clef et non pas par mot de passe ; si ça ne marche pas c'est que j'ai mal mis ta clef, reviens donc vers nous. Si ça te gonfle, tu peux aussi demander qu'on t'en mette un autre en nous disant lequel (il est preferable de pas choisir un mot de passe trop simple, genre surtout pas "toto"). \\
 \\
Tu peux te connecter : \\
- par le webmail : webmail.fdn.fr \\
- en POP ou en IMAP : mail.fdn.fr(port 143 pour l'imap, port 110 pour le pop
, starttls, mot de passe non chiffré) \\

Pour envoyer du courrier, tu peux utiliser smtp.fdn.fr (port 587, pratique si le port 25 est bloqué, starttls, mot de passe non chiffré)

Les certificats utilisés par FDN sont signés par l'autorité CACert, qui
n'est pas forcément présente par défaut sur toutes les machines.

Il peut donc falloir que tu importes le certificat racine Class 3 de CACert (en pièce jointe, je te laisse trouver le bon format pour ton logiciel) ou alors que tu acceptes l'exception de sécurité. Sinon, tu peux aussi repasser sur une connexion non chiffrée (sans
STARTTLS), mais c'est moins bien. N'hésite pas à revenir vers nous en cas de pépin, en laissant bien
adminsys@fdn.fr dans les destinataires pour maximiser les chances de
réponse :)

*Pour mettre le certificat en piece jointe, on peut aller le chercher la : https:*www.cacert.org/index.php?id=3 //

== Dans le cas où un ou plusieurs alias à/ont été créé(s), préciser : ==
Tu as une et une seule boite mail, et 2 adresses qui arrivent toutes les
deux dans la meme boîte, donc une seule boîte à configurer comme indiqué ci-dessus ; tu y trouveras les messages envoyés à ''mdugenou@fdn.fr'' et ceux
à ''marcel.dugenou@fdn.fr''

Si tu veux envoyer des messages depuis l'adresse ''mdugenou@fdn.fr''
il faut que tu ailles "gérer les identites" dans l'outil de gestion de courriels : webmail, thunderbird (dans
"Édition" puis "Paramètres des comptes")...

Au moment ou tu rediges un message, tu peux choisir quelle identité utiliser.

### Autres adresses pour une personne :
Dans ce cas, il vaut mieux créer un [[adminsys:dns|sous-domaine]], ce qui peut donner michu@dugenou.fdn.fr 8-)
Se baser sur les comptes présents dans /etc/postfix/virtusertable
par exemple :

    <code># Philippe Michel (576)
    michel.fdn.fr   anything
    philippe@michel.fdn.fr  pmichel@imap.fdn.fr
    come@michel.fdn.fr      cmichel@imap.fdn.fr
    aude@michel.fdn.fr      amichel@imap.fdn.fr
    enfant.dysphasie@michel.fdn.fr  philippe@michel.fdn.fr</code>



Donc, créer les différents comptes voulus, comme les classiques @fdn.fr,
puis remplir virtusertable :

    <code>damaine  chaine quelconque
    a@doamine a-fdn@imap.fdn.fr
    b@doamine b-fdn@imap.fdn.fr
    c@doamine c-fdn@imap.fdn.fr</code>


Enfin taper make dans /etc/postfix
C'est fait.

Pour ce qui est des domaines de liste de diffusions il y a plusieurs
exemples disponibles.

Voir par exemple :
/etc/sympa/lists.ffdn.org/*

/etc/postfix/virtual-ffdn

grep ffdn /etc/mail/sympa/aliases


## Supprimer un compte

Il faut préalablement trouver tout ce que l'utilisateur pouvait
utiliser, une boîte mail cyrus, un sous-domaine en fdn.{fr,org}, un
domaine à lui, etc.  Il faut également savoir si c'était du forward ou
une boîte locale.

Par exemple, pour un utilisateur ''mdugenou'' qui aurait un
sous-domaine FDN ''marcel.fdn.fr'', on peut obtenir ces informations
avec la commande suivante, en superutilisateur sur Solo :

    $ grep -ER 'mdugenou|marcel' /etc/{postfix,mail,procmailrcs}

Pour les vieux comptes, ça utilise souvent ''fdnprocmail'', une
extension de procmail faite pour les besoins de FDN, la configuration
se trouve dans ''solo:/etc/procmailrcs'', souvent dans deux fichiers,
''marcel'' et ''marcel.rc''.


### Désactivation des mails pour le sous-domaine

La règle qui dit d'utiliser fdnprocmail ou autre chose se trouve dans
''solo:/etc/postfix/transport'', par exemple :

    # mdugenou, adh xxx
    marcel.fdn.fr         fdnprocmail:/etc/procmailrcs/marcel
    .marcel.fdn.fr        fdnprocmail:/etc/procmailrcs/marcel

Pour désactiver le compte, on va commencer par mettre en erreur les
mails pour le domaine, en remplaçant ''fdnprocmail:...'' par
''error:message'', par exemple :

    # Suppression par [admin], le 2014-02-25
    # mdugenou, adh xxx
    marcel.fdn.fr         error:Mailbox does not exist
    .marcel.fdn.fr        error:Mailbox does not exist

Maintenant, on ''compile'' la base de transport, pour informer postfix
des changements :

    $ sudo postmap /etc/postfix/transport

Désormais, postfix va rejeter le mail pour les destinations
''quiconque@marcel.fdn.fr''.  On peut faire un peu de ménage en
supprimant les fichiers dans ''/etc/procmailrcs'' :

    $ rm /etc/procmailrcs/marcel{,.rc}


### Suppression de la boîte mail
  - On peut s'assurer de la non-utilisation de la boîte en consultant les tentatives de connexions dans les journaux :-(
Si ''solo:/etc/mail/user.aliases'' contient une entrée pour notre
M. Dugenou du type :

    # mdugenou aliases-start
    mdugenou: mdugenou@imap.fdn.fr
    # mdugenou aliases-stop

Cela signifie qu'il possède au moins une boîte mail dans ''cyrus''
nommée user.mdugenou.  Il nous faut supprimer cette boîte.  On peut
aller voir de quand datent les derniers messages reçus dans le spool
de cyrus (Les boîtes sont splittées en fonction de la première lettre du login
sans ''user.''.) :

    $ sudo ls -lht /var/spool/cyrus/mail/m/user/mdugenou/ | head -n 5
    total 17M
  -rw------- 1 cyrus mail 1.3K Oct  3  2011 837.
  -rw------- 1 cyrus mail 1.1M Oct  3  2011 cyrus.cache
  -rw------- 1 cyrus mail  44K Oct  3  2011 cyrus.index
  -rw------- 1 cyrus mail 1.1K Aug 27  2011 836.

Pensez à changer juste après ''mail'', ou abusez de
<Tab> si vous êtes root.

Il faut maintenant supprimer la boîte mail.  Postfix fera une erreur
"Mailbox does not exist" automatiquement (il me semble).

Première, étape, se connecter au shell cyrus, comme pour créer un
compte (même mot de passe que MySQL, voir ''/root/.my.cnf'') :

    $ cyradm -user cyradm localhost
    IMAP Password:
    localhost>

On obtient un prompt, on peut alors lister les boîtes de notre
ex-abonné :

    localhost> lm user.mdugenou
    user.mdugenou (\HasNoChildren)

Si vous avez de la chance, il y a pas de sous-dossiers.  Comme
l'exemple pratique qui m'a amené [fulax] à remplir ce tuto n'en avait
pas, ben faudra adapter pour le cas où il y en a, et mettre à jour
cette section (Stéphane n'a pas eu d'erreur en appliquant cette procédure sur une boîte en possédant).

La suppression n'est pas possible directement avec la commande
''deletemailbox'', il faut d'abord nous octroyer le droit de le faire
avec ''setaclmailbox''.
La commande ''lam'' (''listaclmailbox'') affiche les permissions d'une
boîte.
    localhost> lam user.mdugenou
    mdugenou lrswipcda
Nous ajoutons la permission ''c'' (create/delete) à
l'utilisateur ''cyradm'', qui est justement celui avec lequel nous
nous sommes loggés !
    localhost> sam user.mdugenou cyradm c

    localhost> lam user.mdugenou
    cyradm c
    mdugenou lrswipcda



On peut désormais supprimer la boîte :

    localhost> dm user.mdugenou

    localhost>
    ''quit''

A fortiori, pas d'erreurs, donc c'est bon.  On peut vérifier dans le
spool :

    $ sudo ls -lht /var/spool/cyrus/mail/m/user/mdugenou/ | head -n 5
    ls: cannot access /var/spool/cyrus/mail/m/user/mdugenou/: No such file or directory

#### Finalisation de la suppression :
  - Consulter les alias de la boîte dans ''/etc/mail/user.aliases'' 8-)
  - Remplacer l'adresse de la personne dans le SI 8-O
  - Chercher tous les alias repérés précédemment dans Sympa et les remplacer/supprimer 8-o

Boîte mail supprimée, on peut aller virer l'alias dans
/etc/mail/user.aliases, et regénérer les alias :

    $ sudo newaliases

Voilà, plus de boîte pour notre ancien abonné, et ces mails associés à
son sous-domaine sont refusés.

Enfin, pour finaliser les suppressions, on édite /root/Changelog.

    $ sudo $EDITOR /root/Changelog

### Suppression des enregistrements DNS

Sur [[adminsys:serveurs:leia]] cette fois, on va retirer les
enregistrement MX associés aux sous-domaines et domaines hébergés qui
pointent vers [[adminsys:serveurs:solo]] (la suppression complète des
domaines est en dehors de la porté de ce guide, qui ne concerne que
les mails).

En principe, tous les sous-domaines des abonnés sont déclarés dans
''/etc/bind/fdn.subdomains'', un grep sauvage peut aider à les trouver.

    $ grep marcel fdn.subdomains
    marcel        IN      A       198.51.100.42
  *.marcel      IN      A       198.51.100.42
    marcel        MX 10   mail.fdn.fr.
  *.marcel      MX 10   mail.fdn.fr.

Nous allons donc retirer les deux entrées MX.  Une bonne pratique
aurait pu être de mettre un "Null MX record", afin d'annoncer que ce
domaine n'accepte plus de mail, mais la RFC n'a jamais quitté l'état
de draft, donc on va faire sans, et supprimer purement et simplement
les deux entrées, de sorte qu'à la fin, le même grep donne :

    $ grep marcel fdn.subdomains
    marcel        IN      A       198.51.100.42
  *.marcel      IN      A       198.51.100.42
    ; MX marcel commentés par fulax, 2014-02-25
    ;marcel       MX 10   mail.fdn.fr.
    ;*.marcel     MX 10   mail.fdn.fr

(Une conséquence facheuse de ce retrait pur et simple et l'application
du mécanisme de A-record fallback.  S'il un MTA ne trouve pas de MX,
il va contacter la machine indiqué par le RR A.

On met à jour le serial des zones fdn.fr et fdn.org qui utilisent
''fdn.subdomains'' :

    $ sudo -i
    # cd /etc/bind
    # ./update_serial.pl db.fdn.fr
    serial 2013103101 -> 2014022501
    # ./update_serial.pl db.fdn.org
    serial 2014020201 -> 2014022501

(Je sudo -i ou -s parce que sudo ./update_serial.pl semble pas
fonctionner).

On rafraîchit les informations de bind9 :

    # rndc reload
    server reload successful


Reste à patienter une semaine le temps que la réjuvénation DNS se
fasse (le ''Expires'' de fdn.fr est d'une semaine).

    $ sudo $EDITOR /root/Changelog

### La semaine suivante (ou plus tard)

On peut supprimer définitivement les entrées MX commentés dans
fdn.subdomains, remettre à jour le serial de fdn.fr et fdn.org, et
recharger bind9.

Ensuite, sur solo, on va retirer les ''error:Mailbox does not exist''
de /etc/postfix/transport, puis postmap du fichier transport.

Et voilà, plus de mail pour mdugenou ne transite via FDN.
