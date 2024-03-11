
# Admincamp 2024 - Journal

Cet admincamp s'est fait en visio à défaut d'avoir pu trouver un lieu à temps.

Présent·es :

   * Ewen
   * Afriqs
   * Youpi
   * Tom28
   * As{m,}a
   * Pandaroux
   * henvi
   * Philippe aka papilip pour aloli
   * Éric
   * Jean-Michel aka grouick
   * Thibd
   * Khrys
   * Schtroumpf

## Accueil

Pour rappel, le déroulé sera le suivant avec de potentielles adaptation en cours de route :

   * Samedi 9 mars
       * 09h-10h -> Définition de la vision des admincore
       * 10h-12h -> Accueil des personnes intéressées par le groupe de travail adminsys (Avec webcam si possible pour voir nos bouilles)
       * 12h-12h30 -> Pause apéro/déj' (chacun chez soit mais pourquoi pas en discutant)
       * 12h30-14h -> Échange sur la supervision. Que veut-on faire ? Quelle solution technique ? etc
       * 14h-15h -> Présentation et échange sur ce que va devenir le SSO (LDAP, Keycloak, etc.)
       * 15h-00h -> Formation des micros groupes de travail et Yaka
   * Dimanche 10 mars
       * 00h-15h -> Travail sur les sujets Faukon
       * 15h-16h -> Discussion sur nos avancés du weekend
Nous referons très certainement une session de rattrapage sur l'accueil dimanche matin (10h-11h ?) pour les personnes ne pouvant pas être disponible samedi Si c'est votre cas, n'hésitez pas à le faire savoir.



## Vision des admincores

Rôle technique et de conseil, absolument pas politique.

Ouverture du groupe adminsys : nécessite de la motivation (notamment à lire de la doc)

   * Définition d'une méthode d'accueil (parrainage ? Recommandation - prérequis - de documentation ?)
Différence adminsys/admincore : clarification des rôles à prévoir : [https://git.fdn.fr/adminsys/wiki/-/blob/master/equipe/fonctionnement.md?ref\_type=heads](https://git.fdn.fr/adminsys/wiki/-/blob/master/equipe/fonctionnement.md?ref\_type=heads)



Admincore, qui continue ?

   * ewen
   * afriqs +1
   * tom28
   * Asma: J'arrête FDN (au futur) il y a 3 ans!
   * Pandaroux


## Tour de table

Présentation des personnes présentes

Discussion sur l'infrastructure de FDN, la documentation et les outils utilisés



## Service NTP

Migration des services NTP des machines physique lns11/22 vers une VM (séparation des services) ou vers les nouvelles VM LNS qui existent déjà ?

Service publique fournit avec les IP des LNS dont l'on veut se débarrasser -> changement de DNS

ntp.fdn.fr (pool FDN) :

   * ntp1.fdn.fr
   * ntp2.fdn.fr
   * pour l'instant vers les lns3[12] (qui ont déjà un serveur NTP pour leur propre synchro de toutes façons)
   * fait en séance (vers 12:30)
   * Après plus de 24h (TTL DNS), on a éteint les lns{11,22} vers 21:30, on peut déracker !
Dans un second temps faire des conteneurs ? De manière plus générale réfléchir au déploiement de containers (par exemple LXC) avec config FDN.

> j'avais testé en pratique le script d'install actuel n'est pas si adhérent que ça au fait que ce soit des VM, mais quite à faire des containers je serais pour sortir du moule puppet et gérer des dockerfile / containers "stateless" avec uniquement un service qui tourne, pour des trucs comme NTP c'est bien plus simple...



## De Etherpad à HedgeDoc ?

[https://hedgedoc.org/demo/](https://hedgedoc.org/demo/)

installation en parallèle avec Etherpad dans un premier temps

   * pad2.fdn.fr ?
   * installation test sur sandbox @thibd @henvi
       * bon accès à donner, envoyer un e-mail services@
à terme, installation sur la même VM qu'Etherpad ?



## Changement de registraire ?

Un pad dédié est ouvert => [https://pad.fdn.fr/registraire](https://pad.fdn.fr/registraire)

Que je recopie pour l'historisation :

### Contexte ###
Changement d'orientation de Gandi n'étant plus en adéquation avec FDN ? Gandi n'est plus Gandi depuis son rachat par une société commerciale peu éthique + augmentation des tarifs.

Les noms de domaine de FDN arrive bientôt à expiration. Avant de les renouveler pour une période plus ou moins longue ils seraient intéressant de se poser la question de notre avenir avec Gandi.

   * fdn.fr : 2024-12-21
   * fdn.org : 2025-05-31


https://next.ink/1282/gandi-fusionne-avec-total-webhosting-solutions-tws-pour-devenir-your-online-et-cela-inquiete/
> Note : ne semble pas être un sujet prioritaire


#### Candidats
Comparatif des différents NDD fait par l'équipe de NexInpact (alias Next)  (googledoc :()  
https://docs.google.com/spreadsheets/d/1hKss7oFiWwg_CmbyVSlQyxkymV1lhgkMP7CQ2BeDKbE/edit#gid=0

##### BookMyName #####

Scaleway -> Groupe Iliad

##### Infomaniak #####

Entreprise suisse : qu'est-ce que cela peut impliquer ?

Attention tout de même, chez infomaniak le "Domain Privacy" (cacher les coordonnées d'un domaine dans le WHOIS) est facturé (2,40 euros/an) en plus 

## Supervision



### Besoins

Avoir une vision des services (technique, systemd) qui fonctionnent sur le machine et un certains nombre de métrics. Visualisation sur 1 an (avec agrégation/consolidation)

   * alerter pour intervention
   * réponse à incident post mortem avec rétention sur 1 an
   * Commencer par collecter relativement peu de metric et en ajouter lorsque que l'on se rend compte du besoin
Visualisation fonctionnelle du statut des services.



#### Outils "traditionnels"

   * Centreon ([https://www.centreon.com/fr)](https://www.centreon.com/fr))
   * Zabbix ([https://www.zabbix.com)](https://www.zabbix.com))
   * LibreNMS ([https://www.librenms.org)](https://www.librenms.org))
   * Munin ([https://munin-monitoring.org)](https://munin-monitoring.org))
   * ...


#### Outils "plus modernes"

#### Collecte des métriques :

   * Netdata ? ([https://www.netdata.cloud)](https://www.netdata.cloud))
   * node exporteur ? ([https://github.com/prometheus/node\_exporter)](https://github.com/prometheus/node\_exporter))
   * telegraph ([https://www.influxdata.com/time-series-platform/telegraf)](https://www.influxdata.com/time-series-platform/telegraf))
   *  ...


#### Centralisation des métriques :

   * Prometheus ? ([https://prometheus.io)](https://prometheus.io))
   * VictoriaMetrics ([https://victoriametrics.com)](https://victoriametrics.com))
   *  ...


##### Visualisation

   * Grafana ([https://grafana.com)](https://grafana.com))


/!\ Il ne faut pas que ça devienne une usine à gaz -> donc pas Centreon ?? !!!



## SSO/IAM - Une identité pour les gouverner tous. Une identité pour les trouver. Une identité pour les amener tous et dans les ténèbres les lier.



Outils utilisés :

   * OpenLDAP ([https://www.openldap.org)](https://www.openldap.org))
   * Keycloak ([https://www.keycloak.org)](https://www.keycloak.org))


Keycloak/Puppet :

   * Gestion de l'installation
   * Gestion simple de la configuration (keycloak.conf)
   * Reste à faire
       * Gestion de la configuration infinispan (cache-ispn.xml)


Base de données Keycloak

   * Cluster MariaDB/Galera en cours de création
       * À mutualiser avec d'autre service interne (cf. voir  la liste au point « Inventaire base de données »)


LDAP :

   * Déplacement des comptes adhérent dans l'arborescence
   * Reconfiguration des outils pour prendre en compte le changement d'arborescence (Gitlab, Vador, Pad, Peertube)
       * Peertube semble OK, mais je n'arrive pas à valider
       * Ancien Keycloak pas fait, pas de compte admin connu et difficulté d'accès à la base de données (h2)


## Groupes de travail

   * SSO/IAM : Puppetisation du Keycloak
       * Ewen
       * Philippe
       * Pandaroux
   * supervision
       * Thibd


## Fait en vrac



### Mises à jour

* solo : Tom
   * RAM 2 Go -> 4 Go
   * /var 35 Go -> 40 Go
   * buster -> bullseye -> bookworm
   * suppression de lighttpd (migration de la partie HTTP vers apache2 qui gérait déjà HTTPS)
   * ménage feeds NNTP morts (freenix glou.fr.eu.org ac-versailles lautre neva.ru schtroumpfette.biz ircam.fr poupinou francinet)
   * ménage feeds UUCP morts (diablo bandini calahan cin dust elessar esip graville gnext le-bar lods ludwig madmex moof nexty rebours shaman toporko ubix)
   * si des adhérents n'arrivent plus à se connecter en UUCP, ils doivent probablement adapter leur configuration comme suit : dans /etc/uucp/sys, remplacer "chat ogin: \L word: \P" par "chat ogin: \L word: \P\r\n\c"
* cecinestpasleia : asma
   * munin / repo Debian fdn OK
   * nagios3 KO (depend d'un vieux perl plus dispo, sources du package +fdn1 pas trouvable...) -> bricolage sur nagios4 qui marche plus ou moins bien, mais qui suffira bien en attendant "La Supervision"
* rey : afriqs
   * bullseye -> bookworm
   * rajout de 10 Go pour /srv
   * ajout module PHP imagick sur les versions installées
* sebulba : afriqs
   * buster -> bullseye -> bookworm + dernière version gitlab-runner et docker
* coruscant : afriqs
   * buster -> bullseye -> bookworm
* scarif : afriqs
   * PBS 2.4.1 -> 2.4.6
* palpatine : doublement taille / (+10 Go) pour avoir plus d'inodes


### Suppressions VM

   * ~~yoda~~
   * ~~bibliogram~~
   * ~~obiwan~~
   * ~~rsf~~
   * ~~fdn2~~
   * ~~resolver.test~~
   * ~~katarn~~
   * ~~bane~~


### Doc ??? :p

   * wiki adminsys
       * suppression références VM supprimées
       * suppression ganeti
       * Nettoyage VLAN inutilisés
   * Nettoyage des tickets dans les différents projets Gitlab


### Autre

   * LNS
       * vieux lns11/22 : MySQL, Freeradius éteints
       * migré les IP 10.0.0.35 et .36 du VLAN d'admin sur les LNS3{1,2}, pour le NTP avec les switchs
       * corrigé la conf NTP pour bookworm (-> ntpsec)
       * fix de la création du dossier stats dans /run au boot
       * ajout d'une dépendance bird/l2tpns pour que le reboot attende un peu entre la coupure de l2tpns et la coupure du bird/le reboot


### Inventaire base de données

   ```
    $ clush -ba systemctl is-active mariadb

    ---------------

    boba.fdn.fr,chewie.fdn.fr,jyn.fdn.fr,radius[0-1].fdn.fr,rey.fdn.fr,si.fdn.fr,skytop.fdn.fr,solo.fdn.fr,taslin.fdn.fr (10)

    ---------------

    active

    ---------------

    anakin.fdn.fr,bbb.fdn.fr,c3px.fdn.fr,capsule.fdn.fr,cecinestpasleia.fdn.fr,coruscant.fdn.fr,dgsi.fdn.fr,gchq.fdn.fr,geeknode3.fdn.fr,guardian.fdn.fr,gw[1-2].fdn.fr,invidious.fdn.fr,jira.fdn.fr,lns[31-32].fdn.fr,mustafar.fdn.fr,neo.fdn.fr,nitter.fdn.fr,nsa.fdn.fr,onion.fdn.fr,pad.fdn.fr,padme.fdn.fr,palpatine.fdn.fr,pz4co.fdn.fr,r5d4.fdn.fr,r4p17.fdn.fr,resolver[0-1].fdn.fr,sabe.fdn.fr,sebulba.fdn.fr,talk.fdn.fr,tc14.fdn.fr,tiree.fdn.fr,turn.fdn.fr,vpn[1-10].fdn.fr,vpn-open1.fdn.fr (46)

    ---------------
   ```
    
   ```
   $ clush -ba systemctl is-active postgresql

    ---------------

    invidious.fdn.fr,jira.fdn.fr,neo.fdn.fr,pad.fdn.fr,palpatine.fdn.fr,tiree.fdn.fr (6)

    ---------------

    active

    ---------------

    anakin.fdn.fr,bbb.fdn.fr,boba.fdn.fr,c3px.fdn.fr,capsule.fdn.fr,cecinestpasleia.fdn.fr,chewie.fdn.fr,coruscant.fdn.fr,dgsi.fdn.fr,gchq.fdn.fr,geeknode3.fdn.fr,guardian.fdn.fr,gw[1-2].fdn.fr,jyn.fdn.fr,lns[31-32].fdn.fr,mustafar.fdn.fr,nitter.fdn.fr,nsa.fdn.fr,onion.fdn.fr,padme.fdn.fr,pz4co.fdn.fr,r5d4.fdn.fr,r4p17.fdn.fr,radius[0-1].fdn.fr,resolver[0-1].fdn.fr,rey.fdn.fr,sabe.fdn.fr,sebulba.fdn.fr,si.fdn.fr,skytop.fdn.fr,solo.fdn.fr,talk.fdn.fr,taslin.fdn.fr,tc14.fdn.fr,turn.fdn.fr,vpn[1-10].fdn.fr,vpn-open1.fdn.fr (50)

    ---------------

    inactive
   ```


## Synthèse du WE

   * Globalement satisfaisant mais un peu de déception que ce soit en virtuel et non en physique.
   * Déroulement un peu plus cadré ?
   * Difficulté de focalisation en mode virtuel. Plus simple en physique.
   * De la découverte et de l'intérêt pour les sujets abordés.
   * Penser à faire un mode hybride physique+virtuel
   * Faire un nettoyage des tickets.
   * Prévoir des ateliers plus spécifiques.
