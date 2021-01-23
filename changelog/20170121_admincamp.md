
### Switchs N3K-3064PQ-10GE

- olb, capslock: réception les switch et de 30 SFP cuivre (GLC-T)
- olb, capslock: test du 100Mbps sur les SFP GLC-T (nous en avons besoin pour
  certaines cartes IPMI). Ça ne marche pas pour l'instant. Pistes : autre
  firmware, autre SFP.

### Collecte xDSL Liazo

- youpi: génération de la clé pour signer les commandes liazo: /etc/ssl/private/commandes-liazo.{key,pub}
- youpi: codage commande DSL liazo signée en ECDSA

### Migration de blog.fdn.fr

- mat: blog.fdn.fr
  - migré sur chewie
  - dépot https://git.fdn.fr/communication/blog avec dans la branche master la version 2.4.2 qui est en prod, dans la branch update-2.8.2 la version sur blog-dev

### Gitlab sur sa propre machine

- mat, capslock: git.fdn.fr
  - installé la même version que celle en prod sur kamino.fdn.fr, installation d'une deuxième vm en cours pour tester les mises à jour du gitlab.deb
  - chiffrement de kamino, vm pour le gitlab en cours d'installation/migration

### wiki adminsys

- olb: jardinage wiki

### Let's Encrypt

- vg: Let's encrypt sur les sites web openbar (public et devel)

### Monitoring

- belette: remise en route de isengard (monitoring), conf réseau et limitation
  des log des tests openvpn qui généraient trop d'io

### Mise en place de rôles pour les accès aux machines

- olb : il s'agit de définir des rôles dans puppet et d'associer ces rôles aux
  utilisateurs. Un rôle regroupe un ensemble d'accès (plutôt que de définir les
  choses accès par accès).

### hébergement du site vpn openbar

- vg : mise en place d'un virtualenv python pour le site vpn openbar sur chewie .

