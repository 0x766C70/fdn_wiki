
Pour se simplifier la vie lors des mises à jour des serveurs, on peut utiliser l'outil apt-dater.

## Accéder à l'outil

L'outil apt-dater est installé sur [[infra/machines/obiwan]]. Pour s'en servir, il faut se connecter en tant que `apt-dater` :

    ssh apt-dater@obiwan.fdn.fr

Il faut donc avoir sa clé ssh dans le `authorized_keys` de l'utilisateur `apt-dater`. Les roots peuvent le faire pour eux-même.

Ensuite, l'outil se lance avec la commande :

    apt-dater@obiwan.fdn.fr:~$ apt-dater

