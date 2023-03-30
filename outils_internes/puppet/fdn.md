# Puppet/fdn - gestion des serveurs

## Introduction

Nous utilisons une configuration à base d'envionnement dynamique. C'est à dire que chaque branche du dépôt correspond à un environnement puppet et pourra être testée sur une machine spécifique. Lorsque l'on publie ou modifie une branche dans le dépôt principal l'environnement est automatiquement mis à jour. C'est à dire que lorsque l'on publie des modifications dans la branche production du dépôt principal, **toutes les machines seront mise à jour**.

Documentation [officielle](https://puppet.com/docs/)

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
    - lancer `sudo puppet agent -t --environment ma_super_feature --noop`

Aucune modification ne sera réellement effectuée. À la place puppet montrera ce qui ferait, s'il était lancé pour de vrai.

:warning: la branche doit avoir été poussée au préalable !

### Appliquer une branche

- depuis son ordinateur :
    - `git checkout ma_super_feature`
    - `./bin/apply machine`
- depuis la machine concernée :
    - se connecter à la machine en SSH
    - lancer `sudo puppet agent -t --environment ma_super_feature`

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
apt-get install -y puppet
```

Ajouter ça au fichier /etc/puppet/puppet.conf :
```
cat >/etc/puppet/puppet.conf <<EOF
[main]
server = palpatine.fdn.fr
certificate_revocation = leaf
EOF
```

Lancer puppet pour générer un certificat SSL et attendre qu'il soit accepté par le master :
```
puppet agent --test --waitforcert=5
```

C'est tout pour le client, il faut maintenant aller accepter sur le server le certificat généré sur le client.

Une fois la première pass de puppet terminée, se déloguer, passer un coup d'etckeeper et relancer puppet agent pour terminer l'install : 
```
etckeeper commit
puppet agent --test --waitforcert=5
```

#### Sur palpatine

(À faire après que le client ait généré et proposé son certificat avec une première execution de l'agent):
- vérifier qu'on a bien une demande de certificat : `puppetserver ca list`
- la signer : `puppetserver ca sign --certname le-client.fdn.fr`

Le nom du certificat devrait être le FQDN du client, sinon il y a un souci.

Tant que les clients sont en puppet 5 (bullseye et antérieur), il faut ensuite réparer le certificat CA : le serveur puppet 7 a un CA avec certificat intermédiaire, et les clients ne récupèrent que l'un des deux, et refuse de marcher. À priori ça ne sera plus nécessaire à partir de puppet 7, inclus dans bookworm.  
En attendant, on copie le CA et la CRL à la main pour palier à ce problème :
```
scp /etc/puppetlabs/puppet/ssl/certs/ca.pem le-client:/var/lib/puppet/ssl/certs/
scp /etc/puppetlabs/puppet/ssl/crl.pem le-client:/var/lib/puppet/ssl/
```


(Note: en profiter pour ajouter la nouvelle machine à /etc/clustershell/groups.d/fdn.yaml sur palpatine!)

## Les services

### Sur les serveurs (puppet-agent)

- `systemctl status puppet.service` : [puppet-agent](https://puppet.com/docs/puppet/7/services_agent_unix.html), l'agent puppet, dont le role est de se connecter au serveur régulièrement (toutes les 30 min) et de vérifier que le serveur est conforme à son catalogue, sinon de corriger

### Sur Palpatine (puppet-server)

- `systemctl status puppetserver.service` : [puppet-server](https://puppet.com/docs/puppet/7/server/about_server.html), le grand ordonnateur
- `systemctl status puppetdb.service` :  [puppetdb](https://puppet.com/docs/puppet/7/puppetdb_overview.html), bdd dans laquelle sont stockées toutes les données générées par *puppet-server*
- `systemctl status puppet.service` : [puppet-agent](https://puppet.com/docs/puppet/7/services_agent_unix.html), l'agent puppet, Palpatine étant aussi un noeud comme les autres

## Les modules

Les modules fdn sont stockés dans le répertoire `modules`, dont par exemple **base** qui est le module de base (comme son nom l'indique) qui devrait être inclus sur tous les nœuds.

Idéalement chaque module a un **Readme** qui explique à quoi il peut bien servir, mais la vérité est dans le code :innocent: .

### Les mots de passes et les variables

Nous avons mis en place le module [eyaml](https://github.com/voxpupuli/hiera-eyaml) pour gérer les passwords et éviter de les afficher en clair dans les conf puppet.

Pour chiffrer une info :

- déplacez-vous sur votre copie locale du dépôt puppet (vous devez avoir eyaml installé) ou si sur Palpatine dans `/root/fdn`
-  exécuter `eyaml encrypt -p`
- tapez l'information à chiffrer (tel qu'un mot de passe ou un gecos).
Eyaml va s'appuyer sur la clef publique contenue dans `./keys` pour chiffrer l'information. Vous obtiendrez en retour une chaine du type ENC[PKCS7,SUPERLONGTRUC]

#### Exemple de chiffrement d'info dans templates de module :
- Dans la classe du module utilisé, définir les variables qui contiendront les pass : `$db_user`, par exemple. Vous trouverez un cas concret sur le module matrix et sa [class bridge](https://git.fdn.fr/adminsys/puppet/-/blob/production/modules/matrix/manifests/bridge.pp)
- Dans le template maintenu par le module, utilisez la variable choisie dans la classe à la place de votre passwd sous le format : `<%= @db_user %>`
- Enfin dans le fichier hieradata qui sera du coup en .eyaml au lieu de .yaml, définissez la variable. Pour notre exemple : `matrix::bridge::db_user: irc_bridge_db_user` (ie : puppet va comprendre => dans le module matrix, la classe bridge : replacez db_user par la valeur irc_bridge_db_user) 
- Si cette valeur est un password et doit être chiffrée, remplacez la valeur en clair par la chaine de charactères obtenue à la première étape.

### Les utilisateurs

Voir la page [users](users.md) pour le détail.

## FAQ

### Passer de l'agent du dépôt puppet vers l'agent de la distribution

Selon la phase de la lune on peut vouloir préférer le client puppet (agent) de la distribution plutôt que celui du dépôt puppet, ou l'inverse.

La migration est gérée dans le module base::puppet de notre dépot puppet et se passait bien la dernière fois que ça a été testé donc a encore des chances de fonctionner. La seule chose à faire est de changer la valeur de `base::puppet::puppetlabs_agent` dans hiera, soit directement dans la configuration de la machine `hieradata/hosts/<machine>.yaml` soit au niveau de la distro pour appliquer plus globalement dans `hieradata/distros/Debian/<release>.yaml`.

Une fois la modification faite, passer `puppet agent -t` pour appliquer, puis `hash -r` pour que bash puisse retrouver le nouveau binaire puppet qui n'est pas au même endroit et à nouveau `puppet agent -t` pour vérifier.  
Le service devrait se relancer tout seul si la modification a été faite en background.
