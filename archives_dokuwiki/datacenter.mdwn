# Datacenters

FDN dispose de deux points de présence, sur Paris :
  * Au telehouse2 (th2), datacenter historique
  * À Paris Bourse.

## Principes généraux
On réfléchit avant d'intervenir en baie, on documente sur un support durable (wiki sur [[adminsys:interventions-baies]], plus mail si possible).

## TH2
### Le topo
Au th2, la baie qui nous intéresse est la baie 11A4. Elle appartient à l'asso amie Gitoyen, qui nous héberge (moyennant finances :p).
On peut y intervenir en autonomie pour des interventions d'urgence, mais l'idée est de réfléchir aux interventions avec Gitoyen.
Il faut donc essayer de les prévenir de nos velléités d'intervention le plus en amont possible, et voir s'ils peuvent venir avec nous.
Pour mémoire, la bonne adresse est ''equipage@gitoyen.net'' et il est plutôt chouette de mettre le bureau (''buro@fdn.fr'') en copie.

### Accès
Telehouse2 est situé au 137, boulevard Voltaire, Paris 11ème.
C'est accessible sur la ligne 9 de métro (station Charonne), et sur la ligne 56 de bus (arrêt Gymnase Jappy).

Pour rentrer, il faut d'abord présenter sa carte d'identité pour obtenir un badge et se faire prendre en photo
(premier poste de contrôle), puis présenter son badge pour vérifier que l'on a accès aux équipements.

Il faut donc être autorisé à accéder aux équipements. On a deux moyens :
  * être sur la liste des personnes ayant un accès permanent
  * disposer d'un accès temporaire
Sachant que les personnes qui sont dans le premier cas peuvent distribuer les accès temporaires.

Au 1er juillet 2015, les personnes ayant un accès permanent sont :
  * Mathieu Arnold (mat)
  * Benjamin Bayart (bayartb)
  * Arnaud Luquin (birdy)
  * Dominique Rousseau (domi)
  * Fabien Sirjean
On peut aussi, en cas d'urgence, demander directement aux amis de Gitoyen. Mais c'est pas pire de commencer par ceux-là.

Lorsque l'on est au helpdesk de th2, et qu'on fait vérifier son badge, il faut aussi récupérer la clé de la baie 
(et non pas demander à la faire ouvrir, on est un cas très particulier chez eux). On monte alors au premier étage,
on passe la porte à badge, on part sur la droite jusqu'au fond ou presque, puis à gauche jusqu'au fond. La baie est alors
à droite, tout au bout de la rangée (c'est quasiment la plus vieille baie du datacenter, on est dans une zone ancienne).

### Les équipements
Au 21 juin 2015, nous avons 5U dans la 11A4 : 
  * Partie baute :
    * LNS11 (va bouger en bas)
  * Partie basse :  
    * Le switch HP procurve
    * Vador
    * LNS22
    * LNS01

À terme, on devrait avoir l'agencement suivant, en partie basse : 
  * Switch HP procurve
  * LNS11
  * LNS22

### Trucs utiles
#### Accès réseau pour intervention
Il y a un câble ethernet en bas de la baie, et une multiprise. On peut se brancher dessus et utiliser la config réseau suivante :
    IP : 80.67.168.30 /27
    GW : 80.67.168.1
  
## Bourse
### Le topo
À paris bourse, FDN loue une demi-baie, en propre. C'est la baie Z1A11, partie basse.

Les personnes y ayant accès sont les membres du bureau restreint, et les membres du noyau adminsys.

### Accès
Le datacenter est situé au 35 rue des Jeûneurs, Paris 2. C'est un immeuble assez classique.
Il y a un digicode (cf. Password Store) pour rentrer dans l'immeuble, puis il faut monter au FIXME étage.

Deux cas de figure :
  * En heures de bureau (semaine, ~8h-18h), il suffit de sonner à la porte, on vient vous ouvrir
  * En dehors, il faut demander l'ouverture à Liazo (l'entreprise qui exploite le DC) :
    * prévenir par mail le plus à l'avance possible de l'intervention
    * téléphoner ou envoyer un sms sur le numéro d'astreinte (frémo, en général) pour demander l'ouverture de la porte par SSH.

Une fois rentré dans le DC, il y a un accès aux sales par contrôle biométrique. Il faut donc avoir ses circuits veineux
enregistrés dans leur système, à l'avance (y aller une première fois, en gros). C'est la salle de gauche, notre baie est 
située au fond à droite, dans le couloir froid. Y'a des stickers pour aider à se repérer :p

La baie s'ouvre avec un code, qui est stocké dans le Password Store.

### Les équipements
Au 21 juin 2015, on a une baie organisée de la manière suivante :
  * L'adduction électrique est en bas, en dual feed;
  * Les patchs réseau (on ne tire rien nous même) sont en haut, sur un bandeau fibre;
  * On câble l'électricité d'un coté, le réseau de l'autre;
  * On repère tous les câbles, des deux cotés.

Les équipements présents sont les suivants :
  * Le switch cisco 3560
  * Les deux droïdes r4p14 et c3px
  * La machine des RMLL
  * Les deux droïdes r2d2 et c3po

### Trucs utiles
#### Accès réseau pour intervention
Il y a un câble ethernet en bas de la baie, et une multiprise. On peut se brancher dessus et utiliser la config réseau suivante :
    IP : 80.67.168.30 /27
    GW : 80.67.168.1
