
### Vpn openbar 

- blackmoor : Tests sur le vpn openbar pour avancer sur le tuto du futur site web.
- Vg : correction des problèmes de compilation de pelican pour le site du vpn openbar sur chewie. Python 3.4 needed, à voir ? Scripts de déploiement du vpn openbar sur le modèle du site web fdn.

### Mise en place de la collecte DSL Liazo

- CapsLock / Fabien : on a mis en place les sessions BGP avec Liazo (modulo un problème coté Liazo qui n'est toujours pas résolu) ; on a appris radius et commencé à le confer ; il nous reste à passer dire bonjour sur L2TPNS et faire un premier test. Il restera alors à Benjamin d'avancer sur le SI.

### Monitoring

- Belette : monitoring des vpn : mise en place d'une sonde qui permet de vérifier que les vpn fonctionnent. Il bosse aussi sur "l'expérience utilisateur", càd voir l'état des services d'un point de vue utilisateur. Un compte de radius de test vpn a été créé pour les sondes d'Isengard (conf radius).

### Déplacement de gitlab

- Capslock : commencé à préparer une VM pour soulager leia de son gitlab (kamino.fdn.fr)

### VPN

- youpi : modification de la conf exemple VPN pour essayer différents profils: dans l'ordre UDP 1194, UDP 53, UDP 123, TCP 443, TCP 993, TCP 22, TCP 80.

### Divers

- Fabien : créé un compte htpasswd sur le SI pour Stéphane Ascoet
- olb: Déprovisionner la conf radius pour tétaneutral : checks nagios, conf radius.
- olb: Ajouter un check puppet dans check_mk pour vérifier que les puppet tournent bien.
- olb: puppet & etckeeper: désactivation du postrun qui faisait que puppet commitait tout le temps
- olb: répératation du cluster ganeti (soucis de VG)
- olb: let's encrypt: La conf d'une machine est entièrement puppetisée (et appliquée seulement sur
  les machines qui en ont besoin)
- olb: let's encrypt: https://lists.fdn.fr
- olb: let's encrypt: kylo: reparation de la conf apache pour acme_renew (Il manquait un "Require granted all". Probablement suite à une maj vers jessie)
- olb: puppetiser la conf des droïdes pour jessie (notamment /etc/lvm/lvm.conf)
- olb: Mise en place le système de rôles pour les authorisations dans puppet


