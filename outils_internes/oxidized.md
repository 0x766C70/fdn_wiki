
[https://github.com/ytti/oxidized](https://github.com/ytti/oxidized)

Oxidized est un outil de backup des matériels réseau (en l'occurence chez FDN, les switchs).
L'application se connecte automatiquement à intervalles réguliers (en telnet ou SSH) sur les équipements à sauvegarder, lit leur configuration et la sauvegarde dans un dépôt git.
Le script tourne sur la machine obiwan. Le user "oxidized" est dédié à cet usage.

FAQ :
-----

**Où sont sauvegardés les fichiers de conf des switchs ?**  
`/srv/oxidized/oxidized/<nom_du_switch>`

**Comment je modifie la liste des équipements à sauvegarder ?**  
dans `/srv/oxidized/.config/oxidized/router.db`

**Quels identifiants oxidized utilise t-il pour se connecter sur les équipements ?**  
cf "username" dans dans `/srv/oxidized/.config/oxidized/config`
et "password" dans `~/oxidized/`

**Où est le fichier de conf principal ?**  
`/srv/oxidized/.config/oxidized/config`

**Reste t-il des choses à faire ?**  
oui, monitorer l'état du service. Actuellement s'il tombe en panne on ne s'en rendra pas forcément compte.

-------  
Pour mémoire, procédure d'installation :
installer ruby + dépendances :

    apt-get install ruby ruby-dev libsqlite3-dev libssl-dev pkg-config cmake

installer oxidized :

    gem install oxidized
    gem install oxidized-script

lancer une fois l'exécutable  pour créer un fichier de conf dans ~/.config/oxidized/config :

    oxidized

modifier les paramètres dans le fichier : 

 * username et password
 * rest: false
 * ajouter la configuration suivante sous la ligne "default: csv" dans la section "source" :

     csv:
       file: "~/.config/oxidized/router.db"
       delimiter: !ruby/regexp /:/
       map:
         name: 0
         model: 1
         password: 2

(en français : la liste des routeurs à configurer est un fichier csv dans ~/.config/oxidized/router.db,
le délimiteur est ":", la première colonne est le hostname du switch, la seconde le modèle, la troisième le password de connexion)

créer le fichier csv : `~/.config/oxidized/router.db`, le passer en chmod 600 et le remplir, exemple :

    mon_switch_1:ios:le_passw0rd
    mon_switch_2:procurve:le_passw0rd

lancer "oxidized" pour récupérer les backups. La sauvegarde des équipements est faite par défaut toutes les heures (configurable dans le fichier de conf).
la commande est mise dans la crontab en @reboot pour lancement automatique au boot du serveur.
