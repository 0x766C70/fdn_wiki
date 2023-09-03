# Administration du service

> À destination des adminsys : comment administrer le service

## Caractéristiques

*A completer par un adminsys*
Machine physique, virtuelle, emplacement salle/cluster, etc.

*Pas la peine de trop détailler les caractérisqtiques des machines virtuelles car elles peuvent être modifiées assez souvent ;)*

url d'administration : https://pad.fdn.fr/admin/
login : admin
mot de passe : dans le fichier settings.json


## Administration

### Tâches spécifiques

https://github.com/ether/etherpad-lite#installation

*Lister ici les tâches spécifiques au service : création d'utilisateur, administration de l'outil, etc.*

### Installation

installation dans le dossier /home/etherpad

faire un sudo git clone --branch master https://github.com/ether/etherpad-lite.git

il utilise dans le conf de Fdn un DB postgreql local

### Suppression des pad inactifs depuis 1 an
````
"ep_delete_after_delay": {
    "delay": 31622400,
    "loop": true,
    "loopDelay": 3600,
    "deleteAtStart": true,
    "text": "Le contenu de ce pad sera effacé après une année."
},
````
### Ne pas activer le suivi des auteur·ices par défaut
````
"ep_author_follow": {
   "followAll" : false,
   "enableFollow" : false
 },
````

### Logs

*Où trouver les logs en cas de problème*

### Base de données

*Sauvegardes, restoration*

### Sauvegarde

*Où et comment sont sauvegardés les données et/ou fichiers de configuration*

> Si aucune sauvegarde, l'indiquer quand même (ça évite de chercher)

### En cas de pépins

*Mettre les commandes habituelles pour checker un status, redemarrer...*

https://github.com/ether/etherpad-lite/wiki


## FAQ administration

https://github.com/ether/etherpad-lite/wiki/FAQ

Plugin [MyPads](https://framagit.org/framasoft/Etherpad/ep_mypads)
Configuration : Configure an admin user in Etherpad's settings.json and use those credentials in https://pad.fdn.fr/mypads/?/admin


> Lister ici les questions fréquemment rencontrées par les adminsys : ex "j'ai ce log, qu'est-ce que je fais ?"

### Question

Réponse...
