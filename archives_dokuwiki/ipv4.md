# Ajout d'une plage IPv4 pour un abonné

Chaque abonné ADSL a par défaut une seule adresse IPv4, mais on peut tout à fait lui en fournir plus. La procédure pour ce faire est à la fois administrative et technique. Il faut absolument commencer par la partie administrative, sinon elle reste dans les oubliettes et c'est ingérable.

## Demande : le formulaire RIPE

Un bon conseil : **ne faites pas remplir le formulaire par le demandeur**, c'est le meilleur moyen que ce soit mal fait et que ça lui pose des problèmes ensuite. Remplir le formulaire c'est le travail du LIR qui a lu les docs du Ripe et connait ses exigences : les trois quarts du temps **le demandeur ne sait pas** et vous vous simplifierez la vie en ne lui déléguant pas ce travail.

La première chose est de bien faire comprendre au demandeur qu'on a **besoin de comprendre quand, comment et pourquoi les IPs demandées seront utilisées** pour pouvoir l'expliquer au Ripe.

Ensuite il faut demander à l'abonné de fournit les documents et informations suivants (format texte pour inclusion facile dans un mail) :

    > un doc officiel qui établisse l'existence du demandeur (kbis, extrait de JO, récépissé de préf, carte d'identité)
    > nom légal de l'organisation
    > localisation (« France, trifoulli-les-oies »)
    > site web si dispo
    > description succincte de l'organisation (en anglais)
    > espace déjà dispo pouvant convenir à cet usage (en général il n'y en a pas, mais si l'utilisateur a déjà des IPs il faut se poser la question « lui en reste-t-il qui pourraient servir à cet usage »)
    > espace demandé (/30, /28, etc.)
    > découpage de cet espace selon les usages et usage dans le temps (usage immédiat, intermédiaire, et en fin de période)
    > politique d'assignation pour chacun de ces usages (pour ce qui est des attributions à des client / abonné / « autre qui e soit pas le demandeur »c'est forcément maximum une IP par personne)
    > explications (en anglais) sur chacun des usages ci-dessus
    > liste des équipements utilisés pour l'infrastructure (nom + fabricant + modèle + commentaire/rôle) : quelques infos  essentielles suffisent mais si vous avez prévu qu'une partie des IPs sont utilisées pour votre infra, il faut que ca puisse correspondre
    > un plan du réseau (si c'est un peu compliqué)


Avec ces informations, si faut ensuite se tourner vers un LIR qui va mettre tout ça en forme dans le [[http://www.ripe.net/docs/iprequestform.html|le formulaire RIPE]] pour justifier de l'utilisation des adresses IP demandées. 

Il est possible de préparer le travail en suivant les [[http://www.ripe.net/docs/ripe-489.html|notes indicatives]] (ripe-489 ou plus récent) à conditions d'avoir préalablement lu et compris les Polices du Ripe, notamment la [[http://www.ripe.net/ripe/docs/ipv4-policies.html|politique de gestion des IPv4 du Ripe]]. Sinon il faut mieux s'abstenir.


## Le LIR, quel LIR ?

Il existe plusieurs LIRs capables de faire des demandes auprès du Ripe, et le choix dépend de plusieurs critères. En premier lieu, le LIR d'un utilisateur de FDN n'a pas forcément à être celui de tout le monde. 

Les critères à prendre en compte lors du dialogue avec le demandeur incluent notamment 
  * le routage et la routabilité,
  * l'indépendance (politique, technique),
  * la tarification des services,
  * la disponibilité des ressources (et pour un élargissement futur), 
  * la localisation géographique,
  * la convention
c'est pourquoi il est **nécessaire** d'avoir bien compris et évalué la problématique du demandeur et de comprendre les implications de ce choix (et donc de ne pas se contenter de lui refiler le formulaire à remplir).

Faites-vous conseiller sur IRC par des personnes qui ont de l'expérience dans ce domaine si vous avez un doute.

Ensuite une personne « habilitée » dans le LIR (re)valide la demande, l'archive, et choisit en fonction des ressource disponibles un subnet pour l'assigner à l'utilisateur. Ou en fait la demande au Ripe, notamment dans le cas de ressources indépendantes (provider independant, PI).

Ceci consiste notamment à renseigner la base whois du Ripe avec les objets qui vont décrire le subnet et la personne à qui il est assigné. Pour plus d'informations sur la base du Ripe voir [[http://www.ripe.net/db/docs.html|ici]].


## Publication : le Whois

La plage d'adresses qui va être assignée à l'utilisateur par le LIR doit être renseignée dans la base publique Whois du Ripe. Ceci se fait au moyen d'un objet « inetnum » et d'un ou plusieurs objets « person », éventuellement d'un objet « organisation ».

Ils sont décrits ci-dessous. Les champs « mandatory » sont obligatoires, les champs « multiple » peuvent être répétés autant de fois que nécessaire (par exemple pour mettre une adresse sur plusieurs lignes).

Il faudra récupérer auprès du demandeur, au moins les informations nécessaires à remplir les champs « mandatory » ci-dessous.

NOTE: certains champs sont pré-remplis ci-dessous. Ceux qui contiennent « AUTO-1 » seront remplacés par une référence attribuée par le RIPE. Vous pouvez spécifier jusqu'à 4 lettres sous la forme AUTO-1abcd, qui seront reprises dans la référence générée et vous aideront à la mémoriser.

### Inetnum

C'est le descriptif de la plage d'IPs assignée, se compose ainsi.

    inetnum:        [mandatory]  [single]     [la plage d'adresse assignée] 
    netname:        [mandatory]  [single]     [valeur indiquée dans le ripe-488]
    descr:          [mandatory]  [multiple]   [ ]
    country:        [mandatory]  [multiple]   [ ]
    org:            [optional]   [single]     [inverse key]
    admin-c:        [mandatory]  [multiple]   [inverse key]
    tech-c:         [mandatory]  [multiple]   [inverse key]
    status:         ASSIGNED PA
    remarks:        [optional]   [multiple]   [ ]
    notify:         [optional]   [multiple]   [inverse key]
    mnt-by:         Gitoyen-NCC
    changed:        root@gitoyen.net
    source:         RIPE

À noter qu'il y a deux champs ''admin-c'' et ''tech-c'' qui désignent respectivement des personnes, responsable administratif et responsable technique. Il faut les compléter avec les références (nic-hdl) qui auront été attribués par le Ripe à la création d'objets de type « person ».

=#### Person

Désigne une personne physique.

    person:         [mandatory]  [single]    [nom prénom]
    address:        [mandatory]  [multiple]   [ ]
    phone:          [mandatory]  [multiple]   [ ]
    fax-no:         [optional]   [multiple]   [ ]
    e-mail:         [optional]   [multiple]   [lookup key]
    org:            [optional]   [multiple]   [inverse key]
    nic-hdl:        AUTO-1
    remarks:        [optional]   [multiple]   [ ]
    notify:         [optional]   [multiple]   [inverse key]
    abuse-mailbox:  [optional]   [multiple]   [inverse key]
    mnt-by:         Gitoyen-NCC
    changed:        root@gitoyen.net
    source:         RIPE

Il y a aussi un champ « org » pour « organisation » qui peut vous permettre de décrire un peu une personne morale

### Organisation

Elle est décrite par un objet comme suit :

    organisation:   AUTO-1
    org-name:       [mandatory]  [single]     [lookup key]
    org-type:       [mandatory]  [single]     [ ]
    descr:          [optional]   [multiple]   [ ]
    remarks:        [optional]   [multiple]   [ ]
    address:        [mandatory]  [multiple]   [ ]
    phone:          [optional]   [multiple]   [ ]
    fax-no:         [optional]   [multiple]   [ ]
    e-mail:         [mandatory]  [multiple]   [lookup key]
    org:            [optional]   [multiple]   [inverse key]
    admin-c:        [optional]   [multiple]   [inverse key]
    tech-c:         [optional]   [multiple]   [inverse key]
    ref-nfy:        [optional]   [multiple]   [inverse key]
    mnt-ref:        [mandatory]  [multiple]   [inverse key]
    notify:         [optional]   [multiple]   [inverse key]
    abuse-mailbox:  [optional]   [multiple]   [inverse key]
    mnt-by:         Gitoyen-NCC
    changed:        root@gitoyen.net
    source:         RIPE

Là aussi des contacts administratifs et technique sont requis, ça peut être les mêmes personnes (voire la même personne) que dans l'inetnum.

## Activation technique

Côté RADIUS FDN, il faut ajouter un attribut Framed-Route avec dedans le subnet à router. 

aller dans le SI, trouver le membre (par son numéro de tel ou d'adhérent)
puis sa ligne, (view-ligne.cgi?lid=<id>&do=yes)
puis son compte radius (view-raduser.cgi?uid=<id>&do=yes)

de là on va pouvoir lui ajouter un bloc d'IP (ici un /29) pour son compte.

en face de "Attributs de l'utilisateur" cliquer sur "Ajouter" et remplir
le formulaire comme suit :
(page new-uattr.cgi?uid=<id>&from=raduser<id>)

Création/modification d'un attribut radius utilisateur

    Nom de l'attribut    Framed-Route
    Opérateur         =
    Valeur de l'attribut    80.67.160.96/29
    Type                    reply
    User id                (prérempli)

Côté routage, a priori, il n'y a rien à faire de particulier chez FDN ni chez Gitoyen.

Côté abonné, il n'y a plus qu'à utiliser les IP de ce subnet (probablement configurer en conséquence le "routeur ADSL"). FIXME  => un exemple concret...

On peut ruser un peu pour ne pas « gâcher » les adresses IP de réseau et de broadcast FIXME => exemple concret... FIXME => ça ne semble pas très clean


## Compléments / Extra

(d'autres infos, à finir de convertir vers cette page, dans un [[https://lists.fdn.fr/wws/arc/adminsys/2010-07/msg00021.html|mail de Benjamin S sur adminsys]])

