## Comptes POP/IMAP

*Note : ceci est un rafraichissement de l'ancienne page dokuwiki sur la gestion des comptes POP/IMAP, plusieurs vérifications ont été menées lors de cette transposition, il y a pu également avoir des suppressions. si une info vous manque, vous pouvez toujours consulter l'[archive dokuwiki](./archives/archives_dokuwiki/services/comptesmail.md) de cette page.*

# Création d'un compte mail

## Informations nécessaires pour procéder à la création de compte

Les informations nécessaires pour la création d'un compte mail sont :

- numéro adhérent
- abonnement(s)
- adresse souhaitée
- cette nouvelle adresse est-elle à utiliser pour les listes de discussion ? le SI ?

S'il s'agit du premier compte mail pour la personne demandeuse, il faut en plus :

- vérifier qu'elle est bien adhérente
- vérifier qu'elle est abonnée aux services
- nom et prénom de la personne (pour la création du compte unix, vous devrez alors suivre la [convention de nommage](./howto/conventions.md) pour composer le login)
- une clé SSH publique (facultative) de la personne demandeuse (dans le setup actuel, l'utilisateur doit se connecter en SSH à solo pour changer son mot de passe)
- un mot de passe aléatoire pour le nouvel utilisateur (*pwgen* ou *apg* ou *makepasswd* peuvent vous en générer un, par exemple)

## Premier compte email pour la personne demandeuse

Vous avez maintenant toutes les informations nécessaires pour créer le compte unix de cette personne.

### Création du compte unix sur solo

Prenons en exemple, le cas de l'adhérent *Marcel Dugenou* ayant le numéro d'adhérent 666.

Son login est donc *mdugenou* et son UID est donc *10066*.

On se connecte alors sur solo et on crée son compte :

```bash
ssh gentiladmin@solo.fdn.fr
sudo adduser --ingroup users --uid 10666 --gecos "Marcel Dugenou" mdugenou
```

Si l'utilisateur a fourni sa clé SSH publique, on l'ajoute à son compte.

Toujours en gardant l'exemple de Marcel Dugenou :

```bash
$ sudo mkdir /home/mdugenou/.ssh
$ sudo touch /home/mdugenou/.ssh/authorized_keys
$ sudo chown -R mdugenou:users /home/mdugenou/.ssh
$ sudo chmod 0700 -R /home/mdugenou/.ssh
$ sudo chmod 0600 /home/mdugenou/.ssh/authorized_keys
```

puis, coller sa clé dans */home/mdugenou/.ssh/authorized_keys*.

Nous utilisons [Cyrus](https://cyrusimap.org/) pour fournir de l'IMAP à nos utilisateurs et [Postfix](http://www.postfix.org/) pour la partie SMTP.

Quelques ressources utiles sur Cyrus :

* [https://cyrusimap.org/imap/reference/manpages/systemcommands/imapd.html?highlight=imapd](https://cyrusimap.org/imap/reference/manpages/systemcommands/imapd.html?highlight=imapd)

Nous allons d'abord configurer Cyrus, puis nous passerons à la configuration de Postfix.

### Configuration de Cyrus

Pour les opérations liées à Cyrus, vous aurez besoin du mot de passe de l'utilisateur *cyradm*. vous pourrez le trouver dans */root/.my.cnf*.

Vous pourrez alors vous connecter à la console d'administration avec la commande :

```bash
$ cyradm -user cyradm localhost
IMAP Password: ***************
localhost>
```

Avant de créer l'adresse email, on vérifie si celle-ci n'existe pas déjà :

```bash
localhost> lm user.%
```

Si l'adresse est libre (non listée par la commande précédente), on procède à sa création :

```bash
localhost> createmailbox user.mdugenou
localhost> quit
$
```

**ATTENTION à ne pas oublier le préfixe "user." !** : Le nom qui se situe derrière est le même que celui créé au niveau système.

On peut alors passer à la configuration de Postfix, on doit lui indiquer qu'il a une nouvelle adresse à gérer.

### Configuration de Postfix

Pour ce faire, éditer le fichier */etc/mail/user.aliases* en ajoutant les lignes suivantes (à adapter à votre cas, indeed) :

```
# mdugenou aliases-start
mdugenou: mdugenou@imap.fdn.fr #Il faut seulement remplacer "mdugenou" par le nom utilisé dans Cyrus dans le cas que l'on traite, elle sera accessible aussi bien en POP qu'en IMAP
marcel.dugenou: mdugenou #Cette ligne, optionnelle, permet de créer un alias : elle signifie que l'adresse courriel marcel.dugenou@fdn.fr renverra vers mdugenou@fdn.fr
# mdugenou aliases-stop
```

Et enfin, comme à chaque fois que la liste des alias est modifiée :

```bash
$ sudo newaliases
```

Et pour finir, faire le commit etckeeper :

```bash
$ sudo etckeeper commit "Ajout mail mdugenou"
```

### Prévenir la personne demandeuse que son email est créé, via un courriel sur l'adresse utilisée pour la demande avec copie vers la nouvelle

Exemple de message envoyé par Hamster :

```
Ton adresse est faite :
''mdugenou@fdn.fr''
* Ton identifiant de connexion est : ''mdugenou''
* Ton mot de passe est : ''toto''
* Tu peux changer ton mot de passe avec la commande passwd en te connectant en ssh sur solo.fdn.fr. Les connexions ssh se font uniquement par clef et non pas par mot de passe ; si ça ne marche pas c'est que j'ai mal mis ta clef, reviens donc vers nous. Si ça te gonfle, tu peux aussi demander qu'on t'en mette un autre en nous disant lequel (il est preferable de pas choisir un mot de passe trop simple, genre surtout pas "toto").

Tu peux te connecter :
- par le webmail : webmail.fdn.fr
- en POP ou en IMAP : mail.fdn.fr(port 143 pour l'imap, port 110 pour le pop, starttls, mot de passe non chiffré)

Pour envoyer du courrier, tu peux utiliser smtp.fdn.fr (port 587, pratique si le port 25 est bloqué, starttls, mot de passe non chiffré)

Les certificats utilisés par FDN sont signés par l'autorité CACert, qui n'est pas forcément présente par défaut sur toutes les machines.

Il peut donc falloir que tu importes le certificat racine Class 3 de CACert (en pièce jointe, je te laisse trouver le bon format pour ton logiciel) ou alors que tu acceptes l'exception de sécurité. Sinon, tu peux aussi repasser sur une connexion non chiffrée (sans STARTTLS), mais c'est moins bien. N'hésite pas à revenir vers nous en cas de pépin, en laissant bien adminsys@fdn.fr dans les destinataires pour maximiser les chances de réponse :)

*Pour mettre le certificat en piece jointe, on peut aller le chercher la : https:*www.cacert.org/index.php?id=3
```

Dans le cas où un ou plusieurs alias a/ont été créé(s), préciser :

```
Tu as une et une seule boite mail, et 2 adresses qui arrivent toutes les deux dans la meme boîte, donc une seule boîte à configurer comme indiqué ci-dessus ; tu y trouveras les messages envoyés à ''mdugenou@fdn.fr'' et ceux à ''marcel.dugenou@fdn.fr''

Si tu veux envoyer des messages depuis l'adresse ''mdugenou@fdn.fr'' il faut que tu ailles "gérer les identites" dans l'outil de gestion de courriels : webmail, thunderbird (dans "Édition" puis "Paramètres des comptes") ...

Au moment ou tu rediges un message, tu peux choisir quelle identité utiliser.
```

## Mail additionnel pour une personne ayant déjà un compte mail chez FDN

Dans ce cas, il vaut mieux créer un [sous-domaine](./dns.md), ce qui peut donner michu@dugenou.fdn.fr.

Se baser sur les comptes présents dans */etc/postfix/virtusertable* par exemple :

```
# Philippe Michel (576)
michel.fdn.fr   anything
philippe@michel.fdn.fr  pmichel@imap.fdn.fr
come@michel.fdn.fr      cmichel@imap.fdn.fr
aude@michel.fdn.fr      amichel@imap.fdn.fr
enfant.dysphasie@michel.fdn.fr  philippe@michel.fdn.fr
```

Donc, créer les différents comptes voulus, comme les classiques @fdn.fr, puis remplir virtusertable :

```
domaine  chaine quelconque
a@domaine a-fdn@imap.fdn.fr
b@domaine b-fdn@imap.fdn.fr
c@domaine c-fdn@imap.fdn.fr
```

Enfin :

```bash
$ cd /etc/postfix
$ sudo make
```

C'est fait.

Pour ce qui est des domaines de listes de diffusion il y a plusieurs
exemples disponibles.

Voir par exemple : 

* */etc/sympa/lists.ffdn.org/*
* */etc/postfix/virtual-ffdn*

```bash
$ grep ffdn /etc/mail/sympa/aliases
```

# Suppression d'un compte mail

Les informations nécessaires pour supprimer un compte email sont :

* l'adresse email à supprimer

## Vérifications avant suppression

Il faut préalablement trouver tout ce que l'utilisateur pouvait utiliser, une boîte mail cyrus, un sous-domaine en fdn.{fr,org}, un domaine à lui, etc. Il faut également savoir si c'était du forward ou une boîte locale.

Par exemple, pour un utilisateur *mdugenou* qui aurait un sous-domaine FDN *marcel.fdn.fr*, on peut obtenir ces informations avec la commande suivante, en superutilisateur sur Solo :

```bash
$ grep -ER 'mdugenou|marcel' /etc/{postfix,mail,procmailrcs}
```

Pour les vieux comptes, ça utilise souvent *fdnprocmail*, une extension de procmail faite pour les besoins de FDN, la configuration se trouve dans *solo:/etc/procmailrcs*, souvent dans deux fichiers, *marcel* et *marcel.rc*.

On peut s'assurer de la non-utilisation de la boîte en consultant les tentatives de connexions dans les journaux.

Chercher l'adresse mail à supprimer dans */etc/mail/user.aliases* (sur solo) ; dans le cas de M. Dugenou, on devrait trouver quelque chose comme :

```
# mdugenou aliases-start
mdugenou: mdugenou@imap.fdn.fr
# mdugenou aliases-stop
```

*mdugenou@imap.fdn.fr* nous indique qu'il existe un boîte gérée par *Cyrus*. Cette boîte est nommée *user.mdugenou*.

C'est cette boîte qu'on veut donc supprimer.

Pour voir quand sont arrivés les derniers messages pour cette boîte mail, on peut aller voir */var/spool/cyrus/mail/m/user/mdugenou/*.

*Note : Cyrus trie les boîtes mails selon la première lettre du nom d'utilisateur, ici "m"*

```bash
$ sudo ls -lht /var/spool/cyrus/mail/m/user/mdugenou/ | head -n 5
total 17M
-rw------- 1 cyrus mail 1.3K Oct  3  2011 837.
-rw------- 1 cyrus mail 1.1M Oct  3  2011 cyrus.cache
-rw------- 1 cyrus mail  44K Oct  3  2011 cyrus.index
-rw------- 1 cyrus mail 1.1K Aug 27  2011 836.
```

On peut maintenant passer à la suppression de la boîte dans Cyrus (nous ne redétaillons pas ici la procédure pour utiliser cyradm, vous la trouverez plus haut dans cette page).

## Désactivation des mails pour le sous-domaine

La règle qui dit d'utiliser fdnprocmail ou autre chose se trouve dans *solo:/etc/postfix/transport*, par exemple :

```
# mdugenou, adh xxx
marcel.fdn.fr         fdnprocmail:/etc/procmailrcs/marcel
.marcel.fdn.fr        fdnprocmail:/etc/procmailrcs/marcel
```

Pour désactiver le compte, on va commencer par mettre en erreur les mails pour le domaine, en remplaçant *fdnprocmail:...* par *error:message*, par exemple :

```
# Suppression par [admin], le 2014-02-25
# mdugenou, adh xxx
marcel.fdn.fr         error:Mailbox does not exist
.marcel.fdn.fr        error:Mailbox does not exist
```

Maintenant, on *compile* la base de transport, pour informer postfix des changements :

```bash
$ sudo postmap /etc/postfix/transport
```

Désormais, postfix va rejeter le mail pour les destinations *quiconque@marcel.fdn.fr*.

On peut faire un peu de ménage en supprimant les fichiers dans */etc/procmailrcs* :

```bash
$ rm /etc/procmailrcs/marcel{,.rc}
```

## Suppression de la boîte dans Cyrus

```bash
localhost> lm user.mdugenou
user.mdugenou (\HasNoChildren)
```

ici, la commande lm (listmailbox) indique que la boîte mail existe bien.

Même si nous utilisons l'utilisateur administrateur de Cyrus, nous ne sommes pas autorisés à supprimer une boîte email par défaut.

Pour cela, il nous faut modifier les ACL (Access Lists) de cette boîte en donnant à notre utilisateur le droit "c" ("create", qui sous-entend qu'on peut aussi supprimer).

Pour vérifier les ACL d'une boîte mail :

```bash
localhost> lam user.mdugenou
mdugenou lrswipcda
```

Comme on peut le voir, notre utilisateur *cyradm* n'a aucun droit sur cette boîte.

Ajoutons, avec la commande *sam* (ou *setaclmailbox*), les droits de création/suppression pour l'utilisateur *cyradm* :

```bash
localhost> sam user.mdugenou cyradm c
```

Notre utilisateur *cyradm* doit avoir de nouveaux droits pour cette boîte :

```bash
localhost> lam user.mdugenou
cyradm c
mdugenou lrswipcda
```

On peut désormais supprimer la boîte :

```bash
localhost> dm user.mdugenou
localhost> quit
```
On peut vérifier dans le spool que la boîte a bien été supprimée :

```bash
$ sudo ls -lht /var/spool/cyrus/mail/m/user/mdugenou/ | head -n 5
ls: cannot access /var/spool/cyrus/mail/m/user/mdugenou/: No such file or directory
```

## Suppression de l'alias pour cette boîte mail

Dans le fichier */etc/mail/user.aliases*, supprimer les alias repérés précédemment.

Faire le tour du SI et de sympa pour s'assurer que cette boîte mail n'est plus utilisée.

Chercher également les autres alias pouvant pointer sur la boîte mail supprimée et les remplacer/supprimer.

Pensez à regénérer les alias :

```bash
$ sudo newaliases
```

Voilà, plus de boîte pour notre ancien abonné, et les mails associés à son sous-domaine sont refusés.

Enfin, pour finaliser les suppressions, on fait un commit *etckeeper*.

## Suppression des enregistrements DNS

Dans le cas de la suppression d'un mail lié à un sous-domaine, il faudra retirer les enregistrements MX associés.

Voir la documentation sur le [dns](./dns.md).

Une conséquence fâcheuse de ce retrait pur et simple est l'application du mécanisme de A-record fallback. Si un MTA ne trouve pas de MX, il va contacter la machine indiqué par le RR A.

Comme d'habitude, commit *etckeeper*.

La semaine suivante (ou plus tard)

On peut supprimer définitivement les entrées MX commentés dans fdn.subdomains, remettre à jour le serial de fdn.fr et fdn.org, et recharger bind9.

Ensuite, sur solo, on va retirer les *error:Mailbox does not exist* de */etc/postfix/transport*, puis postmap du fichier transport.

Et voilà, plus aucun mail pour mdugenou ne transite via FDN.

## Suppression du compte unix

Si d'aventure la suppression de l'email est liée au départ d'un adhérent, qu'il n'y a plus de signe de vie de lui et qu'il a récupéré ses données, il est possible de supprimer son compte unix :

```bash
$ sudo deluser --remove-home mdugenou
```

