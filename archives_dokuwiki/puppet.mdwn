**Nouveauté 1er mai 2013 :** On utilise le dépôt apt de PuppetLabs (http://apt.puppetlabs.com/ ou son miroir à l'Ircam) histoire d'avoir un Puppet à jour partout.

# Introduction

Le puppetmaster tourne sur leia. Sa config est dans /etc/puppet.

La configuration puppet est stockée dans le dépôt leia.fdn.fr:/srv/puppet/fdn.git .

Ce dépôt contient des sous-modules branchés sur les modules puppet existants (sur gitlab).

Nous utilisons une configuration à base d'envionnement dynamique. C'est à dire que chaque branche du dépôt correspond à un environnement puppet et pourra être testée sur une machine spécifique. Lorsque l'on publie ou modifie une branche dans le dépôt principal l'environnement est automatiquement mis à jour. C'est à dire que lorsque l'on publie des modifications dans la branche production du dépôt principal, toutes les machines seront mise à jour.

Attention, pour l'instant, un certain nombre de modules puppet sont branchés au dépôt principal en tant que sous module git. Cela complexifie un peu la gestion.

# Procédures

## Démarrer

Il faut être dans le noyau adminsys de FDN.

    git clone --recursive leia.fdn.fr:/srv/puppet/fdn.git puppet-fdn

=### Écrire une nouvelle fonctionalité

    git checkout -b ma_super_feature production
    # je fais mes commits
    git push

L'environnement ma_super_feature va être créé, et on observe le message suivant :

    Décompte des objets: 1, fait.
    Écriture des objets: 100% (1/1), 195 bytes | 0 bytes/s, fait.
    Total 1 (delta 0), reused 0 (delta 0)
    remote: .----------------------------------------------- PuppetSync ---
    remote: | Host        : leia.fdn.fr
    remote: | Branch      : ma_super_feature
    remote: | Deploy To   : /srv/puppet/environments/ma_super_feature
    remote: | Repository  : /srv/puppet/fdn.git
    remote: | Depuis git.fdn.fr:puppet/module-stats
    remote: |    d1f9177..d7dff11  master     -> origin/master
    remote: `--------------------------------------------------------------
    To leia.fdn.fr:/srv/puppet/fdn.git
     a958680..495bea3  ma_super_feature -> ma_super_feature


## Tester une fonctionnalité

Se positionner sur la branche correspondant à ma fonctionnalité

    git checkout ma_super_feature

Pour tester sur une machine donnée :

    ./bin/test machine

Aucune modification ne sera réellement effectuée. À la place puppet montrera ce qui ferait, s'il était lancé pour de vrai.

Attention la branche doit avoir été poussée au préalable !

## Appliquer une branche
  
    ./bin/apply mamachine

Attention la branche doit avoir été poussée au préalable !

## Rajouter un utilisateur

Au préalable, il est nécessaire d'avoir récupérer de manière sure :

  * l'empreinte de son mot de passe (générée avec mkpasswd)
  * sa ou ses clés ssh

    cd modules/users

Rajouter un l'utilisateur dans data/users.yaml

    editor data/users.yaml

Rajouter le fichier data/ssh_keys/<user>.yaml en prerant exemple sur les autres

    editor data/ssh_keys/<user>.yaml

Si c'est un satellite, lui donner des droits dans le fichiers satellites.yaml
  
    editor data/satellites.yaml

Si c'est un membre du noyau, le rajouter dans data/core.yaml

    editor data/core.yaml


Appliquer sa modification

    cd ../..
    git add modules/users
    git commit -m "rajout d'un compte"
    git push

(Remarque, cette modif peut être faites dans une branche)

## Supprimer un utisateur

L'ensemble des comptes data/users.yaml sont géré par puppet. C'est à dire que si c'est compte n'apparaissent ni dans data/core.yaml et ni dans data/satellites.yaml alors ces comptes seront supprimés de toutes les machines.

    git checkout production
    cd modules/users
    # supprimer la ligne qui va bien
    editor data/core.yaml        
    # supprimer la ligne qui va bien
    editor data/satelites.yaml
    cd ../..
    git add modules/users
    git commit -m "suppression d'un compte"
    git push


## Ajouter une nouvelle machine

### Sur la machine cliente

Installer le paquet *puppetlabs-release* correspondant à la version de l'OS ; ça se trouve [[http://apt.puppetlabs.com/|chez PuppetLabs]].  Par exemple, pour wheezy :

    curl -O http://apt.puppetlabs.com/puppetlabs-release-wheezy.deb
    dpkg -i puppetlabs-release-wheezy.deb

Installer le paquet *puppet*. Ça se dit comme ça :

    apt-get install puppet
  
Ajouter ça au fichier /etc/puppet/puppet.conf :

    [agent]
    server = leia.fdn.fr

Si on veut que puppet tourne en tant que démon (**ce n'est pas le cas pour les LNS**), changer la variable START à "yes" dans /etc/default/puppet, puis lancer le service puppet :

    /etc/init.d/puppet start

Dans le cas contraire, on le fait juste tourner une fois pour lancer la machine :

    puppet agent --test

C'est tout pour le client.

### Dans le dépôt de configuration

Créer un manifests/<machine>.pp pour indiquer quoi faire installer.

Ajouter l'hôte à modules/base/manifests/postfix.pp

Commiter tout ça et publier tout ça (eventuellement dans une branche de test).

### Sur leia

    Edit du 20150912 - plus nécessaire selon nono :
  * Éditer /etc/puppet/fileserver.conf et autoriser le client dans la section [plugins].
  * Redémarrer le puppetmaster.

(Pour la suite, puppet doit être en train de tourner sur le client) Vérifier qu'on a bien une demande de certificat :

    puppetserver ca list

Et la signer :

    puppetserver ca sign --certname le-client.fdn.fr

Le nom du certificat devrait être le FQDN du client, sinon il y a un souci.

## Faire tourner puppet

### Sur les serveurs

Tant que la variable START est à "yes" dans /etc/default/puppet, pas de souci, le démon se lance au démarrage de la machine et lance une passe toutes les demi-heures.

### Sur les LNS

Quand on a besoin de lancer une passe puppet (genre quand on a modifié la config), on lance le script /usr/local/sbin/run-puppet.

On peut aussi utiliser le script ./bin/apply du dépôt :

    ./bin/apply lns01.fdn.r


# Les modules

Outres les modules sont stockés dans le dépôt principal dans répertoire modules, le puppetmaster est configuré pour aller chercher ses modules dans le répertoire /srv/puppet/environments/production/modules

## Installer un module

Ça se fait :

  * soit en rajoutant un modules dans le dépôt principal
  * soit en clonant le dépôt Git dans ///etc/puppet/modules-others//.

 A priori pas besoin de redémarrer le puppetmaster.

## Liste des modules FDN

Ils sont dans le gitlab et ils existent en tant sous-module du dépôt leia.fdn.fr:/srv/puppet/fdn.git

Pour en créer un, le créer sur https://git.fdn.fr/ dans le namespace puppet et ajoutez le dépôt principal en tant que sous-module.

Si l'on commite dans les sous-modules sans passer par un checkout de fdn.git, il faut faire un pull (et surtout pas des cherry-pick, ça ne fonctionnerait pas) depuis un checkout de fdn.git pour le pousser dans le repo fdn.git

### base

C'est le module de base (comme son nom l'indique) qui devrait être inclus sur tous les noeuds.

Ce qu'il fait :

  * installation de locate avec sa config par défaut,
  * installation du script run-puppet dont il est question plus bas dans /usr/local/sbin,
  * installation de metche avec la config qui va bien.

### ganeti

Installe le nécessaire pour un noeud du cluster Ganeti. La config se fait manuellement, [[adminsys:ganeti|cf la doc]].

### users

Gère les utilisateurs.

### stats

Contient les scripts pour collecter les statistiques réseau

### vpn

Configure un serveur de vpn authentifié

### vpn-open

Configure un serveur de vpn openbar

### vpn-rw

Configure un NAT pour mettre openvpn sur tous les ports d'une adresse IP

# La doc de puppet

http://docs.puppetlabs.com/
