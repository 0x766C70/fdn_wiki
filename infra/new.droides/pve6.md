Réinstall en pxe6 suite aux problèmes de shutdown qui ne passent pas bien / ipv6 pas up au boot

* l'install sur DVD fut possible après copie du dvd sur une partition lvm + modification de l'initrd et ajout kernel/initrd du DVD au grub de la machine, mais l'installer ne sait pas faire du partitionnement custom...
* -> installation de proxmox dans une VM sur tc14, et extraction du continue de la VM dans une nouvelle partition vg1/pveroot
* bidouillages pour faire rentrer le /boot de pveroot dans le /boot raid1, et support temporaire des deux systèmes côte à côte en cas de pépin
* reboot sur la nouveau système sans souci, copie sur r5d4
* copie de vg1/pveroot sur vg1/pveroot-prepuppet sur tc14
* passage puppet sur les deux nœuds
* conf réseau sur les deux nœuds via l'interface web proxmox
* ... un peu de bidouillage via le fichier network pour la mtu, à mettre sur l'interface physique ET l'interface ovs (mais pas nécessairement le bridge, qui hérite de la mtu de l'interface physique...) https://pve.proxmox.com/wiki/Open_vSwitch#Note_on_MTU
* création du cluster / join du cluster sur les vlan 802 et 800 (vlan800 qui est ?!)
* recréation des certificats acme pour tc14 qui l'a perdu dans la bataille
* copie de vg1/pveroot sur vg1/pveroot-preceph sur tc14 et r5d4

* ceph c'est pourrit (il faut des disques vides, pas par dessus du raid)
* se rendre compte que les backups faits à grand coups de dd sont corrompus (au niveau ext4, je ne vois pas trop comment ?!) et que j'aurais du faire des tar... -> bon pour réinstaller quand on voudra repartir au propre...
* pour le réseau: il faut aussi mettre la mtu sur l'interface du bridge, pas que les deux autres, pour que l'interface graphique accepte d'editer à nouveau le fichier + renomer ipmi en admin et vlan800 en intra
* setup gluster, c.f. [stockage](stockage)
* jouer avec cloud-init: echec
 -> la VM cloud debian ne supporte pas le réseau en static https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=931173
  -> la conf cloud-init built-in de proxmo est -super- limitée, uniquement les 5 champs qu'ils ont prévus et surtout rien d'autre (alors que c'est un langage de script qui permettrait n'importe quoi...)
  * jouer avec mkosi (un wrapper au dessus de deboostrap et autres qui permet de faire un peu plus)
   -> commence à être pas trop mal....
   * jouer avec comment créer une VM et ajouter tout les périphériques en cli...
    -> en cours...


    TODO
     * remettre les depots proxmox (deleted by puppet)
     