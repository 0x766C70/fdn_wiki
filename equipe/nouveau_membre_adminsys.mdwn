[[!meta title="Nouveau chez les adminsys"]]

# Nouveau chez les adminsys !

Voici les quelques étapes à effectuer pour avoir les outils et les pré-requis permettant de contribuer au Wiki.
Génial tu viens de débarquer et tu sais pas quoi faire avec tes doigts.
Étape par étape on va tâcher de démystifier cela. Rassure-toi, c'est simple.

## Les indispensables

* Un laptop (distro linux, c'est plus propre ^^)
* Tes identifiants lors de ton adhésion ( Format Nom Prénom et ton numéro d'ahérent No d'adh.: xxxx) ainsi que tes identifiants de connection (login : adhacc-xxxx )
* Client IRC (Webchat irssi, pidgin, xchat,... ) et/ou Matrix (Riot...)

## Accéder au wiki FDN

Avant toute chose on se rend sur [le Wiki FDN](https://wiki.fdn.fr/start).
En bas de page tu trouveras le bouton "connexion".
Les identifiants utilisés seront les mêmes que pour l'espace adhérents sur le site [FDN](https://www.fdn.fr/) : login `adhacc-xxxx` et le mot de passe associé.

## Prendre le temps d'apprécier l'espace Wiki FDN

Comme tu le consteras rapidement il y a beaucoup de contenu.
Et si tu te trouves sur cette page c'est que tu n'as pas forcement un bus à prendre donc reste zen.
Si tu es curieux, cela peut être une bonne chose de regarder un peu les différentes rubriques.
Vouloir devenir **Adminsys** c'est sympa mais c'est encore mieux de savoir dans quel univers tu viens de tomber.

## Accéder au wiki Adminsys

Dans la liste on retrouve [adminsys](https://adminsys.fdn.fr/), logiquement une boîte de dialogue devrait s'ouvrir et demander une nouvelle fois ton authentification.

Cette authentification est exactement la même que sur le wiki FDN, une seule chose diffère ce sont les droits sur les pages. Tu seras en lecture seule sur toutes les pages.

## Comprendre le fonctionnement de l'équipe

Le plus important dans l'histoire c'est de comprendre comment le groupe fonctionne pour mieux s'adapter et s'intégrer :)
Un tour dans la [page dédiée](https://adminsys.fdn.fr/equipe/fonctionnement/) à ce sujet est fortement conseillée !

## Contribuer au Wiki Adminsys

Pour devenir contributeur il faut avoir une clé SSH publique et l'avoir envoyée à un adminsys et avoir été intégré au préalable au groupe adminsys! 

### Création de sa clé SSH

Ouvrir un terminal avec ton profil utilisateur (pas besoin d'être admin de ta machine)
Lance la commande suivante :

```bash
$ ssh-keygen -b 4096 -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa):
Enter passphrase (empty for no passphrase): mapassphraseamoiquejevaisretenirbiensur
Enter same passphrase again: mapassphraseamoiquejevaisretenirbiensur
Your identification has been saved in /home/user/.ssh/id_rsa.
Your public key has been saved in /home/user/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:sha256isbetterencryption user@themachine
The key's randomart image is:
+---[RSA 4096]----+
           / \
          / _ \
         | / \ |
         ||   || _______
         ||   || |\     \
         ||   || ||\     \
         ||   || || \    |
         ||   || ||  \__/
         ||   || ||   ||
          \\_/ \_/ \_//
         /   _     _   \
        /               \
        |    O     O    |
        |   \  ___  /   |
       /     \ \_/ /     \
      /  -----  |  --\    \
      |     \__/|\__/ \   |
      \       |_|_|       /
       \_____       _____/
             \     /
             | fdn |

+----[SHA256]-----+
```

une chose à retenir c'est l'emplacement de ta clé SSH publique, ici c'est **/home/user/.ssh/id_rsa.pub**.
Cette clé est à transmettre à un membre adminsys qui te donnera les droits sur le dépôt git.

Petit tip pour les utilisateurs irssi (client irc en terminal), parce que le terminal c'est la vie en fait 

`/dcc send pseudo_de_l_adminsys /home/user/.ssh/id_rsa.pub`

Qu'est-ce qu'un dépôt git ? C'est un dépôt versionné de données. Git est utilisé essentiellement dans les milieux de développeurs. Les pages du Wiki adminsys sont stockées dans un dépôt Git. Crée toi un dossier sur ta machine où tu pourras récupérer l'aborescence du wiki adminsys, évite de mettre ça en vrac n'importe où , essaie de garder une structure et de la logique. Il ne te restera plus qu'à récupérer le contenu du wiki comme ceci :

```bash
$ git clone obiwan.fdn.fr:/srv/repositories/adminsys.git
```

## Notions de base - GIT et Markdown

Etre contributeur c'est connaître un minimum les langages et les outils employés. 

### GIT 

Qu'est-ce que le git ? on peut demander ça à wikipédia éventuellement, mais en gros c'est un logiciel permettant la gestion de versions décentralisées créé par Linus Torvalds (Et oui le papa du noyau linux). Si tu souhaites plus d'informations sur le sujet [Git](https://fr.wikipedia.org/wiki/Git). Sur le wiki adminsys il y a un tuto expliquant les commandes de base en git [tuto Git](https://adminsys.fdn.fr/outils/git_tuto/). Si tout se passe bien dans le meilleur des mondes l'ordre pour pousser une de tes pages ce sera comme ceci : 

```bash
$ git clone obiwan.fdn.fr:/srv/repositories/adminsys.git
```
**Git clone** - on récupère le contenu du wiki adminsys.
N'oublie pas que tu as envoyé ta clé publique avec tes infos pour que tu puisses être clairement reconnu·e par le serveur. 
Cela te donnera avec tes accès comme ceci :

```bash
$ git clone user@adminsys.fdn.fr:/srv/repositories/adminsys.git
```

```bash 
$ git pull
```
**Git pull** - Récupère les dernières modifications apporté au git 

```bash
$ git status 
``` 
**Git status** - Si un fichier est différent du dernier pull effectué, cela te prévient ( si tu viens de modifier une page existante ou dans le cas d'une création)

```bash
$ git log -3
```
**Git log** - Cela te donne les logs des trois derniers commits effectués

```bash
$ git add nom_de_la_page.mkdwn
```
**Git add** - permet de rajouter le ou les pages que tu souhaites pousser dans ton prochain commit

```bash 
$ git commit -m (n'affiche pas le preview de ta page) "écrit un commantaire sur ta page et l'ajout effectué, reste clair et conçis"
```
**Git commit** - permet de commiter ton travail sur les pages créées

```bash
$ git push
``` 
**Git push** - permet de pousser ta page sur le dossier du wiki adminsys

```bash 
$ git log -3
```
**Git log** - tu vérifies que ton push est bien pris en compte et qu'il n'y a pas d'erreur.

#### Markdown

Qu'est-ce que le Markdown ? On peut demander à ma grand mère, enfin je ne suis pas certain qu'elle sache ! ^^, c'est simple en tout cas. Ce langage a été créé par un certain John Gruber en 2004. Ce langage permet entre autres d'être directement lisible en l'état sans besoin d'être interprété ou même compilé, ce qui lui donne un bel avantage. C'est un langage avec un balisage léger, il peut aussi être interprété pour une sortie HTML, Perl, Ruby, Python, et j'en passe... Les utilisateurs de github auront forcement à faire à lui. Le README.md est du markdown. Pour plus d'informations tu peux aller voir ici [Markdown](https://fr.wikipedia.org/wiki/Markdown). Pour les bases en Markdown [Markdown Basics](https://daringfireball.net/projects/markdown/basics).

## Liens connexes 

Il y a déjà du contenu existant sur la contribution au wiki adminsys [Accéder et contribuer au wiki](https://adminsys.fdn.fr/outils/ikiwiki/).
