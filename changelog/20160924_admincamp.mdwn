
### Vador n'est plus MX2 de qui que ce soit

### Migration de wiki.fdn.fr sur kylo

- Le wiki était précédemment sur vador.
- Mise en place de [[outils/letsencrypt]].

### Rangement de la baie à Téléhouse2 en 11A4

- benner une machine inutilisée
- éteindre et benner vador
- déplacer un lns à coté de l'autre et du switch

### Remplacement du switch procurve en 11A4

- Le procurve à lacher au moment où nous enlevions vador de la baie.
- Nous avons mis un cisco catalyst 2970 en catastrophe dans la nuit du samedi au dimanche (merci à belette pour ce switch).

### Mise à jour de la pki de puppet

Voir la doc de puppet : c'est un peu pénible à faire. Il faut bien respecter l'ordre des choses.

### Mise à jour de acme_tiny via puppet

- Le lien vers le Service Agreement de letsencrypt a changé

### Migration flyspray sur kylo

### Migration de ns1.fdn.fr sur [[infra/machines/resolver1]]

- Avec les règles iptables de rate limit.

### Ménage DNS

- Suppression des références à Vador (jabba/guinness) dans les zones FDN / adhérents
- Pas mal de ménage sur la zone DNS fdn.fr/org

### Arrêt freeradius sur solo

- Ce freeradius n'était pas utilisé.

### Mise à jour jessie [[infra/machines/resolver0]], [[infra/machines/resolver1]], et [[infra/machines/kylo]]

### Tunnels chiffrés : ajout d'un deuxième cpu aux vm vpn1 et vpn2

### Amélioration de Cachet et Nagios

- Pour le monitoring à distance, les bases sont posées
- Mise à jour de la doc [[outils/supervision/remote_monitoring]]
- Mise à jour de la Todo list pour le prochain admincamp

