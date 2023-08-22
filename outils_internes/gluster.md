:warning: cette page n'est plus d'actualité

gluster est une solution de stockage distribué (en concurrence avec CEPH)
CEPH a besoin d'un multiple de trois nœuds pour fonctionner donc nous sommes parti sur gluster qui autorise une configuration plus risquée à 2 nœuds.

La configuration chez FDN est la suivante:
 - 2 nœuds avec 4 disques SSDs chacuns
 - luks sur chaque SSD indépendament, avec un xfs par dessus
 - gluster en mode redondance 2 (les fichiers sont copiés sur chaque nœud) avec 24 briques: 2 nœuds fois 4*(4-1) briques pour avoir quelque chose de facilement rééquilibrable en cas de panne d'un disque.

# configuration / creation d'un volume gluster

FDN a pas mal d'options qui ne sont pas par défaut: le SSL et des options orientées "virtu"

## configuration TLS

/!\ TLS sous gluster est largement sous-utilisé, il y a des problèmes en TLS qu'il n'y aurait pas sans. Une version au moins 7.3 de gluster est conseillée pour utiliser sérieusement TLS

Il y a plusieurs façons de faire la conf TLS, nous utilisons un CA autogénéré:
```shell
cd /etc/ssl
# à faire une fois, glusterfs.ca et dhparam.pem sont à copier sur tous les nœuds
openssl genrsa 4096 > glusterfs.ca.key
openssl req -sha512 -new -x509 -nodes -days 3 -key glusterfs.ca.key > glusterfs.ca
openssl dhparam -out /etc/ssl/dhparam.pem 2048
# à faire pour chaque nœuds
openssl genrsa 4096 > glusterfs.key
openssl req -new -key glusterfs.key -subj "/CN=$(hostname --fqdn)" -out glusterfs.csr
openssl x509 -req -in glusterfs.csr -days 3 -CA glusterfs.ca -CAkey glusterfs.ca.key -set_serial 01 -out glusterfs.pem
touch /var/lib/glusterd/secure-access
systemctl restart glusterd
```

# ajouter les noms des deux -repli dans les /etc/hosts de chaque host

## config initiale / creation du volume (ne le faire que sur un host)

```shell
# HOSTNAME = nœud 1, interface data (-repli)
# OTHER = nœud 2, interface data
gluster peer probe $OTHER
# lister /mnt/dataX/dataX-Y pour les nœuds machines.
# alterner entre chaque machine est important pour que la redondance
# soit bien placée
for i in {0..3}; do for j in {0..2}; do for machine in $HOSTNAME $OTHER; do
  echo "$machine:/mnt/data$i/data$i-$j"
done; done; done |
  xargs bash -c 'gluster volume create data replica 2 transport tcp "$@" force' --
```

## settings du volume

Il existe un "group" virt; voici les settings placés pour archivage détaillé
```shell
# partie TLS -- /!\ hostname doit matcher le certif (donc les vrais hostnames)
gluster volume set data auth.ssl-allow "host1.fdn.fr,host2.fdn.fr"
gluster volume set data client.ssl on
gluster volume set data server.ssl on
gluster volume set data ssl.cipher-list 'HIGH:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1:TLSv1.2:!3DES:!RC4:!aNULL:!ADH'
# partie virt
gluster volume set data performance.quick-read off
gluster volume set data performance.read-ahead off
gluster volume set data performance.io-cache off
gluster volume set data performance.low-prio-threads 32
gluster volume set data network.remote-dio disable
gluster volume set data performance.strict-o-direct on
gluster volume set data cluster.eager-lock enable
gluster volume set data cluster.quorum-type auto
gluster volume set data cluster.server-quorum-type server
gluster volume set data cluster.data-self-heal-algorithm full
gluster volume set data cluster.locking-scheme granular
gluster volume set data cluster.shd-max-threads 8
gluster volume set data cluster.shd-wait-qlength 10000
gluster volume set data features.shard on
gluster volume set data user.cifs off
gluster volume set data cluster.choose-local off
gluster volume set data client.event-threads 4
gluster volume set data server.event-threads 4
gluster volume set data performance.client-io-threads on
# partie en plus, qui en fait viennent contredire le group virt...
# pour permettre au gluster de marcher avec seulement 1 nœud
gluster volume set data cluster.quorum-type none
gluster volume set data cluster.choose-local true
gluster volume set data cluster.server-quorum-type none
# pour détecter plus rapidement quand un nœud tombe et
# ne pas passer les fs des VMs read-only
gluster volume set data network.ping-timeout 11
# Aucune idée de pourquoi mais c'est comme ça sur le volume...
gluster volume set data locking-scheme full
```

démarrer le volume après: gluster volume start data

# Maintenance
## Vérifier l'état de synchro

Une commande: gluster volume heal data info
Si tout va bien elle doit lister 0 fichiers pour toutes les briques; s'il y a des fichiers listés il faut creuser pourquoi.

## Architecture en trois mots

Il y a plusieurs entitées :
 - glusterd, le "maitre" gluster qui va gérer les briques, aiguiller les demandes de montage, piloter les heals, etc etc ;
 - glusterfsd, un process par brique ;
 - glusterfs, un process par point de montage client (fuse) et un pour le heal daemon
 - qemu peut aussi être un client directement (fichier avec un chemin gluster://), à faire attention potentiellement.

Il faut savoir que les briques sont "bêtes", toute l'intelligence (réplication, quel fichier choisir en cas de désynchro, etc etc) est dans les clients.
Le "heal info" par exemple est donc un client qui va simplement comparer le contenu des deux serveurs : ça peut être relativement long.

## Mises à jour

Les mises à jour peuvent se faire sans couper les VMs, avec une grosse condition: bien vérifier et attendre que le volume soit synchro avant chaque mise à jour, et ne surtout pas faire plusieurs serveurs en même temps.
En pratique sous debian l'upgrade ne coupe pas les services briques donc il faut bien redémarrer manuellement les processes gluster après une upgrade.

Un exemple détaillé est lisible dans la page de [mise à jour proxmox](./proxmox.md#mises-à-jour)

## Remplacement d'une brique (en attente de remplacement d'un disque cassé par exemple)

Il y a en théorie plusieurs manières de remplacer une brick ; la manière recommandée serait de add-brick puis remove-brick... Mais si la brick ne marche déja pas on peut replace-brick.
/!\ replace-brick jette complètement les données de l'ancienne brick et ne fait aucune vérification sur la disponibilité des données (e.g. heals en cours), à manipuler avec précautions /!\

```shell
# donc si /mnt/data1 est pourrit sur $HOSTNAME par exemple, il faut remplacer les 3 bricks qui sont dedans:
gluster volume data $HOSTNAME:/mnt/data1/data1-0 $HOSTNAME:/mnt/data0/data1-0 commit force
gluster volume data $HOSTNAME:/mnt/data1/data1-1 $HOSTNAME:/mnt/data2/data1-1 commit force
gluster volume data $HOSTNAME:/mnt/data1/data1-2 $HOSTNAME:/mnt/data3/data1-2 commit force
# puis bien suivre l'évolution avec heal info / iftop
gluster volume heal data info
# à la fin, tout doit être à 0.
```

L'autre méthode (à priori conseillée, mais bien plus lourde), imposer de remplacer la paire de briques à chaque fois et ressemblerait à ça:
```shell
gluster volume add-brick $HOSTNAME:/mnt/data0/data1-0 $OTHER:/mnt/data1/tmp-data1-0 $HOSTNAME:/mnt/data2/data1-1 $OTHER:/mnt/data1/tmp-data1-1 $HOSTNAME:/mnt/data3/data1-2 $OTHER:/mnt/data1/tmp-data1-2
gluster volume remove-brick data $HOSTNAME:/mnt/data1/data1-0 $OTHER:/mnt/data1/data1-0 $HOSTNAME:/mnt/data1/data1-1 $OTHER:/mnt/data1/data1-1 $HOSTNAME:/mnt/data1/data1-2 $OTHER:/mnt/data1/data1-2 start
# ça pose une question sur un setting sans regarder la valeur du setting, on est bon à priori
gluster volume remove-brick data $HOSTNAME:/mnt/data1/data1-0 $OTHER:/mnt/data1/data1-0 $HOSTNAME:/mnt/data1/data1-1 $OTHER:/mnt/data1/data1-1 $HOSTNAME:/mnt/data1/data1-2 $OTHER:/mnt/data1/data1-2 status
# jusqu'à ce que ça dise compelted
gluster volume remove-brick data $HOSTNAME:/mnt/data1/data1-0 $OTHER:/mnt/data1/data1-0 $HOSTNAME:/mnt/data1/data1-1 $OTHER:/mnt/data1/data1-1 $HOSTNAME:/mnt/data1/data1-2 $OTHER:/mnt/data1/data1-2 commit
gluster volume status
```

## Changement de topo gluster (rajout d'un nœud, briques etc)

En théorie on peut tout faire à chaud ; en pratique c'est plutôt lent et touchy (aucun check de la part de gluster pour te dire que tu es en train de corrompre tout ton système), donc on préfère faire des évolutions en deux temps:
 - créer un nouveau volume
 - migrer toutes les VMs dessus
 - supprimer l'ancien volume.

La seule chose à faire attention est de bien reconfigurer le volume. Ça peut aussi permettre une phase de tests avant de tout basculer.

Pour migrer les disques, il y a un script `migrate-disk.sh` dans /mnt/pve/gluster/mkosi qui prend deux options:
DISK_TARGET: le nom du volume destination (e.g. "gluster" ; c'est le nom du volume dans l'interface pve)
VM_TARGET: une regexp (awk) pour filtrer sur les VMs qui tournent actuellement sur la machine.

Il faut donc le lancer une fois par hyperviseur ; le script n'a jamais été testé sir des VMs sont éteintes.

# Troubleshooting

À prendre dans l'ordre si "ça marche pas", ou au cas par cas si un problème est identifié.

## briques crashées / éteintes

`gluster volume status` doit lister tout les composants Online à Y, avec un PID et un port pour les briques.
Si ce n'est pas le cas, `gluster volume start x force` règlera probablement le problème.

## peer disconnected

À vérifier en cas de problème: `gluster peer status` doit dire "Peer in Cluster (Connected)" pour tous les peers.

Si ça ne marche pas, prendre exactement le hostname du bloc qui n'est pas connected et tenter de se connecter sur le port 24007:
```shell
# nc -v $OTHER 24007
Ncat: Version 7.70 ( https://nmap.org/ncat )
Ncat: Connected to x.y.z.t:24007.
^C
```

Si ça marche mais que ça dit disconnected, je ne sais pas !
Les logs pour la partie 'peer' doivent être dans glusterd.log

## Logs

Il y a plein de logs gluster dans /var/log/glusterfs ; en gros un par process.

 - glusterd.log pour le master
 - glustershd.log pour le heal daemon
 - bricks/<path-to-brick>.log pour chaque brique
 - <path-to-mount>.log pour chaque montage

## split-brain

Avec un setup à deux nœuds, il existe un risque de split-brain.
Ça se produit sur un fichier quand, en partant d'un fichier synchro, on a un premier write uniquement sur un serveur, suivi d'un deuxième write uniquement sur l'autre serveur plus tard sans avoir eu le temps de recopier les modifs du premier serveur (par exemple en cas d'upgrade des deux nœuds de manière rapprochées, un serveur redémarre et manque des IOs ; les deux serveurs reviennent ; l'autre serveur redémarre avant que le info heal ne soit clean)
Dans ce cas, tout aura l'air de marcher jusqu'au moment où le client se reconnectera aux deux serveurs et le client refusera de lire ou d'écrire plus sur ce fichier.

En pratique, sur une sandbox:
```
root@sandbox1:~# cat /mnt/splitme 
cat: /mnt/splitme: Input/output error
cat: /mnt/splitme: Input/output error
root@sandbox1:~# gluster volume heal data info
...
Brick sandbox1:/var/gluster/brick2
/splitme - Is in split-brain
Status: Connected
Number of entries: 1

Brick sandbox2:/var/gluster/brick2
/splitme - Is in split-brain
Status: Connected
Number of entries: 1
...
```

Une fois arrivé là, pas de solution miracle. On peut:
 - examiner le contenu directement sur la brique, ici le fichier sera /var/gluster/brick2, et décider de laquelle garder:
`gluster volume heal data split-brain source-brick <hostname:brickname> [path]`
 - ne pas réfléchir et dire de prendre la copie la plus récente: si le fichier a longtemps marché avec un seul serveur par exemple et que ça a cassé au retour du 2nd serveur, il y a de bonnes chances que ça fonctionne bien comme ça. (latest-mtime)
 - On peut aussi dire l'inverse: cette copie risque d'avoir un trou, alors que l'autre copie devrait être entièrement cohérente... Il n'y a pas de earliest-mtime ;D

## shards

Normalement, gluster reproduit l'arborescence du volume dans la brique, par exemple <mnt>/truc va être stocké dans <unebrique>/truc.
Si un fichier est trop gros et est shardé, seul les 64 premiers MB sont à cet endroit, tout le reste sera physiquement dans la brique gluster sous /.shard

Par exemple:
```shell
ls -l /var/gluster/brick2/.shard
# -rw-r--r-- 2 root root 67108864 Jun 16 09:09 de07375e-d668-42a8-b212-ff4e387bd9ef.19
# -rw-r--r-- 2 root root 67108864 Jun 16 09:09 de07375e-d668-42a8-b212-ff4e387bd9ef.24
```

On peut avoir besoin de retrouver de quel fichier il s'agit.

Le chemin avant le point représente le 'gfid' du fichier qui est shardé, donc il suffit de retrouver ce fameux fichier, qui doit être sur une des briques :
```shell
ls -li /var/gluster/*/.glusterfs/de/07/de07375e-d668-42a8-b212-ff4e387bd9ef
# 131500 -rw-r--r-- 2 root root 4194304 Jun 16 09:09 /var/gluster/brick0/.glusterfs/de/07/de07375e-d668-42a8-b212-ff4e387bd9ef
find /var/gluster/brick0 -inum 131500
# /var/gluster/brick0/bigfile
# /var/gluster/brick0/.glusterfs/de/07/de07375e-d668-42a8-b212-ff4e387bd9ef
```

On a donc affaire à /bigfile dans le point de montage.
À noter :
 - la brick n'est pas forcément la même
 - le de/07 vient des quatre premiers chiffres du gfid
 - pas mieux que find sur l'inode number: ça peut être long...

Pour l'opération inverse, c'est bien plus simple ; il y a deux manières d'obtenir le gfid d'un fichier:
```shell
getfattr -n 'glusterfs.gfid.string' /mnt/bigfile 
# glusterfs.gfid.string="de07375e-d668-42a8-b212-ff4e387bd9ef"
getfattr -d -m 'trusted.*' -e hex /var/gluster/*/bigfile
# trusted.gfid=0xde07375ed66842a8b212ff4e387bd9ef
```

