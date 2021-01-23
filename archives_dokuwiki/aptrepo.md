# Le repository APT maison

Les machines de FDN utilisent différents paquets Debian compilés avec des modifications spécifiques pour FDN.
Depuis toujours, ceci est géré assez anarchiquement : chacun recompile les paquets dont il « s'occupe » dans son coin et fait la mise à jour à la main à coup de dpkg -i.
J'ai (benoar) décidé de monter un « repository » APT qui contient tous les paquets maison, sur [[adminsys:serveurs:leia]].

## Comment ça marche

En gros, les paquets sont construits avec [[http://www.netfort.gr.jp/~dancer/software/pbuilder.html.en|pbuilder]] puis copiés dans un répertoire avec dcmd, d'où ils sont accessibles par FTP, après un obligatoire coup de dpkg-scanpackages.

Le script qui gère tout ça est dans /root/custom_builds et s'appelle package.sh et propose les commandes suivantes (sous la forme ''./package.sh <commande> [arguments]'') :

  * ''help''
    * Montre l'aide
  * ''update <distro>''
    * Mets à jour « distro » (la crée si besoin), pour l'instant limité à lenny et squeeze. N'est utile que de temps en temps, quand il y a des mises à jour nécessaires à faire.
  * ''build <distro> <package>''
    * Construit « package » pour « distro » : le package source doit être sous une des formes suivantes :
      * package.dsc, accompagné d'un .tar.gz (voire avec un diff.gz), comme n'importe quel paquet source Debian
      * un sous-répertoire du /usr/cvsroot qui est un paquet debian
      * un répertoire versionné par git, et qui est un paquet debian
  * ''publish <distro> <package.dsc>''
    * Publie « package » pour « distro » : ici, on se base aussi sur le .dsc même si en pratique c'est le .changes généré à l'étape précédente qui est utilisé

Pour faire court, seules les commandes ''build'' et ''publish'' vous serons nécessaires pour créer votre paquet.

Si vous souhaitez, pour mieux comprendre le code, allez le lire, c'est 90 lignes de shell qui se rapprochent plus d'un wrapper que d'un vrai programme. Il est aussi versionné par git : n'oubliez pas de commiter vos éventuelles modifications.

## La mise à disposition du repository

Il y avait un serveur FTP qui traînait sur leia, je l'ai donc utilisé : les paquets sont mis à dispositions dans /home/ftp/debian-fdn, le ~ftp étant la racine de l'accès anonyme. Le Packages.gz nécessaire à en faire un repository APT est régénéré à chaque publication de paquet.

## Du côté des clients

La ligne à rajouter dans son sources.list :

    deb ftp://leia.fdn.fr/debian-fdn <distro> main

en remplaçant <distro> par lenny ou squeeze, en fonction.

## Les paquets maison qu'on utilise

  * l2tpns (géré par benoar en git) pour les LNS
  * openvpn pour avoir les variables d'environnement IPv6
  * openvpn-auth-radius pour ajouter le support IPv6
