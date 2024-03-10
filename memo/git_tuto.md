
Git est notamment utilisé pour révisionner le wiki adminsys, voici un petit
tuto sur les commandes de base.


# Les Bases

**Attention:** pour l'ensemble des commandes à l'exception du `git clone`, il
faut se situer dans un dossier ou sous dossier du dépôt, et bien sûr faire toutes les opérations avec le même utilisateur (sinon bonjour le micmac).
## Mise en place initiale(a ne faire qu'une fois)
### Cloner un dépôt

    git clone login@machine:chemin/de/repo/nomdurepo.git nomdurepo_en-local

### Configurer son nom et son mail pour les commits

Avant de pusher pour la première fois, on peut éventuellement configurer son
nom et son mail :

    $ git config user.email USER@fdn.fr
    $ git config user.name  <nom>
*Bizarrerie*: il semble que ce soit le courriel qui soit pris pour l'affichage des modifications dans Ikiwiki, du coup il vaut mieux y mettre son prénom ou pseudo.
## Utilisation quotidienne :
### Etat du dépôt (status)

À tout moment, on peut consulter l'état de notre dépôt local avec :

    git status
### Avant toute intervention, récupérer les dernières modifications :

Lorsque l'on veut récupérer les dernières modifications faites par d'autres
sur son dépôt local, on utilise :

    git pull

Et on se retrouve avec un dépôt à jour sur sa machine.

## Déplacer un fichier

Dans l'arborescence, ne pas utiliser `mv` mais `git mv`, sinon il ne sera pas pris en compte correctement lors de la publication.
## Publication des modifications :
### 1-Ajouter un fichier et/ou enregistrer ses modifications: faire un commit
#### On fait nos modifications.
#### On les ajoutes au *futur commit*:

    git add les/fichiers/modifiés/ou/ajoutés

#### Enfin on *commit* :
##### A-Methode avec un court commentaire:
    git commit -m "Un petit commentaire sur ce que j'ai modifié"
##### B-Methode plus bavarde:
On peut mettre plus de détail au commit en faisant:

    git commit

Il est alors possible de mettre plusieurs ligne au message de commit.

##### C-Astuce pour mettre un commentaire apres-coup:

**On peut**, lorsque les fichier sont déjà dans le dépôt et que l'on ne
veut mettre qu'un petit message de commit, **faire**:

    git commit -a -m "Un petit commentaire sur ce que j'ai modifié"
### 2-Pousser les modifications :

Enfin, pour publier ses modifications, on pousse sur le dépôt distant :

    git push

Et hop, le site web se met à jour.


## Historique et logs

Pour voir l'historique des modifications, on utilise :

    git log

# Cas un peu plus complexe

## git rebase

**A compléter**

## merge

**A compléter**

# Aller plus loin

**Ajouter des liens**

