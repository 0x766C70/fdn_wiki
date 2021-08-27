# Merge requests

On peut faire des merge requests au moint partiellement en ligne de commande.

Pour cela il faut forker le repository auquel envoyer les merge requests.
Dans l'interface web normalement on devrait avoir un bouton de fork[1].

Si c'est pas le cas il faut demander (par exemple dans #fdn-adminsys sur
Geeknode que les admins authorisent les forks dans le projet en question).

Il y'a peut être aussi moyen de foker un projet en ligne de commande avec
python-gitlab.

Par contre il est fortement déconseillé de ne pas forker le repository
et de pousser la modification dans une branche du repository auquel on
veut contribuer et de créer une merge request à partir de cette
branche.

Si on le fait, et que le repository auquel on veut contribuer est lui
même un fork, ça va envoyer les modification du repository auquel on veut
contribuer, ainsi que nos modifications, au parent du repository auquel
on veut contribuer à la place.

Une fois que notre fork est crée on peut faire le reste en ligne de commande.

Pour ça il suffit de pousser le code dans une branche de votre fork, et de
rajouter quelques options à git qui vont dire à gitlab de créer une pull
request.

Par exemple:
    git push monfork HEAD:mr1 -o merge_request.create -o merge_request.target=master

Références:
-----------
[1] https://docs.gitlab.com/ee/user/project/repository/forking_workflow.html
[2] https://docs.gitlab.com/ee/user/project/push_options.html

License: CC-BY-SA 3.0 Unported
