En attendant remise en forme, faisons simple : copier-coller d'un mail de Vincent.

<file>
Date: Tue, 28 Sep 2010 17:47:43 +0200
From: Vincent Bernardoff <vb@vb.fdn.fr>
To: FDN Adminsys <adminsys@fdn.fr>
Subject: Service Jabber!
Message-ID: <20100928154743.GA22998@vb.fdn.fr>


Hello,

Bon, j'ai fait les modifs dont on avait parlé il y a un bail
concernant le serveur jabber. Voilà l'état du truc, pour le moment.

- Le serveur est jabber.fdn.fr, Xen sur je sais pas quelle machine.

- Le serveur utilise ejabberd (un vrai plaisir à configurer pour moi,
    excellent soft, etc. etc.).

- Le serveur utilise MySQL comme base de données. Tout est stocké là
    dessus.

- MySQL est installé en local sur jabber.fdn.fr

- Le serveur dessert deux hostnames, jabber.fdn.fr et fdn.fr

- Les utilisateurs de ces deux domaines sont respectivement stockés
    dans les bases ejabberd et ejabberd_fdn du MySQL sus mentionné.

- L'enregistrement est ouvert à tous pour jabber.fdn.fr, fermé à tous
    pour fdn.fr (pour le moment).

- Pour ajouter des utilisateurs sur fdn.fr, il faudrait hooker ça sur
    le SI (pas envie de faire ça, j'y connais rien, mais ça devrait être
    facile).

- Le serveur dispose de passerelles vers MSN, ICQ, Yahoo, et QQ (le
    truc chinois, ça doit pas marcher terrible ça). Le prog utilisé est
    Spectrum (qui gère d'ailleurs toutes les passerelles à lui tout
    seul).



J'ai fait un gros nettoyage sur jabber.fdn.fr, j'avais installé un peu
n'importe quoi n'importe comment et y'avait des milliers de paquets
qui servaient à rien. Maintenant, y'a plus qu'une installe
minimaliste, plus de paquets inutiles.

TODO:
* Hooker fdn.fr au SI
* Régler le problème de certificat (lorsqu'on essaye de s'enregistrer
sur FDN.fr, on se récupère un certificat pour jabber.fdn.fr et ça
gueule).
* Sauvegardes des DB?
* Updater le wiki (je ferai plus tard).

Pour le moment, pas grand chose à dire de plus que
/etc/init.d/ejabberd start pour démarrer, etc... tout marche tout seul après.

--
Vincent
</file>

