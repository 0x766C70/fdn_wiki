
Nous utilisons etckeeper sur toutes les machines gérées par puppet. Il est
installé via puppet.

Etckeeper permet de conserver un historique du répertoire `/etc`. La commande
suivante permet d'enregistrer chaque modification.

    sudo etckeeper commit

Le fichier `/etc/etckeeper/bashrc`, inclu dans le `.bashrc` permet de faire en
sorte que :

* un point d'exclamation s'affiche dans l'invite de commande lorsque une
  modification non commitée est présente dans /etc.

* un message d'avertissement s'affiche lorsque l'on sort du shell.
