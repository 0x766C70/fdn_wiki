[[!toc levels=2]]


Introduction
============

Nous utilisons actuellement puppet5 provenant des dépôt de puppetlabs.
puppetserver et puppetdb sont installés sur la machine palpatine qui leur
est dédiée. Sur chaque machine l'agent puppet est installé.

La configuration puppet est stockée dans le dépôt palpatine.fdn.fr:/srv/puppet/fdn.git .

Nous utilisons une configuration à base d'envionnement dynamique. C'est à dire
que chaque branche du dépôt correspond à un environnement puppet et pourra être
testée sur une machine spécifique. Lorsque l'on publie ou modifie une branche
dans le dépôt principal l'environnement est automatiquement mis à jour. C'est à
dire que lorsque l'on publie des modifications dans la branche production du
dépôt principal, toutes les machines seront mise à jour.


# Procédures

Attention, avec le paquet de puppetlabs les binaires de puppet sont installés
dans le répertoire `/opt/puppetlabs/bin`. C'est plus simple si ce chemin est
dans la variable PATH. C'est le cas en utilisant `sudo -i puppet ...` ou en
passant root avec la commande `sudo -i`.

## Démarrer sur son ordinateur

Il faut être dans le noyau adminsys de FDN.

    git clone palpatine.fdn.fr:/srv/puppet/fdn.git puppet-fdn

## Écrire une nouvelle fonctionalité

    git checkout -b ma_super_feature production
    # je fais mes commits
    git push

L'environnement ma_super_feature va être créé, et on observe entre autre la
ligne suivante :

    remote: r10k updating ma_super_feature environment


## Tester une fonctionnalité

Se positionner sur la branche correspondant à ma fonctionnalité

    git checkout ma_super_feature

Pour tester sur une machine donnée :

    ./bin/test machine

Aucune modification ne sera réellement effectuée. À la place puppet montrera ce
qui ferait, s'il était lancé pour de vrai.

Attention la branche doit avoir été poussée au préalable !

## Appliquer une branche
  
    ./bin/apply mamachine

Attention la branche doit avoir été poussée au préalable !

## Ajouter et supprimer un utilisateur

Cf [[howto/gestion_des_comptes_adminsys.mdwn]]

## Ajouter une nouvelle machine

### Dans le dépôt de configuration

Dans le git puppet dans la branche `production` :

- Créer un hieradata/hosts/[machine].yaml pour décrire ce qui doit être installé.

- Ajouter l'hôte à modules/base/manifests/[machine].pp

- Commiter tout ça et publier tout ça (eventuellement dans une branche de test).


### Lesson Learned (dans le cas d'un nouveau droide tout frais)

Bien penser à ajouter le nom de la machine.fdn.fr dans /etc/hosts sinon mistmatch entre le Signing Certificate Request For qui apparait en nom de machine sans le .fdn.fr et puppet affiche une jolie erreur 500 : Server Error: Function lookup() did not find a value for the name 'classes' on node r5d4

### Sur la machine cliente

Ajout le dépôt de puppetlabs :

    cat >/etc/apt/sources.list.d/puppetlabs.list <<EOF
    deb http://apt.puppetlabs.com buster puppet5
    EOF
    wget -O - http://apt.puppetlabs.com/pubkey.gpg| apt-key add -

Update apt, installer les paquets *puppet-agent* & lsb-release:

    apt-get update
    apt-get install -y puppet-agent lsb-release

Ajouter ça au fichier /etc/puppetlabs/puppet/puppet.conf :

    cat >/etc/puppetlabs/puppet/puppet.conf <<EOF
    [main]
    server = palpatine.fdn.fr
    EOF

Lancer puppet pour générer un certificat SSL et attendre qu'il soit accepté par le master :

    puppet agent --test --waitforcert=5

C'est tout pour le client, il faut maintenant aller accepter sur le server le
certificat généré sur le client.

Une fois la première pass de puppet terminée, se déloguer, passer un coup d'etckeeper et relancer puppet agent pour terminer l'install : 

    sudo etckeeper commit
    puppet agent --test --waitforcert=5

### Sur palpatine

(Pour la suite, puppet doit être en train de tourner sur le client) Vérifier qu'on a bien une demande de certificat :

    puppetserver ca list

Et la signer :

    puppetserver ca sign --certname le-client.fdn.fr

Le nom du certificat devrait être le FQDN du client, sinon il y a un souci.

## Faire tourner puppet

### Sur les serveurs

Tant que la variable START est à "yes" dans /etc/default/puppet, pas de souci, le démon se lance au démarrage de la machine et lance une passe toutes les demi-heures.

### Sur les LNS

On peut aussi utiliser le script ./bin/apply du dépôt :

    ./bin/apply lns01.fdn.fr


## Procédure de migration utilisée pour passer à puppet5

Précédemment puppetmaster était sur leia. Il a été migré sur palpatine.

Sur palpatine, nous avons utilisé la doc de puppet :
https://puppet.com/docs/puppet/5.3/install_pre.html pour installer puppetserver
et puppetdb.

Ensuite pour chaque machine nous avons mise à jour l'agent selon la procédure suivante.

Sur chaque host on avait préalable poussé la conf apt suivante (adapter à
chaque os) grace a l'ancien puppet master:

    cat /etc/apt/sources.list.d/puppetlabs-puppet.list
    # This file is managed by Puppet. DO NOT EDIT.
    # puppetlabs-puppet
    deb http://apt.puppetlabs.com wheezy puppet5

Cela permet d'installer le puppet-agent en v5.

Pour le cas spécifique de yoda (os: squeeze) qui est trop ancien, nous n'avons
pu mettre que le puppet-agent v4. Il arrive tout de même bien à communiquer
avec le puppetserver v5.

Conf de yoda pour apt:
    cat /etc/apt/sources.list.d/puppetlabs-puppet.list
    # This file is managed by Puppet. DO NOT EDIT.
    # puppetlabs-puppet
    deb http://apt.puppetlabs.com squeeze PC1

La recette puppet dedié aux sources apt a été mise à jour par rapport à ces
adaptation.

Ensuite il suffit de désinstallé l'ancienne version, d'installer la nouvelle,
de créer le certificat utilisé pour puppet et de l'accepter sur le
puppetserver. Les commandes:

Sur HOSTNAME :

    apt-get remove --purge puppet
    rm -rf /etc/puppet
    apt-get install puppet-agent
    cat > /etc/puppetlabs/puppet/puppet.conf <<EOF
    [main]
    server = palpatine.fdn.fr
    environment = production_palpatine
    EOF

    etckeeper commit "Passage à puppet5"
    /opt/puppetlabs/bin/puppet agent --test

Sur palpatine :

    sudo -i puppetserver ca list
    sudo -i puppetserver ca sign --certname HOSTNAME
    sudo etckeeper commit "Integration de HOSTNAME à puppet"

Sur HOSTNAME :

    /opt/puppetlabs/bin/puppet agent --test --noop

    # Il est possible de que la commande avec --noop échoue. Auquel cas il faut corriger
    # les erreurs dans le dépôt puppet lié à la migration vers puppet5.
    # Quand il n'y a plus d'erreur :

    /opt/puppetlabs/bin/puppet agent --test


# Les modules

Les modules sont stockés dans deux répertoires :

* Le répertoire `modules` contient les modules de FDN.
* Le répertoire `thirdparty` contient les modules gérés par r10k. Ils sont
  spécifiés dans le fichier `Puppetfile`  pour les mettre à jour, il faut
  l'utilitaire r10k (paquet r10k).
  
      r10k pupppetfile install --puppetfile ManualPuppetfile
  
  Et commiter.

## base

C'est le module de base (comme son nom l'indique) qui devrait être inclus sur tous les noeuds.

Ce qu'il fait :

  * installation de locate avec sa config par défaut,
  * installation du script run-puppet dont il est question plus bas dans /usr/local/sbin,
  * installation de metche avec la config qui va bien.

## ganeti

Installe le nécessaire pour un noeud du cluster Ganeti. La config se fait manuellement, [[adminsys:ganeti|cf la doc]].

## users

Gère les utilisateurs.

## stats

Contient les scripts pour collecter les statistiques réseau

## vpn

Configure un serveur de vpn authentifié

## vpn-open

Configure un serveur de vpn openbar

## vpn-rw

Configure un NAT pour mettre openvpn sur tous les ports d'une adresse IP

# Hiera

Paragraphe rédigé par Nono et certifié valable le 23/04/2016.

La configuration de Hiera se trouve dans le fichier _/etc/puppet/hiera.yaml_ de _leia_. Les données Hiera sont dans le sous-répertoire _hieradata/_ du dépot Git Puppet ; on y trouve un fichier _common.yaml_ pour la config par défaut, et éventuellement un fichier par machine pour surcharger des options.

# La doc de puppet

http://docs.puppetlabs.com/
