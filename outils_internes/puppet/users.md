## Gestion des utilisateurs

Puppet nous permet de gérer les utilisateurs sur
le parc FDN.

Pour l'instant, seuls les comptes administrateurs (droit root)
sont gérées.

### Repo:

`git clone palpatine.fdn.fr:/srv/puppet/users.git`

### Structure du dépôt

    puppet-module-users/
   - README             L'indispensable LISEZMOI
   - data/              Les utilisateurs
     - user.yaml        les users fdn
   - manifests/         Les fichiers de paramètres
      - init.pp         La définition de la classe 'users' (inutilisée pour l'instant)
      - fdnuser.pp      La définition de la classe 'users::fdnuser'
      - admins.pp       La définition de la classe 'users::admins'

### Déclarer un utilisateur

Il suffit de l'ajouter dans le fichier data/user.yaml.

Exemple de déclaration d'un administrateur (c'est au format [[http://fr.wikipedia.org/wiki/YAML|YAML]]) :

* Penser à bien modifier tous les champs après le copié/collé !
* l'uid est incrémental, prendre celui d'avant +1
* la clef est un hash du password

    tom:
    gecos: Thomas Parmelan
    password: '$1$LbcnM6yX$uBTGQyJEG5SuMWR4LSXZ./'
    uid: '2012'

Pour ajouter ensuite la clefs ssh:
* se rendre dans le répertoire ssh_key.
* créer un fichier 'pseudo'.yaml

    tom:
      type: ssh-ed25519
      key: AAAAC3NzaC1lZDI1Ndfgdfgc1JF89768L05We0q4IhTYvE3a2PeujQ

### Passer en prod

Push les modif et attendre 30mn que l'agent puppet passe sur palpatine pour déployer le nouvel user
