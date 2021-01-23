## Gestion des utilisateurs

L'outil [[:adminsys:puppet]] nous permet de gérer les utilisateurs sur
le parc FDN.

Pour l'instant, seuls les comptes administrateurs (droit root)
sont gérées.

### Structure du dépôt

    puppet-module-users/
   - README             L'indispensable LISEZMOI
   - data/              Les utilisateurs
     - admins.yaml        Administrateurs
     - others.yaml        Autres (pas pris en compte pour l'instant)
   - manifests/         Les fichiers de paramètres
      - init.pp         La définition de la classe 'users' (inutilisée pour l'instant)
      - fdnuser.pp      La définition de la classe 'users::fdnuser'
      - admins.pp       La définition de la classe 'users::admins'

### Déclarer un utilisateur

Il suffit de l'ajouter dans le fichier data/admins.yaml (pour un administrateur), ou data/others.yaml, à terme, pour un autre utilisateur.

Pour le cas des administrateurs, on force l'UID à partir de 2000, en prenant bien soin de ne pas faire de doublon (la bonne méthode est de prendre "le dernier plus un").

Pour les autres, cela n'est pas encore géré via Puppet, mais les conventions d'UID existent déjà (voir les pages de création de comptes mail ou Web pour les détails, inutile de doublonner).

Exemple de déclaration d'un administrateur (c'est au format [[http://fr.wikipedia.org/wiki/YAML|YAML]]) :

    tom:
    gecos: Thomas Parmelan
    groups:
    - adm
    - sudo
    password: '$1$LbcnM6yX$uBTGQyJEG5SuMWR4LSXZ./'
    ssh_keys:
      tom@pern.ankh.fr.EU.org:
        key: AAAAB3NzaC1yc2EAAAABIwAAAIEAq//7sqW+13uGzKGv6dWKBb0dgm9Zu6VFF0/acfZzUznb67lMFhCqn8rakIL6CJvwzI9JHI/aMERMuM3IRwxan4oTkwhTxtmyKv5qkbyhs8S+WD9LoxROJ5w6R7eakxD8FSN7wdD/NXvWmxDuua1NX+n/BVEtVmHpXZpiOHvt3Dk=
        type: ssh-rsa
    uid: '2012'

La liste de groupes est à comprendre comme "cet utilisateur doit appartenir au moins à ces groupes" (s'il appartient à d'autres groupes, il n'en sera pas supprimé).

### Passer en prod

Commiter vos fichiers, pousser les changements sur le
git de leia, se connecter sur leia, et tirer les
changements dans le dossier ''/etc/puppet'' via la commande :

    sudo sh -c 'cd /etc/puppet/modules-FDN/users && git pull'

Puppet va déployer automatiquement les changements sur une partie du
parc, voir la section [[:adminsys:puppet#faire_tourner_puppet]] sur la
page de [[:adminsys:puppet]].
