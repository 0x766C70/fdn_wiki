## Notions de base - GIT et Markdown


### Création de sa clé SSH

Ouvrir un terminal avec ton profil utilisateur (pas besoin d'être admin de ta machine)
Lance la commande suivante :

```bash
$   ssh-keygen -t ed25519 -a 256
```
une chose à retenir c'est l'emplacement de ta clé SSH publique, ici c'est **/home/user/.ssh/id_ed25519.pub**.


```bash
$ git clone git@git.fdn.fr:adminsys/wiki.git
```
Vous avez maintenant accès en local à tout le wiki ! Consultez un tutorial git & markdown pour commencez à participer ! Et n'hésitez pas à venir poser des questions sur le chan adminsys !

Etre contributeur c'est connaître un minimum les langages et les outils employés. 
Consultez un tutorial git & markdown pour commencez à participer ! Et n'hésitez pas à venir poser des questions sur le chan adminsys !
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

