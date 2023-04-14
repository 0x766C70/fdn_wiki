# Puppet/users -  gestion des utilisateurs

Puppet nous permet de gérer les utilisateurs sur le parc FDN.

Pour l'instant, seuls les comptes administrateurs (droit root) sont gérés.

## Config

La gestion des utilisateurs se fait dans le dépôt puppet principal à partir du répertoire: `modules/users`

## Structure des fichiers

```
 modules/users/
- data/              		Les utilisateurs
  - users.eyaml       		Les utilisateurs fdn
  - roles.yaml			La définition des roles et serveurs associés
  - authorisations.yaml		Les autorisations : associations utilisateurs/rôles
  - ssh_keys			Les clés SSH des utilisateurs
- lib/puppet/parser/functions/
  - find_role_groups.rb		Script ruby pour que Puppet puisse gérer les autorisations
- manifests/         		Les fichiers de paramètres
   - init.pp         		La définition de la classe 'users' (inutilisée pour l'instant)
   - fdnuser.pp      		La définition de la classe 'users::fdnuser'
   - admins.pp       		La définition de la classe 'users::admins'
```

## Déclarer un utilisateur

Il suffit de l'ajouter dans le fichier `data/users.eyaml`.

Les informations sensibles (GECOS et hash du mot de passe) sont chiffrées afin de rendre le module puppet public. Il faudra donc se référer à la [doc](https://git.fdn.fr/adminsys/wiki/-/blob/master/outils_internes/puppet/fdn.md#les-mots-de-passes-et-les-variables) pour les explications sur la commande `eyaml encrypt -p`.

Exemple de déclaration d'un administrateur. C'est au format [YAML](http://fr.wikipedia.org/wiki/YAML) :

* Penser à bien modifier tous les champs après le copié/collé !
* l'uid est incrémental, prendre celui d'avant +1
* le champ password est le hash du password (cf. [memo](memo/generate_hash.md))
```
  tom:
    gecos: Thomas Parmelan [donnée à chiffrer]
    numadh: 411
    password: '$1$LbcnM6yX$uBTGQyJEG5SuMWR4LSXZ./' [donnée à chiffrer]
    uid: 2012
```
Après utilisation de `eyaml encrypt -p` sur les deux données à chiffrer :

```
  tom:
    gecos: ENC[PKCS7,MIIBeQYJKoZIhvcNAQcDoIIBajCCAWYCAQAxggEhMIIBHQIBADAFMAACAQEwDQYJKoZIhvcNAQEBBQAEggEAlXuqGEdYldI1KZGSnuECUORXrnTBIprTLzjXRbiTqc51NCOKt1C/i4FxYU9rTunNolkwmnRGE5Az5r3ARmO8Wb93ijoG/0b/CHiaQwh/8Q5/DYG7n93wqzrNpEwtsyv+9tKcZ3DgYCeCWYL4YXm3aEJC3l3v3o+LU4asNogetHVTw+4eAHJAZLMWW4tZDJS6R17ADNlN5oGWeWeRbpmLnuyAwJeQgXRph8AdhJGUG6udhA/Li69x8hk+PE8wiIsAjrTn5wYSHzAore5+qZT0ExGiyzItoDaR91fw4HqM5wpb++0GQoXITvjMk0PnLBFLOtXPCrqkbQfQKfv2cVJXNDA8BgkqhkiG9w0BBwEwHQYJYIZIAWUDBAEqBBCC9hdKzOEPx3spqpl5qk1FgBDEi5Qzb+HO0lhCV/5vdLo9]
    numadh: 411
    password: ENC[PKCS7,MIIBmQYJKoZIhvcNAQcDoIIBijCCAYYCAQAxggEhMIIBHQIBADAFMAACAQEwDQYJKoZIhvcNAQEBBQAEggEAZXDbipUOm2JpQGot91uivsXMX4+q/M8/alqfVwe0WSkDwfJ/eMGZDPEj/HEk0iu83OQnIkpg2VQLTwiezgBuh41T4RbK8yexZYFwdR+J3ik8LlljrMTvojosL/+PN/W0Zp3ohuETmlV6UMCuokjSzGLBqZH7xnYUJeXEPVN7G095r2ykSkJhitysVQxpx2I4j37T7toz+3eWhiJ996Nunu3JqbJr9KGBhrJxxh2I8depkSVF+bCsgh6CqVTiJ+c/wIGQRDlCnAbxL7jRcujqhcS1JgoXoKOdfG9Lvb/IwFvhbdEHRTO57U05VHusf/9qW6+i8yZEC3KoT5nfIq2qljBcBgkqhkiG9w0BBwEwHQYJYIZIAWUDBAEqBBCD8aMNLcQ34XIkQIKSv2dTgDBJaQBxHNGhNCOHeW63lXsgj+1OndTbocr7qOAHfah30045KbcHi++JtFHbucPSf+s=]
    uid: 2012
```
Pour ajouter la clef publique SSH :
* se rendre dans le répertoire `ssh_keys`.
* créer un fichier 'pseudo'.yaml
```
tom@somewhere:
  type: ssh-ed25519
  key: AAAAC3NzaC1lZDI1Ndfgdfgc1JF89768L05We0q4IhTYvE3a2PeujQ
```
On peut y mettre plusieurs clefs.

## Passer en prod

Pousser les modifications et attendre 30mn que l'agent puppet se relance sur la machine pour déployer le nouvel utilisateur. Si pressé :
- se connecter sur le serveur en SSH
- `sudo puppet agent -t --noop` : pour voir ce qu'il compte faire :fingers_crossed:
- si OK `sudo puppet agent -t`
