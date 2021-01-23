### Accueil des nouveaux, accès & comptes

Samedi matin, nous avons fait le tour de l'infrastructure et des services de
FDN en se basant sur le schéma fait par belette et olb.

Samedi en début d'après midi nous avons promu belette en tant que membre du
noyau adminsys et créé les comptes des nouveaux membres d'adminsys : prunus
et openponey.

### Ammélioration du wiki adhérents

(OpenPoney) Lorsque l'on clic sur le bouton "Wiki" du site web fdn.fr on ne tombe pas sur
la page de login (si pas co) ou d'accueil (si déjà co)

### Avancée sur la messagerie instantanée

- (olb) création de la vm jyn pour migration jabber (messagerie instantanée)
- (wannig, prunus) test de prosody
- (wannig, prunus) test de migration des comptes de ejabberd vers prosody sur jyn (3000 comptes)

Nous prévoyons la migration pour le prochaine admincamp (un trentaine de
comptes ont des contacts). Il y aura également un certificat let's encrypt à
générer.  Il y a néamoins deux questions à trancher par le buro : 

- que fait-on des comptes qui n'ont pas de contacts ? (et que l'on suspecte
  fortement d'être des robots)

- quelle serait la politique d'ouverture des comptes pour le nouveau
  serveur ?

### Migration de vpn1 en 64bits (non finie)

- (belette & olb) création de la machine vpn3
- (youpi?) correction scripts puppets vpn, ils devraient fonctionner correctement pour reconstruire une VM de zéro

### Modification config par défaut cluster Ganeti (performances)

(tom28)

(Sur demande de youpi pour les vpn, mais on a décidé de l'appliquer à toutes
les VM par défaut)
    
Pour une VM spécifique : gnt-instance modify -H
cpu_type=qemu64,+pclmulqdq,+ssse3,+sse4_1,+sse4_2,+aes,+avx

Pour la config par défaut du cluster, il faut jouer un peu avec des échappements :
    
    root@r4p17:/home/tom# gnt-cluster info | grep cpu_type
        cpu_type: 
    root@r4p17:/home/tom# gnt-cluster modify -H kvm:cpu_type='qemu64\,+pclmulqdq\,+ssse3\,+sse4_1\,+sse4_2\,+aes\,+avx'
    root@r4p17:/home/tom# gnt-cluster info | grep cpu_type
        cpu_type: qemu64,+pclmulqdq,+ssse3,+sse4_1,+sse4_2,+aes,+avx
    root@r4p17:/home/tom# 

Note : cette nouvelle configuration ne sera effective qu'après redémarrage complet des VM (ça se fera donc tout seul au fil de l'eau...)

### Traitement de mails en attente

- (tom28) demandes DNS en attente
- (blackmore) réponses à des gens qui veulent participer à adminsys
- (blackmore) création d'une VM exegetes2.fdn.fr (dans le but de migrer la VM actuelle exegetes.eu.org)

### Tri de la liste des choses à faire

(blackmore)

### mails : Passer sur la config SSL/TLS des mails

- (vg) migration du certificat de cyrus-imap (serveur imap et pop) sur certificat Let's Encrypt

### Mise en place de la collecte xDSL Liazo

- (wanig, olb) duplication de la config faite sur lns22 sur lns11
- (wanig, olb) redémarrage complet des deux lns
- (wanig, olb) test du failover du cluster l2tpns
- (wanig, olb) puppetisation de la conf radius & l2tpns

Il manque les info d'interco pour LNS22 et Liazo. On a besoin de trois nouveaux
/31 (radius, besteffort, premium).

On a également constaté que les l2tpns ne remontaient pas correctement au
redémarrage des machines. Le service s'allume bien, mail il se déclare master,
se fait jeter par l'autre master et se tue (pb réseau au démarrage ?).


### Normalisation de la conf apt dans puppet

- (olb) La configuration des dépôts APT de chaque n'étaient pas gérée par puppet et
c'était un peu le brun. Maintenant, le fichier source.list et le contenu du
répertoire source.list.d sont entièrement gérés par puppet.

Remarque : si par aventure nous avions des machines plus vielles que wheezy ou
avec des dépôt exotiques autres que celui de sames, de fdn ou de puppetlabs, il
faudra configurer tout ça dans puppet.

### Mise à jour de l2tpns pour que l'ipv6 marche correctement

- (olb) l2tpns n'envoyait pas de RA régulièrement comme la RFC le prévoit et cela
fait que l'ipv6 marchotait en configuration automatique (selon les modèles des
routeurs des abonnés). Il a été patché récemment pour corriger cela et nous
l'avons mis à jour, donc.

### Compatibilité des SFP solid-optics avec CISCO en 100Mbps

(fait le lundi matin avant de prendre le train )

- (olb) Nouvel épisode sans la saison de "des SFP pas compatible 100Mbps en
  cuivre". Alturna nous a demandé de lire un SFP GLC-T Cisco avec
  multi-fiber-tool. Ce qui a été fait. En retour, il nous ont demander
  d'appliquer la marque MSA sur un SFP Solid-Optics mais cela ne fonctionne pas.

  Les ingénieurs de solid optics nous ont préparé trois hot fix à tester sur
  les SFP GLC-T pour la compat 100Mbps, je n'ai pas eu le temps de les tester.

### Préparation de l'installation des switchs

(tom28, nono) Voir prochain admincamp.
la prochaine fois, 5/6 août, nous imagions :
    
  * pousser la conf sur le switch
  * racker le switch à bourse
  * le mettre en // avec une nouvelle interco 10G avec gitoyen
  * brancher les machines dessus

  Ce que nous avons à faire pour la prochaine fois :

  * SFP en 100Mbps (on en a besoin d'au moins 6 idéalement 8 ou 10):
    - (olb) pousser alturna à trouver une solution
    - (belette) demander à Laser2000
    - faire un devis pour 6 SFP cisco GLC-T

  * (belette) avoir 16 écrous cage
  * (tom28) avoir une scie à métaux pour les rails à th2 (because baie de taille télécom, demander à sebian pour + de détail)
  * (tom28, belette) avoir des tournevis 
  * (belette) avoir des patch fibre mono-mode (2 en tout)
  * avoir des patch r45
  * (olb) demander à Liazo de mettre en place une nouvelle interco fibre entre notre demi baie et la baie de l'autre.net (support@)
  * (olb) prévenir liazo de notre intervention (support@)
  * (olb) prévenir gitoyen pour qu'il prépare leur switch
  * (olb) demander une vm à gitoyen avec accès publique et avec réseau d'admin (vlan 801)

Ce que l'on a à faire pour la fois d'après :
    
  * finir la configuration du switch pour TH2 sur https://pad.gresille.org/p/sa0iethe-fdn-admincamp-20170311
  * pour TH2, est-ce que l'on utilise un U supplémentaire temporairement, ou est-ce que l'on remplace en mode ninja



