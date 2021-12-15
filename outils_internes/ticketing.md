# Request Tracker

[Request Tracker](https://bestpractical.com/request-tracker/) est un outil (Perl) de suivi des demandes utilisateur, très modulable, pouvant être piloté via une interface web ou mail.

Pour plus d'informations :

- le [wiki](https://rt-wiki.bestpractical.com/wiki/Main_Page) de Best Practical
- la [documentation](https://docs.bestpractical.com/rt/4.4.3/index.html)
- le [forum](https://forum.bestpractical.com/)

L'interface utilisateur est accessible à l'url [tickets.fdn.fr](https://tickets.fdn.fr/rt/).

Le serveur hébergeant la solution est [[infra/machines/jira]].


## Principe de fonctionnement

### Lexique

- demandeur (*requestor*) : personne qui effectue une demande
- file (*queue*) : regroupement des tickets pour un type de problème donné
- AdminCC : personnes responsables de gérer une file


### Fonctionnement de base

#### Réponses aux demandes

Imaginons que tous les mails envoyés à **contact@fdn.fr** sont redirigés vers une file de RT intitulée **contact**. Lorsqu'une personne recherche des informations concernant FDN, le demandeur, elle envoie un mail à **contact@fdn.fr**. RT récupère ce mail et :

- l'analyse
- crée un ticket dans la file **contact**
- envoie un mail au demandeur pour le notifier que sa demande est bien arrivée
- envoie un mail à tous les AdminCC de cette file pour les informer de l'arrivée d'une nouvelle demande.

Un des AdminCC répond alors au mail via l'adresse **contact@fdn.fr**. RT récupère la réponse et :

- l'analyse
- assigne le ticket à l'AdminCC qui a répondu en premier
- transfère la réponse au demandeur
- envoie une copie de la réponse aux AdminCC (avec quelques informations complémentaires)

Le demandeur peut alors répondre et... ainsi de suite.

Pour tous ces échanges, une seule adresse mail a été utilisée : il n'est pas nécessaire de faire répondre à tous ou de mettre les autres AdminCC en copie, c'est RT qui s'occupe de dispatcher les mails à qui de droit.

> Note : pour s'y retrouver, RT utilise le numéro dans le sujet du mail (plus d'autres en-têtes) donc il faut éviter de le modifier sous peine de se retrouver avec un nouveau ticket...

#### Interface web

Pour celleux qui le souhaitent, il est tout à fait possible de gérer les tickets via l'interface web (IHM), sans utiliser les mails. Lorsque vous vous connectez à l'interface, vous arrivez sur la page listant les files auxquelles vous avez accès ainsi que certains tickets de la file (cette page est personnalisable). En cliquant sur un ticket, vous avez le détail de celui-ci. Description rapide des différents onglets qui permettent de faire des modifications :

- Afficher (*Display*) : un résumé du ticket ;
- Historique (*History*) : évolution du ticket (tout est logué) ;
- Essentiel (*Basics*) : modification de l'intervenant, du statut, de la file, des champs personnalisés, etc. ;
- Personnes (*People*) : modification des destinataires des mails (demandeur, personnes en copie) ;
- Dates (*Dates*) : date de début, échéance, etc. ;
- Relations (*Links*) : permet de lier des tickets entre eux ou de les fusionner ;
- Tout (*Jumbo*) : :-x ;
- Rappels (*Reminders*) : possibilité de rajouter des rappels sur certains tickets, rappels qui apparaissent sur la page d'accueil ;
- Actions (*Actions*) : utilisé pour envoyer des mails depuis l'IHM et modifier certains champs au même moment.

> Note : Attention à bien réfléchir avant de fusionner des tickets parce que dans ce cas les historiques sont fusionnés et il est impossible de les séparer de nouveau. On utilise cette fonctionnalité par exemple quand il y a eu un nouveau ticket créé parce que quelqu'un n'a pas utilisé la bonne adresse mail.

> Note 2 : il est possible de répondre, transférer et commenter à partir de n'importe quel message présent dans le ticket, les actions depuis le menu *Actions* utilisent le dernier message.

#### Statuts

Les différents statuts qu'un ticket peut avoir sont :

- nouveau (new) : ticket vierge ;
- ouvert (open) : quelqu'un a déjà travaillé dessus ;
- stagnant (stalled) : en attente de quelque chose... ;
- résolu (resolved) : terminé ;
- rejeté (rejected) : ticket non pris en compte et pouvant être affiché dans RT ;
- effacé (deleted) : ticket non pris en compte et indisponible à l'affichage dans RT (principalement spams ou tickets de tests).

> Note : les tickets effacés sont régulièrement supprimés de la base de données et donc ne seront jamais récupérables.

#### Commentaires

Il est possible de n'envoyer un mail qu'aux autres AdminCC, sans que le demandeur n'ait de copie du mail, pour échanger entre nous si besoin. Pour cela, il suffit d'envoyer, dans le cas présent, un mail à **contact-comment@fdn.fr**.

#### Astuces / Problèmes connus

Si vous obtenez le message d'erreur suivant en voulant fusionner deux tickets :
> An internal RT error has occurred. Your administrator can find more details in RT's log files.

C'est que **services@fdn.fr** est en demandeur (*requestor*) sur le ticket, il suffit de le supprimer via l'onglet Personnes (*People*) avant de réessayer.

### Fonctionnement avancé

#### Contrôle par mail

De nombreuses fonctionnalités sont accessibles depuis l'IHM, comme par exemple le changement de statut, de file, de owner, etc. Nous avons mis en place des *scrips* pour pouvoir faire cela, pour les tâches les plus courantes, via les mails. Les modifications actuellement disponibles sont les suivantes :

- `Set-Owner: bidule` : définit qui prend en charge le ticket ;
- `Set-Queue: contact` : place le ticket dans une autre file, si on en a le droit bien sûr ;
- `Set-Status: resolved` : change le statut du ticket


#### Envoi de mail depuis l'IHM

Supposons que nous voulions envoyer un mail à tartempion@fdn.fr parce que son adresse postale n'est pas valide (NPAI) :

1. créer un ticket dans la file qui va bien :
   - demandeur : enlever, doit être vide (au risque d'envoyer un mail de confirmation de prise en compte à quelqu'un qui n'a rien demandé)
   - sujet : adresse invalide Tartempion
   - description : reçu un NPAI, adresse à confirmer
1. modifier les utilisateurs du ticket :
   - demandeur : tartempion@fdn.fr
1. répondre au ticket en remplissant avec le texte du mail que vous souhaitez envoyer à Tartempion

Ce dernier recevra alors le mail, pourra y répondre, et le flux standard de gestion des tickets pourra reprendre.

## Organisation FDN

### Support

- Objet : toutes les demandes concernant les incidents techniques rencontrés par les adhérents (accès adsl, vpn, mais, etc.)
- Adresse mail de contact : support@fdn.fr
- Adresse mail de commentaires : support-comment@fdn.fr
- File RT : support
- AdminCC : Équipe-support

### Secrétariat

*Définition en cours*

- Objet : toutes les demandes à destination des secrétaires
- Adresse mail de contact : 
- Adresse mail de commentaires : 
- File RT : secrétariat
- AdminCC : Secrétaires

> Note : seuls les secrétaires ont accès à cette file (file privée).

### Trésorerie

*Définition en cours*

- Objet : toutes les demandes à destination des trésoriers
- Adresse mail de contact : tresorier@fdn.fr
- Adresse mail de commentaires : tresorier-comment@fdn.fr
- File RT : treso
- AdminCC : Trésoriers (accès réservé)

> Note : seuls les trésoriers ont accès à cette file (file privée).

### Services

- Objet : toutes les demandes de mise en place de nouveau service pour les adhérents (accès adsl, adresse mail, configuration DNS, hébergement mutualisé, etc.)
- Adresse mail de contact : services@fdn.fr
- Adresse mail de commentaires : services-comment@fdn.fr
- File RT : services
- AdminCC : Services-adm

Services est le point d'entrée par défaut pour toutes les demandes ne concernant pas les demandes précédentes ;). Les tickets créés dans cette file sont triés par les gentils bénévoles du groupe Services-adm. Ce tri se fait par le déplacement des tickets vers d'autres files auxquelles d'autres groupes sont associés en AdminCC (entre parenthèses) :

- services-dns (Équipe-dns) : demandes concernant la configuration des DNS (délégation, etc)
- services-im (Équipe-im) : demandes concernant les outils de messagerie instantannée (XMPP, IRC, Matrix)
- services-mails (Équipe-mails) : demandes concernant la mise en place d'une adresse mail ou la gestion de listes de diffusion (aka listmaster)
- services-vpn (Équipe-vpn) : demandes concernant le service vpn
- services-web-mutu (Équipe-web-mutu) : demandes concernant l'hébergement mutualisé
- services-xdsl (Équipe-xdsl) : demandes concernant les accès xdsl
- services-other (Équipe-adminsys) : toute autre demande non spécifiée dans les catégories précédentes
 
Ces groupes n'ont pas pour but de cloisonner l'intervention des bénévoles parce que chacun a la possibilité d'aller voir et de prendre en charge les tickets de service et de support, même s'il ne fait pas partie du groupe initialement défini. Cela a pour but d'éviter que ceux qui n'ont pas les accès particuliers (accès à la machine de mails, au SI, etc.) ne reçoivent les demandes qui ne les concernent pas.

Tous les bénévoles font également partie d'un groupe **Bénévoles** et ont tous les mêmes accès aux tickets. Seuls quelques-uns appartenant à un groupe **Administrateurs** ont accès à la configuration de RT et à **toutes** les files.
