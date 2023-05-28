### news

Le serveur `news.fdn.fr` est accessible sans authentification depuis toutes
les adresses IP FDN (xDSL ou VPN). Depuis le reste du monde, il est accessible
en s'authentifiant avec ses identifiants xDSL ou VPN.

Il est hébergé sur [solo](./infra/machines/solo.md). Le logiciel utilisé est
[INN](https://www.eyrie.org/~eagle/software/inn/).

Infos utiles pour son administration dans [les archives](./archives/archives_dokuwiki/usenet.md)

#### Ajout d'utilisateur statique

Pour les adhérents qui n'ont pas d'accès xDSL/FTTH/VPN, on peut créer des compte à la main.

Il suffit de le rajouter dans /etc/news/users de solo au format `user:hash`, avec le hash en sha512crypt tel que généré par la commande `mkpasswd -m sha512crypt`

Le login sera `user@fdn.fr` (donc c'est bien de vérifier rapidement qu'on n'a pas de collision avec le mail de quelqu'un d'autre).
