[[!meta title="Choses à faire - TODO"]]

# NOTE : NE PLUS METTRE À JOUR (READ ONLY et non maintenue) [Version à jour](https://git.fdn.fr/adminsys/suivi/issues)

En cours
--------

### Netoyage des objets RIPE de FDN (olb)

Ça a bien sédimenté...

### Installation de librenms (olb & wannig)

Commencé lors du weekend de l'AG et continué à l'admincamp du 19/20.

Librenms est opérationel, et sont monitorés lns11, lns22, resolver0, resolver1, boba, c3px, r4p17 ainsi que les deux switchs.

Il reste à proprager le réseau intra sur toutes les machines de fdn. Le daemon snmpd s'installe et se configure automatiquement via puppet sur ce réseau lorsqu'il existe (sur la loopback sinon).

### [RTC] Radius pour le RTC

Cf mail youpi 5 mars 2017, plus corrections ici:

- corriger la cible radius en 80.67.169.41 et 42
- y faire arriver les requêtes pour @fdn.nerim aussi
- y faire arriver les requêtes pour @fdn.dslnet.fr aussi
- y faire arriver les requêtes pour @vpn.fdn.fr aussi
- faire marcher toto/toto

(wannig est sur coup)

### [noyau] puppet / apt update

- faire apt update avant install pkg dans puppet

### Refonte Monitoring (belette)

- installation VM et configuration de libreNMS
- choisir quoi monitorer (reflexion sur ce qui manque actuellement)

	{Stephane le 23 Juillet 2018 a minuit et demie}: detecter une panne de syslog(cas arrive sur Solo au premier semestre 2018)

- remplacement de Nagios @ isengard (choisir Icinga ou Shinken)

*choses à discuter dans le pad du camp n°15*

### Supervision end-user (isengard) (belette)

- isenbot auto start au boot
- régler un problème postfix sur isengard
- IPv6 lost quand isengard reboot, check network config
- ajouter rsf.fdn.fr pour sonde openvpn (actuellement que ICMP et SSH sont testés...) + exception IP isengard dans fail2ban
- amélioration des tests sur les URLs pour éviter faux-positif lors d'un HTTP 302
  - vador.fdn.fr
  - git.fdn.fr
  - lists.fdn.fr
  - si d'autres où le site n'est pas à la racie me mettre la liste ici svp

- refaire une passe sur toutes les machines et services en monitoring
- amélioration des check sur les lns, les droides (quoi tester?)
- amélioration check_vpn pour passer par www.fdn.fr
- ajout check_imap
- réflexion sur sonde PPP (permet de faire un test bout en bout avec Radius,l2tpns..)
- mettre un serveur dns faisant autorité pour isengard pour voir la page de status même si l'infra de fdn est par terre
- ajouter un tag sur nos pages en pullant une info via requete SQL pour vérifer fonctionnement multi-tier end-to-end
- check_dns via IPv6 cassé dans le plugin nagios (https://github.com/nagios-plugins/nagios-plugins/issues/154#issuecomment-3092872) en attente d'un fix


*plus d'information sur le mail envoyé @ adminsys le 8 Feb 2018 23:21*

### Résumé des erreurs de notre infra d'après isengard (vue extérieure)

- ackbar.fdn.fr
  - TCP 443 fermé
  - pas de let's encrypt
  - pas de redirect permanent sur 443

- blog.fdn.fr
  - pas de let's encrypt
  - pas de redirect permanent sur 443

- droides.fdn.fr
  - pas d'IPv6

- media.fdn.fr
  - TCP 443 fermé
  - pas de let's encrypt
  - pas de redirect permanent sur 443

- usenet-fr.fdn.fr
  - pas de let's encrypt
  - pas de redirect permanent sur 443

- www.fdn.fr
  - le certificat principal est blog-devel.fdn.fr lors d'un test sur le root

- www.open.fdn.fr
  - pas de let's encrypt
  - pas de redirect permanent sur 443

- yoda.fdn.fr
  - pas de let's encrypt
  - pas de redirect permanent sur 443

- guri.fdn.fr
  - pas présent dans Cachet
  - aucun test dans Nagios

### solo/imaps qui part dans les choux (tom28)

Il fallait "simplement" appliquer deux patches. Deux bugs sont déjà ouverts
pour ça côté Debian :

  - https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=879007
  - https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=863520

=> en attendant que les paquets officiels Debian incluent ces patches, un
paquet custom a été compilé et installé sur solo, et les paquets marqué en
"hold".

### Nouvelle infra mail (vg, tom28)

Séparer les différents services actuellement rassemblés sur solo. Voir CR
admincamp 2018-09-19.

### Matrix/Synapse/pz4co
  - Gérer le restart de synctl lors de la generation de certificat letsencrypt
  - Fine tuning nom affiché dans /who IRC
  - Renommer le bot côté Matrix comme celui d'IRC: pz4co
  - Augmenter le timeout des users matrix sur les chan irc
  - Com sur site + membres ffdn
  - Réféchir sur inscription users: vs CLI => API add user   

En souffrance
-------------

### Le bloc vpn pour l'outre est-il utilisé ?

Il s'agit de 80.67.173.0/27.

### ajouter certificat let's encrypt sur ackbar

### Envie de transformer ackbar en nœud peertube

À voir avec thy, qui s'occupe actuelement de ackbar.

### Mise en place de backup chez globenet

À priori, Globenet est ok, il faut faire une demande officielle.  L'idée c'est
que les backup soient dans futures pas trop éloigné sur des machines qui vont
être mises au CICP.

On partirai sur backupninja + borgbackup.

Cf [[cr/20180519-camp]]


### Le 10G on s'organise ?

Achat de matériel pour passer les passerelles et les droîdes en 10G (objectif
admincamp de septembre).  Cf [[cr/20180519-camp]]


### Problèmes SYMPA suite à la mise à jour de solo en stretch

[2018-07-22 : a priori résolus, en attente de confirmation par Rosemonde]

  - voir avec olb/sebian les différences de config entre FDN et Gitoyen
  - voir si jcd aurait une idée

  - "Problème SYMPA" de "Trésorerie FDN - R. Let" <rletricot@fdn.fr> du 2018-03-25
    - Problèmes dans la partie "Documents Partagés" de l'interface Web de SYMPA


### "[DNS] Souci de résolution DNSSEC vers le domaine isc.org" de "kittycat.fr hostmaster" <admin@kittycat.fr> du 2018-03-16

À investiguer, probablement lié aux règles anti-DDoS. Voir également le mail
"DNS" de youpi du 2018-03-14 qui en parle aussi.

### Warning sur les volume groups des droides

sur les droides, on a quelques volume groups en Warning :

```bash
$ gnt-cluster verify

Sun Oct 15 15:41:49 2017 * Verifying orphan volumes
Sun Oct 15 15:41:49 2017   - WARNING: node c3px.fdn.fr: volume vg1/ef333305-cc5e-49d5-b931-123ec8866532.disk1_data is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node c3px.fdn.fr: volume vg1/swap is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node c3px.fdn.fr: volume vg1/efeb21c2-1710-462c-90b2-783604bbf9bc.disk0_meta is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node c3px.fdn.fr: volume vg1/ef333305-cc5e-49d5-b931-123ec8866532.disk1_meta is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node c3px.fdn.fr: volume vg1/efeb21c2-1710-462c-90b2-783604bbf9bc.disk0_data is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node r4p17.fdn.fr: volume vg1/swap is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node r4p17.fdn.fr: volume vg1/7c3a33a8-c63a-47aa-8f48-4237cbaf10c5.disk1_meta is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node r4p17.fdn.fr: volume vg1/efeb21c2-1710-462c-90b2-783604bbf9bc.disk0_meta is unknown
Sun Oct 15 15:41:49 2017   - WARNING: node r4p17.fdn.fr: volume vg1/ef333305-cc5e-49d5-b931-123ec8866532.disk1_meta is unknown
Sun Oct 15 15:41:50 2017   - WARNING: node r4p17.fdn.fr: volume vg1/a72b22c3-378c-4661-96d3-9901392d2355.disk0_data is unknown
Sun Oct 15 15:41:50 2017   - WARNING: node r4p17.fdn.fr: volume vg1/a72b22c3-378c-4661-96d3-9901392d2355.disk0_meta is unknown
Sun Oct 15 15:41:50 2017   - WARNING: node r4p17.fdn.fr: volume vg1/7c3a33a8-c63a-47aa-8f48-4237cbaf10c5.disk1_data is unknown
```

### [noyau] etckeeper : faire un mail à admin@ quand /etc change

### [dns] migration des resolvers DNS sur resolver2

Leia est encore resolveur.

### [vpn] supprimer l'ancienne allocation dans le reverse DNS

de 2001:910:802::/64 qui ne servira pas finalement.

### [noyau] cluster ganeti : fermer les ports ou resteindre les services inutilement ouverts

### [monitoring] déplacer le check apt dans check_mk et virer nagios-nrpe

### [noyau] Harmoniser configs sshd via puppet (nono conseille https://forge.puppet.com/saz/ssh)

### [noyau] Migrer repo apt FDN de leia vers obiwan (?) + documenter / reprepo

### [dns] générer des RDNS pour les IPv6 attribuées

Pour pouvoir émettre des mails de nos jours, il faut avoir un RDNS valide. En
IPv6 on ne peut pas pré-générer tout un /64 :)

Idéalement, il faudrait voir ce que permet le serveur dns comme traduction
automatique. Sinon, les adhérents doivent explicitement demander un RDNS pour
leur serveur juste pour pouvoir émettre du mail, c'est relou, alors qu'en IPv4
ça ne posait pas de problème.

Sinon, on peut au moins mettre un RDNS sur l'adresse IP que l'on fait configurer
automatiquement (2001:910:1xxx:ffff::1), avec un truc du genre

    $GENERATE 0-255 reverse-$.fdn.fr.  IN AAAA 2001:910:10${0,2,x}:ffff::1
    $GENERATE 0-255 reverse-$.fdn.fr.  IN AAAA 2001:910:11${0,2,x}:ffff::1
    $GENERATE 0-255 reverse-$.fdn.fr.  IN AAAA 2001:910:12${0,2,x}:ffff::1
    $GENERATE 0-255 rev$.vpn.fdn.fr.   IN AAAA 2001:910:13${0,2,x}:ffff::1

    $GENERATE 0-15 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.f.f.f.f.${0,1,x}.0.0.1.0.1.9.0.1.0.0.2.ip6.arpa. PTR reverse-${0,0,d}.fdn.fr.
    $GENERATE 0-15 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.f.f.f.f.${0,1,x}.1.0.1.0.1.9.0.1.0.0.2.ip6.arpa. PTR reverse-${16,0,d}.fdn.fr.
    ...

### [monitoring] détecter quand les esclaves sql sur les lns n'arrivent plus à se synchroniser avec le maître

Ça arrive notamment quand on fait une requête SQL qui porte à la fois sur des tables répliquées (RADUSER, UATTR, GATTR) et sur d'autres tables, par exemple

   update UATTR, RADUSER, VPN set UATTR.UATTR_VALUE="toto" where UATTR.UATTR_ATTR="User-Password" and UATTR.RADUSER_ID = RADUSER.RADUSER_ID and RADUSER.VPN_ID = VPN.VPN_ID and VPN.CLIENT_ID=372;

### Faire une passe une fois par an pour vérifier les comptes (à faire cette fois-ci) -> olb \& belette

### Automatisation des backups puppet + borg

### VPN: Reflexion sur limite de BP par utilisateur en plus de la BP globale de la VM

   *     Voir travaux sur \url{https://wiki.fdn.fr/travaux:vpn\_misc:bw} , pour l'instant le module vpn-open contient un script bw-limit beaucoup plus simple, mais qui est déjà équitable au moins

### VPN: définir de nouveaux noms de domaines pointant vers les serveurs VPN

 wildcard net.fdn.fr a été ajouté dans nos entrées DNS et pointe vers nos 3 serveurs VPN, il reste à générer les certificats pour stunnel et voir si stunnel peut gérer plusieurs certificats car il ne faudrait pas faire apparaitre net et vpn dans le même pour rendre la tâche plus difficile aux solutions de DPI qui viennent fouiller là-dedans. (et aussi dans une autre mesure le faire disparaître de la première requête DNS)

Depuis Mars 2018, let's encrypt supporte les wildcard! Il faudra ajouter une entrée DNS TXT dans le sous domain pour le challenge et voir comment le distribuer automatiquement sur les 3 serveurs VPN.(à discuter avec les copains en admincamp)

### Préparer le déplacement d'un LNS vers Bourse et un droide vers TH2

a préparer pour le prochain admin camp
→ olb, fsirjean?, tom28?, vince?

déplacement pour celui d'après

### Généraliser fail2ban et virer denyhosts si présent, a pupetiser -> noyau

### Ajout de fail2ban pour IPv6 pour (au moins) vpn1/vpn2/vpn3/guri/rsf

### Upgrader les VMs vpn

Pour avoir de bons algos de crypto.

Au minimum vers Jessie comme vpn3, et essayer d'upgrader à Stretch

### Ajouter exception dans le module base de puppet pour ne pas appliquer la configuration postfix sur jira

### Ajouter exception dans puppet pour les sources.list.d pour rey (besoin de php-pfm)
