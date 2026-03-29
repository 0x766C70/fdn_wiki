Date : 5 octobre 2019

FDN avait deux portes de collecte xDSL/ielo-liazo qui étaient toutes deux
livrées sur notre switch au centre de données Téléhouse2. Hier, sebian et olb
avons déplacé la seconde porte de collecte sur notre second switch dans le
centre de données Paris-Bourse. Nous avons donc une porte de collecte de
chaque coté.

Suite à cette opération, et l'opération faite avec Belette et olb en mars
dernier (déplacement d'un lns/passerelle à Paris Bourse et mise en service des
deux nouveaux hyperviseurs), il s'en suit que FDN est maintenant redondé sur
deux sites pour le transit via Gitoyen, et en grande partie pour le xDSL
(seulement pour ielo-liazo). Pour le reste, disons que FDN est redondable : il
faut encore adapter les services au fait que nous ayons deux sites (dns,
tunnels chiffrés, etc).

Une des conséquences très concrètes, c'est par exemple que l'intervention
prochaine de ielo-liazo sur ses propres équipements à téléhouse 2 n'aura aucune
conséquence visible pour les usagers de FDN ce qui avant le déplacement de la
deuxième porte à Paris Bourse n'aurait pas été le cas.


En détail :

- nous avons tué l'instance l2tpns ielo-liazo sur lns22 pour faire
  basculer le cluster sur lns11 et nous avons éteint les sessions bgp
  correspondantes.

- nous avons patché à Paris-Bourse une nouvelle interconnexion avec
  ielo-liazo, directement sur notre switch (port 36, le même que sur
  l'autre switch), et déconfiguré les vlan 530-532 sur le port 36 à TH2
  et configuré ces mêmes vlan sur le port 36 coté PBO.

- sebian a déplacer la porte de collecte coté ielo-liazo à PBO

- nous avons rallumé les sessions bgp et rallumé l2tpns-liazo sur lns22.

- nous avons tuer l2ptns-liazo sur lns11 pour le refaire basculer la
  collecte sur lns22 (et constaté que cela marchait bien).

Cela a été transparent pour les usagers de FDN.

Nous avons constaté au passage que FDN ne maitrisait pas très bien par
ou passait les flux xDSL/ielo-liazo entre TH2 et PBO (le routage est
asymétrique). Si cela intéresse, c'est une manière utile de regarder
cela de plus prêt (freeradius & bird).
