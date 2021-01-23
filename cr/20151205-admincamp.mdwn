[[!meta title="Admincamp n°3 - 5/6 décembre 2015"]]
[[!meta date="20151205"]]
[[!tag done]]

Lieu : Paris, dans les locaux de la quadrature du net.    
Présent·e·s : Fabien, Capslock, Benjamin, Thomas, Mat, Olivier, Quota, Scara

[[!toc levels=3]]

# Rappels de l'infrastructure de FDN

- 7 machines physiques, 2 switchs
- 2 points de présence : TH2 / Paris bourse

- machines hébergées dans un bout de baie
  - TH2 : 3 machines : 2 LNS + Vador
  - Bourse : 4 droides (2 vieux et 2 nouveaux)


## Cluster de VM

- 4 machines pour le cluster
  - 2 machines nouvelles 
  - 2 machines historiques sorties du cluster ; non réintégrées au cluster (reste à faire)

- On a des problèmes de performance disque (raid6 et disques pas rapide)

- dans l'optique de fournir un service de vm aux membres :
  - il faut reflechir au cloisonnement entre les VM FDN et les autres
  - il nous manque une connexion avec le SI (provisionnement, facturation)
  - il nous reste à voir le provisionnement des VM (possibilité entre autres de proposer le chiffrement des VM)


# Trucs à faire

- Rennomer les LNS 11=>01, 22 => 02 ?
- Supervision -> check_mk ? nouvelle vm
- Anciens droïdes
- gitlab ? mise à jour ? virer ? vm à part ?
- Achat de matos
- Offre vm abonné (quid Raqmiya)
- Problématique perf cluster
- Et renvoyer le disque cassé que bientôt plus de garantie
- Vador: empire contre attaque (extinction de vador)
- écouler les différentes demandes formulées sur la ML

# Trucs faits / en cours

- [fait, mat] Créer un contact technique gandi adminsys pour les domaines de FDN
- [fait: olb, fabien] Puppet r10K, fusionner les dépôt
- [fait: olb] Mettre etckeeper dans puppet à FDN 
- accès root : rsf / ackbar / ... (fait : toutes les machines de FDN (sauf vador) sont dans puppet, les users sont gérés avec)
- [fait: capslock] Rallumer munin non public
- [fait: olb] Relation equip communication
- [fait, fabien] purge adminsys (fait, mail pour benevoles envoyé)
- Lancement du nouveau wiki adminsys
  - [fait, benjamin, olb] étude liaison apache -> radius
  - [fait, olb] conf apache et backportage vers jessie de libapache2-mod-auth-radius
  - [benjamin] conf radius
- Mise en place des resolveurs (faut attendre cf plus bas)


## Séparation des resolveurs et des dns faisant authorité

Actuellement .12 (leia) et .40 (vador) font à la fois resolveur et dns faisant
authorité. L'idée est de séparer les resolveurs des serveurs faisant
authorité. Deux mini vm on été créées pour les [[services/resolveurs dns]] et sont
prêtes.

Ce qui a été fait à l'admin camp :

 - Un contact contact technique gandi a été créé (AM16006-GANDI Prénom: Ad, Nom: Minsys)
 - Diminuer le TTL de la zone FDN (mat: fait)
 - Affecter deux nouvelles ip pour les serveurs de noms faisant autorité (.25/.26)
 - Leur trouver des noms (nsa gchq)
 - Changer les glue record à Gandi (fait pour les zones auxquelles j'ai accès)

Ce qui reste à faire :

 - Envoyer un mail aux adhérents pour les zones qui ont des glues record sur les anciennes ip.
 - Augmentation du TTL de la zone FDN
 - Déplacement des IP .12 et .40 sur les deux nouvelles machines (resolver1 / resolver2)



## Gestion des utilisateurs

- Les comptes administrateurs sont gérés par puppet ont un uid > 2000.
- Les comptes liés à des serviecs (exemple solo et yoda) ne sont pas géré par puppet.


## Munin

- Vhost réactivé
- Ajout du support HTTPS
- Seul TLSv1.2 est accepté
- Update de la ciphersuite ; basé sur https://wiki.mozilla.org/Security/Server_Side_TLS#Modern_compatibility
- Page wiki à jour https://adminsys.fdn.fr/outils/supervision/munin/

## blog-devel.fdn.fr

Mise en service de l'instance de développement du blog de FDN.

Opérations effectuées :
    * backup du dotclear de prod (fichiers et sql)
    * Copie du dump sql vers chewie
    * Installation de dotclear 2.8.2; intégration du dump sql
    * update de la base dc_blog pour faire matcher blog_url avec blog-devel.fdn.fr

Question en suspend : laisse-t-on les mêmes utilisateurs, les mêmes mots de passe (et donc les mêmes hash)

