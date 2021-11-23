# Puppet/users -  gestion des utilisateurs

Puppet nous permet de gérer les utilisateurs sur le parc FDN.

Pour l'instant, seuls les comptes administrateurs (droit root) sont gérées.

## Dépôt

Récupération du dépôt : `git clone palpatine.fdn.fr:/srv/puppet/users.git`

## Structure du dépôt

```
 puppet-module-users/
- data/              		Les utilisateurs
  - users.yaml       		Les users fdn
  - roles.yaml			La définition des roles et serveurs associés
  - authorisations.yaml		Les autorisations : associations users/roles
  - ssh_keys			Les clés SSH des utilisateurs
- lib/puppet/parser/functions/
  - find_role_groups.rb		Script ruby pour que Puppet puisse gérer les autorisations
- manifests/         		Les fichiers de paramètres
   - init.pp         		La définition de la classe 'users' (inutilisée pour l'instant)
   - fdnuser.pp      		La définition de la classe 'users::fdnuser'
   - admins.pp       		La définition de la classe 'users::admins'
```

## Déclarer un utilisateur

Il suffit de l'ajouter dans le fichier `data/users.yaml`.

Exemple de déclaration d'un administrateur (c'est au format [YAML](http://fr.wikipedia.org/wiki/YAML) :

* Penser à bien modifier tous les champs après le copié/collé !
* l'uid est incrémental, prendre celui d'avant +1
* la clef est un hash du password (cf. [memo](memo/generate_hash.md))
```
    tom:
    gecos: Thomas Parmelan
    password: '$1$LbcnM6yX$uBTGQyJEG5SuMWR4LSXZ./'
    uid: '2012'
```
Pour ajouter ensuite la clefs ssh:
* se rendre dans le répertoire `ssh_keys`.
* créer un fichier 'pseudo'.yaml
```
    tom:
      type: ssh-ed25519
      key: AAAAC3NzaC1lZDI1Ndfgdfgc1JF89768L05We0q4IhTYvE3a2PeujQ
```
## Passer en prod

Pousser les modifications et attendre 30mn que l'agent puppet se relance sur la machine pour déployer le nouvel utilisateur. Si pressé :
- se connecter sur le serveur en SSH
- `sudo puppet agent -t --noop` : pour voir ce qu'il compte faire :fingers_crossed:
- si OK `sudo puppet agent -t`
