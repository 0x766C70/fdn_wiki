
Date : 6, 7 et 8 mars    
Objet : avoir une infra redondante entre lns22 et Paris Bourse. Mettre ne service un nouveau droïde dans chaque datacenter, déplacer lns22 à Paris Bourse.

## Mercerdi 6 mars soir

Synchronisation des montres

## Jeudi 7 mars matin - Extinction de lns22

Nous nous apercevons que les cluster l2tpns ne fonctionnement pas
correctement. Les deux l2ptns pour chaque porte sont tous les deux en master.
Pour chaque porte, seul l'un des deux porte les sessions. Nous redémarrons les
deux l2tpns qui ne portent aucune session. Après redémerrage, il passent en
slave et les sessions sont bien visibles dessus. Par ailleurs, lorsque nous
éteignons les l2tpns sur lns22, nous nous apercevons que la collecte Nerim ne
fonctionne pas correctement. Après investigation, nous nous rendons compte que
les ip des lns ne sont plus annoncés à Nerim du fait du changement des noms
d'interface tun* depuis l'apparition de la porte de collecte Ielo-Liazo (le
problème a été corrigé). Nous nous sommes également aperçu que la collecte de
franciliens n'avait pas été mise en place de manière redondée sur les deux LNS.

## Jeudi 7 mars après midi - Installation des deux nouveaux droïdes

Nous avons installé Debian sur les deux nouveaux droides et configuré l'ipmi et le réseau.

- /boot en raid1 sur les quatre disques
- / en raid raid5 sur les quatre disques

Nous avons fait des teste d'extension du raid5 de trois disque à quatre disques :
    
    mdadm --manage /dev/md1 --add /dev/sdc5
    mdadm --grow /dev/md1 -n 4

Nous avons également testé le reboot des machines avec un disque en moins.

TODO: photos

## Vendredi 8 mars matin - Intervention à Téléhouse 2.

Désinstallation de lns22 et mise en baie de tc14 à la place.

TODO: photos

RAS tout s'est bien passé.

## Vendredi 8 mars après midi - Intervention à Paris Bourse. 

- Mise en baie de lns22 et r5d4.
- Configuration d'un lien qinq
- pour une raison inconue, le clustering l2tpns entre les deux lns ne fonctionne plus.

TODO : photos.


# Actions à prévoir :

- mettre en place une VIP sur l'interco de franciliens ou mettre en place des sessions BGP.
  => une VIP a été mise en place samedi
- installation de proxmox sur r2d2 et c3po
- réparer le clustering l2tpns 
  => réparé également samedi
- questionner les VLAN sur le port 48 pour en mettre le moins possible : notamment le 14 et le 3.


