# Puppet/fdn - gestion des serveurs

## Introduction

Nous utilisons une configuration à base d'envionnement dynamique. C'est à dire que chaque branche du dépôt correspond à un environnement puppet et pourra être testée sur une machine spécifique. Lorsque l'on publie ou modifie une branche dans le dépôt principal l'environnement est automatiquement mis à jour. C'est à dire que lorsque l'on publie des modifications dans la branche production du dépôt principal, **toutes les machines seront mise à jour**.

Documentation [officielle](memo/generate_hash.md)

## Procédures

### Préliminaires

Pour que n'importe quel adminsys puisse voir la configuration et proposer des modifications, ce dépôt est présent à la fois sur palpatine et sur gitlab : projet [adminsys/puppet](https://git.fdn.fr/adminsys/puppet). Seul le dépôt palpatine est utilisé pour mettre à jour les serveurs.

### Démarrer sur son ordinateur

Configuration des dépôts :
- pour tous les adminsys :
    - `git clone git@git.fdn.fr:adminsys/puppet.git`
- pour les membres du noyau (à faire en plus) :
    - `git remote add palpatine <user>@palpatine.fdn.fr:/srv/puppet/fdn.git`
    - `git fetch palpatine`
    - `git branch --track palpatine-production palpatine/production`

### Écrire une nouvelle fonctionalité

Pour tous :
```
git checkout master
git pull
git checkout -b ma_super_feature production
# je fais mes commits
git push
```

Une branche ma_super_feature a été créé non seulement sur gitlab mais également sur palpatine via un hook configuré sur gitlab.

### Tester une fonctionnalité

- depuis son ordinateur :
    - `git checkout ma_super_feature`
    - `./bin/test machine`
- depuis la machine concernée :
    - se connecter à la machine en SSH
    - lancer `sudo puppet agent -t --environement ma_super_feature --noop`

Aucune modification ne sera réellement effectuée. À la place puppet montrera ce qui ferait, s'il était lancé pour de vrai.

:warning: la branche doit avoir été poussée au préalable !

### Appliquer une branche

- depuis son ordinateur :
    - `git checkout ma_super_feature`
    - `./bin/apply machine`
- depuis la machine concernée :
    - se connecter à la machine en SSH
    - lancer `sudo puppet agent -t --environement ma_super_feature`

:warning: la branche doit avoir été poussée au préalable !

Une fois que vous êtes satisfait avec vos modifications, vous pouvez demander à un [admincore](/equipe/equipe_adminsys.md#admincore) de la valider et de la fusionnner. À partir de là à charge de l'admincore de :
- fusionner dans **gitlab/production**, soit via gitlab, soit via le ligne de commande (idéalement en supprimant la branche associée pour éviter qu'elle ne traîne)
- fusionnner dans **paltapine/production** en CLI :
    - `git checkout production`
    - `git pull --prune`
    - `git checkout palpatine-production`
    - `git pull`
    - `git merge production`
    - `git push palpatine HEAD:production`

:warning: la procédure précédente n'est valable que si **gitlab/production** et **palpatine/production** sont au même commit, sinon il faut au préalable les resynchroniser :sweat:

### Ajouter une nouvelle machine

#### Dans le dépôt de configuration

- Créer une branche comme pour une nouvelle fonctionnalité
- Créer un `hieradata/hosts/[machine].yaml` pour décrire ce qui doit être installé
- Tester comme pour une nouvelle fonctionnalité
- Appliquer comme pour une nouvelle fonctionnalité
- Commiter et publier tout ça quand tout est opérationnel

#### Lesson Learned (dans le cas d'un nouveau droide tout frais)

Bien penser à ajouter le nom de la **machine.fdn.fr** dans `/etc/hosts` sinon mistmatch entre le Signing Certificate Request For qui apparait en nom de machine sans le .fdn.fr et puppet affiche une jolie erreur 500 : Server Error: Function lookup() did not find a value for the name 'classes' on node r5d4

#### Sur la machine cliente

Update apt, installer les paquets `puppet` et `lsb-release` :
```
apt-get update
apt-get install -y puppet-agent lsb-release
```

Ajouter ça au fichier /etc/puppetlabs/puppet/puppet.conf :
```
cat >/etc/puppetlabs/puppet/puppet.conf <<EOF
[main]
server = palpatine.fdn.fr
EOF
```

Lancer puppet pour générer un certificat SSL et attendre qu'il soit accepté par le master :
```
puppet agent --test --waitforcert=5
```

C'est tout pour le client, il faut maintenant aller accepter sur le server le certificat généré sur le client.

> Note : normalement, sur les nouvelle vms installées dans PVE toutes ces étapes ont déjà été faites pour nous :)

Une fois la première pass de puppet terminée, se déloguer, passer un coup d'etckeeper et relancer puppet agent pour terminer l'install : 
```
sudo etckeeper commit
puppet agent --test --waitforcert=5
```

#### Sur palpatine

(Pour la suite, puppet doit être en train de tourner sur le client) :
- vérifier qu'on a bien une demande de certificat : `puppetserver ca list`
- la signer : `puppetserver ca sign --certname le-client.fdn.fr`

Le nom du certificat devrait être le FQDN du client, sinon il y a un souci.

## Les services

### Sur les serveurs (puppet-agent)

- `systemctl status puppet.service` : [puppet-agent](https://puppet.com/docs/puppet/7/services_agent_unix.html), l'agent puppet, dont le role est de se connecter au serveur régulièrement (toutes les 30 min) et de vérifier que le serveur est conforme à son catalogue, sinon de corriger

### Sur Palpatine (puppet-server)

- `systemctl status puppetserver.service` : [puppet-server](https://puppet.com/docs/puppet/7/server/about_server.html), le grand ordonnateur
- `systemctl status puppetdb.service` :  [puppetdb](https://puppet.com/docs/puppet/7/puppetdb_overview.html), bdd dans laquelle sont stockées toutes les données générées par *puppet-server*
- `systemctl status puppet.service` : [puppet-agent](https://puppet.com/docs/puppet/7/services_agent_unix.html), l'agent puppet, Palpatine étant aussi un noeud comme les autres

## Les modules

Les modules fdn sont stockés dans le répertoire `modules`, dont par exemple **base** qui est le module de base (comme son nom l'indique) qui devrait être inclus sur tous les noeuds.

Idéalement chaque module a un **Readme** qui explique à quoi il peut bien servir, mais la vérité est dans le code :innocent: .

### Les mots de passes et les variables

Nous avons mis en place le module [eyaml](https://github.com/voxpupuli/hiera-eyaml) pour gérer les passwords et éviter de les afficher en clair dans les conf puppet..

Pour chiffrer une info: se mettre à la racine du repo `#eyaml encrypt -p` et tapez le password voulue eyaml va s'appuyer sur la clef publique contenue dans /keys pour chiffrer l'information.. Vous obtiendrez en retour une chaine du type ENC[PKCS7,SUPERLONGTRUC]

#### Exemple de chiffrement d'info dans templates de module:
- Dans la classe du module utilisé, définir les variables qui contiendront les pass: `$db_user`, par exemple. Vous trouverez un cas concret sur le module matrix et sa [class bridge](https://git.fdn.fr/adminsys/puppet/-/blob/production/modules/matrix/manifests/bridge.pp)
- Dans le template maintenu par le module, utilisez la variable choisie dans la classe à la place de votre passwd sous le format: `<%= @db_user %>`
- Enfin dans le fichier hieradata qui sera du coup en .eyaml au lieu de .yaml, définissez la variable. Pour notre exemple: `matrix::bridge::db_user: irc_bridge_db_user` (ie: puppet va comprendre => dans le module matrix, la classe bridge: replacez db_user par la valeur irc_bridge_db_user) 
- Si cette valeur est un passwd et doit être chiffrée, remplacez la valeur en claire par la chaine de char obtenue à la première étape.  

## FAQ

### Passer de l'agent du dépôt puppet vers l'agent de la distribution

Pour des raison de facilitation d'administration nous préférons utiliser le client de la distribution plutôt que celui du dépôt puppet. Procédure à suivre pour la migration :
- supprimer l'agent du dépôt de puppet : `apt purge puppet-agent`
- retirer le dépot puppet sur la machine
- retirer `base::puppet::puppetlabs_agent: true` du hiera de la machine (cf. `hieradata`) sur puppet et pousser
- installer l'agent de la distribution : `apt install puppet`
- déplacer les certificats TLS : `mv /opt/puppetlabs/puppet/ssl /var/lib/puppet/ssl`
- ménage des binaires : `rm -rf /opt/puppetlabs`
- vérifier que tout roule : `puppet agent -t [--noop]`
