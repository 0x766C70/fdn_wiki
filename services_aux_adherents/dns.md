[[_TOC_]]

## Généralités

Historiquement, les serveurs de FDN faisant authorité étaient *[ns0.fdn.org - 80.67.169.12](./infra/machines/leia.md)* et *[ns1.fdn.org - 80.67.169.40](./infra/machines/vador.md)*.

Depuis la mise en place des droïdes, les serveurs faisant autorité pour FDN sont *[nsa.fdn.fr](./infra/machines/nsa.md)* et *[gchq.fdn.fr](./infra/machines/gchq.md)*. Ces serveurs sont hébergés sur le cluster ganeti dans des VM éponymes.

Les zones DNS sont gérées dans [git](https://git.fdn.fr/), dans le groupe *dns*. Pour les modifier, cloner le dépôt concerné, modifier les zones, committer, et les pousser : le système va valider les zones, incrémenter le serial de celles modifiées, et recharger le serveur DNS.

Les outils utilisés sont dans le dépôt [dns/utils](./../../../../../dns/utils/), le Makefile peut être utilisé en local pour valider les zones, le hook client/pre-commit peut être utilisé pour valider les zones au commit.

## Hébergement de domaine

La mise en place d'un domaine pour un adhérent passe, tout d'abord, par la création d'un dépôt git spécifique à l'adhérent :

  * Créer un dépôt sur [gitlab](https://git.fdn.fr/), dans le [groupe dns](./../../../../../groups/dns/), ayant pour nom `pnom`. Pour Marcel Dugenou, il sera donc `mdugenou`.
  * Se connecter en SSH sur *git.fdn.fr*
  * Obtenir le chemin vers le dépôt :

        tom@coruscant:~$ echo $(echo "Project.find_by_full_path('dns/mdugenou').disk_path" | sudo gitlab-rails console | grep @hashed | tr -d \").git | xclip -i

  * Utiliser `sudo -u git -i` pour se loger avec l'utilisateur `git`, et aller créer un lien symbolique des hooks nécessaires dans le dossier du dépôt :

        git@coruscant:~$ HASHED_DIR=$(xclip -o)
        git@coruscant:~$ cd git-data/repositories/${HASHED_DIR}
        git@coruscant:~/git-data/repositories/@hashed/........$ mkdir custom_hooks
        git@coruscant:~/git-data/repositories/@hashed/........$ cd custom_hooks
        git@coruscant:~/git-data/repositories/@hashed/......../custom_hooks$ ln -s ~/fdn-dns-utils/server/* .

  * Pour chacun des serveurs DNS faisant autorité sous le contrôle de FDN (pour l'instant : *nsa.fdn.fr* et *gchq.fdn.fr*), se connecter en SSH pour cloner le dépôt de l'utilisateur (le dépôt est pour l'instant vide, c'est normal, il n'y a rien de plus à faire) :

        $ sudo -u bot-dns -i
        $ cd depots && git clone git@git.fdn.fr:dns/mdugenou

  * Si l'adhérent souhaite pouvoir modifier lui même ses zones, lui créer un compte sur git.fdn.fr (dans l'interface d'administration de gitlab), lui donner accès à son dépot avec les permissions "Maintainer" ("Developer" ne permet pas de faire un push vers la branche master, il faut alors passer par des "merge requests", ce n'est pas du tout le but ici...), et lui indiquer que [dns/utils](./../../../../../dns/utils/) contient un Makefile et un pre-commit hook dans le dossier client permettant de valider les zones lors d'un commit.

  * Créer un fichier de zone, nommé `db.le-nom-de-la-zone` (il **faut** que ce soit le vrai nom de la zone, sinon ça ne fonctionnera pas). Y mettre le contenu suivant :

    ```
    $TTL 86400
    @       IN      SOA     nsa.fdn.org. hostmaster.fdn.fr. (
                  2017052001
                  28800
                  7200
                  604800
                  86400 )
                  IN      NS      nsa.fdn.org.
                  IN      NS      gchq.fdn.org.
    ```

  * Lorsque l'on commence avec un dépôt vide, le premier push doit être fait avec la commande `git push -u origin master`.  La toute première fois, il y aura deux erreurs `fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree.`, et `error: pathspec 'output' did not match any file(s) known to git.`, et git parlant de rm db.xxx, ne pas en tenir compte.

## Processus de modification d'une zone dans git

Note : la validation des zones est faite côté serveur lors du push vers
git.fdn.fr, mais si on le souhaite, on peut en plus la faire avant, sur sa
machine locale. Dans ce cas, il **faut** installer le paquet `bind9utils` et
faire les manipulations suivantes pour positionner les *hooks* qui vont bien :

  * Se créer un dossier vide pour y mettre les différents dépôts:

        $ mkdir dns-fdn && cd dns-fdn

  * Cloner le dépôt que l'on veut modifier, par exemple, [dns/fdn](./../../../../../dns/fdn/):

        $ git clone git@git.fdn.fr:dns/fdn.git

  * Cloner le dépôt [dns/utils](./../../../../../dns/utils/):

        $ git clone git@git.fdn.fr:dns/utils.git

  * Coller les hooks présents dans `utils` dans le dépôt `fdn`:

        $ cd fdn/.git/hooks/ && ln -s ../../../utils/client/pre-commit .

  * Une fois les modifications faites, si il y a une erreur, par exemple:

        $ git commit -a -m "modif"
        pre-commit: Validation des modification.....................!
      
        Erreurs:
        ----------------------------
        dns_master_load: db.ffdn.org:50: unexpected end of line
        dns_master_load: db.ffdn.org:50: unexpected end of input
        db.ffdn.org: file does not end with newline
        zone ffdn.org/IN: loading from master file db.ffdn.org failed: unexpected end of input
        zone ffdn.org/IN: not loaded due to errors.
        ----------------------------

  * Une fois les modifications corrigées, et committées, pousser les modifications sur le serveur, il va aussi valider les zones, et refuser le push si non valides, puis, il va compiler les zones, incrémenter le serial, les committer dans la branche `output`, et recharger le serveur DNS:

        $ git push
        Counting objects: 5, done.
        Compressing objects: 100% (5/5), done.
        Writing objects: 100% (5/5), 502 bytes | 0 bytes/s, done.
        Total 5 (delta 3), reused 0 (delta 0)
        remote: pre-receive: Validation des modification...................... Tout va bien.
        [...]
        remote: zone ffdn.org/IN: loaded serial 2014100800
        remote: dump zone to /var/cache/bind/fdn/db.ffdn.org...done
        remote: OK
        remote: server reload successful
        To git@git.fdn.fr:dns/fdn.git
         08f4b53..cdd7e96  master -> master

## Hébergement de sous-domaine de fdn.fr/org

Un sous-domaine n'est qu'un domaine "en-dessous", c'est à dire un enregistrement dans le DNS de la zone "au-dessus". Récupérer le dépôt git ou se trouvent les zones DNS de FDN, [dns/fdn](./../../../../../dns/fdn).

Note, la zone fdn.org est un lien symbolique sur fdn.fr, elles contiennent donc là **même** chose.

### Organisation

Les sous-domaines des membres sont déclarés dans "fdn.subdomains" qui est ensuite inclus dans les fichiers de zone "db.fdn.fr" à la fin de ceux-ci avec une directive "$include".

Donc écrire dans "fdn.subdomains" c'est exactement comme écrire directement dans les fichiers de zone de fdn.fr et fdn.org : attention car une erreur peut impacter toute la zone !

### Exemple

Un exemple pour configurer des MX pour le sous-domaine exemple.fdn.fr et un hôte "www" :

    ; adhérent, numéro et email
    exemple          IN      A       192.0.2.3
                     IN      MX 10   exemple
                     IN      MX 20   mail
    www.exemple      IN      CNAME   exemple

En fait "www" n'est qu'un sous-sous-domaine de fdn.fr...

Il y a plein d'exemples desquels s'inspirer dans "fdn.subdomains", tout dépend de ce qu'on veut faire avec et dans ce nouveau sous-domaine.

Il y a un deuxième fichier, vpn.subdomains, qui contient la sous zone vpn.fdn.fr.


## Zones en slave

Dans le cas où l'adhérent a des zones en slave, il faut créer un fichier `slave`, dans lequel il peut lister des zones, des clefs, des masters et des servers.  C'est un fichier texte, dont les champs sont séparés par des virgules, par exemple, le fichier suivant:

    key,ma-clef,hmac-sha256,nBGZzzbVeg1QRun49H9xqYFD1pbu2OoL2HoKyDAur2U=
    server,1.2.3.4,ma-clef
    server,2000:1:2::4,ma-clef
    masters,babase.bouboule.fr,1.2.3.4,2000:1:2::4
    zone,bouboule.fr,babase.bouboule.fr
    zone,160.67.80.in-addr.arpa,80.67.176.46

Génèrera la configuration BIND:

    # GENERATED FILE, DO NOT EDIT
    masters "babase.bouboule.fr" {
          1.2.3.4 ;
          2000:1:2::4 ;
    };
    key "ma-clef" {
          algorithm "hmac-sha256";
          secret "nBGZzzbVeg1QRun49H9xqYFD1pbu2OoL2HoKyDAur2U=";
    };
    zone "bouboule.fr" {
          type slave;
          file "test/db.bouboule.fr";
          masters {
                  "babase.bouboule.fr" ;
          };
    };
    zone "160.67.80.in-addr.arpa" {
          type slave;
          file "test/db.160.67.80.in-addr.arpa";
          masters {
                  80.67.176.46 ;
          };
    };
    server 1.2.3.4/32 {
          keys "ma-clef";
    };
    server 2000:1:2::4/128 {
          keys "ma-clef";
    };

Le format est:

    key,nom-clef,algorithm,secret
    server,ip-du-serveur,nom-clef
    masters,no-du-master,ip1,ip2,...
    zone,nom-du-domaine,master1,master2,...


## Délégation d'une zone inverse (reverse DNS)

### IPv4

En général, la zone parente n'est pas déléguée à FDN, (vu qu'on va prendre un bout de plage IP libre dans ce qui est attribué à Gitoyen pour l'allouer à l'adhérent,) il faut alors le faire au niveau des serveurs DNS de gitoyen, donc, soit écrire à [tech@gitoyen.net](mailto:tech@gitoyen.net), soit demander à quelqu'un qui est membre de FDN et aussi admin sys de gitoyen, comme domi ou mat. (Je suis sur qu'il y en a plus, mais je ne dénonce pas.)

### IPv6

La plage d'adresses IPv6 allouée aux adhérents est 2001:910:1000::/38, et il y a quatre fichiers de zones inversées qui sont `db.0.1.0.1.9.0.1.0.0.2.ip6.arpa`, `db.1.1.0.1.9.0.1.0.0.2.ip6.arpa`, `db.2.1.0.1.9.0.1.0.0.2.ip6.arpa` et `db.3.1.0.1.9.0.1.0.0.2.ip6.arpa`. Ils se trouvent avec toutes les zones de FDN, dans le [dépôt](./../../../../../dns/fdn/).

Il faut donc d'une part trouver à quelle zone ajouter les enregistrements, (ou la délégation,) pour cela, le plus simple est de ne pas chercher sois-même mais d'utiliser une commande, livrée avec bind, qui elle, ne va pas se tromper en retournant l'adresse :

    $ dig +noall +question -x 2001:910:1042::
    ;0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.2.4.0.1.0.1.9.0.1.0.0.2.ip6.arpa. IN PTR

On retrouve le préfixe alloué à l'adhérent, `dig` a tout seul bien découpé l'adresse, on trouve donc le nom de la zone `0.1.0.1.9.0.1.0.0.2.ip6.arpa.` donc, il faut toucher au fichier `db.0.1.0.1.9.0.1.0.0.2.ip6.arpa` et dans ce fichier, la délégation se fera sur ce qu'il reste, à savoir `2.4`.  Merci de conserver ces zones dans un ordre logique.  Pour installer une délégation, on ajoute, en général, les lignes suivantes :


    ; Marcel Dugenou (adh 1234)
    2.4		IN	NS	ns1.marcel-dugenou.net.
    2.4		IN	NS	ns2.marcel-dugenou.net.


## Suppression d'un dépôt git d'un adhérent

  * Supprimer le dépôt dans gitlab (gardons l'exemple du dépôt `mdugenou`) :
    * aller sur la page du projet dns/mdugenou
    * aller dans Settings -> General -> Advanced -> Expand -> Delete project et suivre la procédure

  * Sur *nsa.fdn.fr* en tant que l'utilisateur `bot-dns` :

```
    bot-dns$ rm -rf ~/depots/mdugenou
    bot-dns$ rm -rf /var/cache/bind/mdugenou
    bot-dns$ env SSH_ORIGINAL_COMMAND="master-bind" ~/depots/utils/update.sh
```

  * Sur *gchq.fdn.fr* en tant que l'utilisateur `bot-dns` :

```
    bot-dns$ rm -rf ~/depots/mdugenou
    bot-dns$ rm -rf /var/cache/bind/mdugenou
    bot-dns$ env SSH_ORIGINAL_COMMAND="master2-bind" ~/depots/utils/update.sh
```

  * Sur *nsa.fdn.fr* et *gchq.fdn.fr*, faire un commit `etckeeper` :

```
    # etckeeper vcs status
    # etckeeper vcs diff
    # etckeeper commit "Suppression du dépôt DNS mdugenou"
```


## Ancien fonctionnement

### Hébergement de domaine

La mise en place d'un domaine pour un adhérent passe par le création d'une zone spécifique :

  * Créer, sur *[[adminsys:serveurs:leia]]*, un fichier `/etc/bind/ladherent.conf` (en général pnom.conf)
  * Y insérer les directives pour son domaine, modèle :

    zone "marcel-dugenou.net" {
        type master;
        file "/etc/bind/db.marcel-dugenou.net";
    };

  * Créer le fichier de la zone, modèle :

    $TTL 86400
    @       IN      SOA     ns0.fdn.org.    hostmaster.fdn.fr. (
                2009121701      ; Serial number
                28800           ; Refresh 8 hours
                7200            ; Retry 2 hours
                604800          ; Expires 7 days
                86400 )         ; Minimum 1 day
                IN      NS      ns0.fdn.org.
                IN      NS      ns1.fdn.org.
                IN      MX 10   mail.fdn.fr.
                IN      MX 20   guinness.fdn.fr.
    @           IN      A       80.67.169.18    ; www.fdn.fr
    www         IN      A       80.67.169.18

  * Insérer une ligne faisant référence à `ladherent.conf` dans `/etc/bind/named.conf`
  * Recharger la configuration : `rndc reconfig`

  * Sur *[[adminsys:serveurs:vador]]*, un fichier `/etc/bind/ladherent.conf` pour la zone esclave, modèle :

    zone "marcel-dugenou.net" {
        type slave;
        masters { 80.67.169.12; };
        file "/var/cache/bind/db/db.marcel-dugenou.net";
    };

  * Insérer une ligne faisant référence à `ladherent.conf` dans `/etc/bind/named.conf`
  * Recharger la configuration : `rndc reconfig`

Pour un domaine .fr il faut s'assurer que le serveur MX principal est bien configuré pour gérer postmaster@marcel-dugenou.net
