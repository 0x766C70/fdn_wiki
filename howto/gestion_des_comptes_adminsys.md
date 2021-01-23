[[!meta title="Gestion des comptes d'administration systeme"]]


Les comptes d'administration système sont gérés par puppet. On distingue les
comptes d'administration des comptes de services (web sur yoda, mail sur solo,
etc).  Les comptes de services ne sont pas gérés par puppet.

Prérequis :

- [[outils/puppet]]

## Rajouter un membre du groupe adminsys

### Liste adminsys (Sympa)

Se connecter sur [lists](https://lists.fdn.fr), aller dans admin de la liste adminsys, gérer 
des abonnés, Ajouter un utilisateur.

### Rajouter les comptes UNIX (Puppet)

Au préalable, il est nécessaire d'avoir récupéré de manière sure :

  * l'empreinte de son mot de passe pour les utilisateurs sudo (générée avec 
mkpasswd -m sha-512)
  * sa ou ses clés ssh
  * le numéro de l'adhérent

Rajouter un l'utilisateur dans data/users.yaml

    editor modules/users/data/users.yaml

Rajouter le fichier `data/ssh_keys/<user>.yaml` en prenant exemple sur les autres

    editor modules/users/data/ssh_keys/<user>.yaml

Lui donner des droits dans le fichiers `data/authorisations.yaml`
  
    editor modules/users/data/authorisations.yaml

Appliquer sa modification

    git commit -m "Rajout d'un compte"
    git push

(Remarque, cette modif peut être faites dans une branche)

Pour tester:

    bin/test lamachine

Si besoin, forcer puppet:

    bin/apply lamachine

## Supprimer un utilisateur

L'ensemble des comptes data/users.yaml sont géré par puppet. C'est à dire que
si c'est compte n'apparaissent ni dans data/core.yaml et ni dans
data/satellites.yaml alors ces comptes seront supprimés de toutes les machines.

    editor modules/users/data/authorisations.yaml        
    git commit -m "suppression d'un compte"
    git push


