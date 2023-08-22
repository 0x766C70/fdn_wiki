:warning: cette page n'est plus d'actualité

FDN maintient un cluster de machines virtuelles pour ses propres besoin. Il est
question de faire un cluster de vm pour ses membres mais c'est pas encore le
cas.

# Qu'est-ce qui est installé sur le cluster ?

Ça consiste en quelques démons et un paquet de commandes *gnt-quelquechose* qui
ont toutes une page de manuel et qui prennent toutes un argument *help*.

En plus de ça, le paquet *ganeti-instance-debootstrap* contient un modèle de VM
construit avec *debootstrap* (étonnant, non ?) ; sa config (en grande partie
piquée à Tetaneutral) est dans ///etc/ganeti/instance-debootstrap// sur toutes
les machines du cluster.

# Et ça marche ?

Pour le savoir, [[ganeti/tests]]. Jettes-y un oeil, tu y trouveras aussi des
situations un peu tricky et la façon de t'en tirer.

# Comment je me connecte sur le cluster ?

Une des machines du cluster est désignée comme maître, toutes les commandes
d'admin doivent être lancées depuis cette machine. Pour la trouver, deux façons
de faire :

  * Solution simple : se connecter directement en SSH sur l'IP d'admin du
    cluster. Ganeti fait ce qu'il faut pour répliquer les clés SSH sur toutes
    les machines du cluster, histoire que SSH ne hurle pas quand le maître change.

        ssh droides.fdn.fr

  * Solution tordue : se connecter sur une des machines, n'importe laquelle,
    puis lui demander qui est le patron :

        /usr/sbin/gnt-cluster getmaster

# Opérations courantes sur les VM

Ça se fait connecté sur le maître.

Voir l'état des VM :

    gnt-instance list

Avec plus d'infos, là le secondary node :

    gnt-instance list -o +snodes

Se connecter sur la console d'une VM :

    gnt-instance console la.vm

Pour sortir de la console :

    ctrl+]

Démarrer une VM :

    gnt-instance start la.vm

Démarrer une VM et avoir la console dès le démarrage :

    gnt-instance start la.vm && gnt-instance console la.vm
  
Arrêter une VM :

    gnt-instance shutdown la.vm
  
**Attention**, il ne suffit pas de lancer *poweroff* dans la VM ; si on fait ça, son noyau s'arrête bien mais Ganeti la voit toujours active.

Migrer une VM vers son socle secondaire (la 2ème patte de son DRBD) :

    gnt-instance migrate la.vm

**Attention**, ça ne marche que si le primaire est up. Si le socle primaire est tombé :

    gnt-instance failover --ignore-consistency la.vm

# Comment j'installe une nouvelle VM ?

Une fois connecté sur le maître, ça se fait avec la commande *gnt-instance
add*. Elle demande un certain nombre de paramètres ; la ligne de commande utile
la plus simple ressemble à ça :

    gnt-instance add \
        -m 512m \
        -t drbd -s 2G \
        --net 0:link=br3 --net 1:link=br800 \
        -o debootstrap+stretch \
        paploo.fdn.fr

Exemple avec plusieurs disques :

    gnt-instance add \ 
        --disk 0:size=5G \
        --disk 1:size=30G \
        --disk 2:size=30G \
        -B memory=2G,vcpus=2 \
        -t drbd \
        -o debootstrap+stretch \
        rey.fdn.fr 

Il faut que le nom de la machine soit déjà dans le DNS avant de lancer la commande.

Ça installe une VM 64 bit sous Debian Stretch, le tout sur un «disque» DRBD de 2
Go avec 510Mo de ram. On peut ajouter d'autres options ; *man gnt-instance* pour les détails,
sachant qu'il vaut mieux ne pas toucher à l'option *-H* (normalement le cluster
est déjà configuré comme il faut). Pour la liste des OS disponibles, *gnt-os
list*.

Attention, au 2 mai 2013, les deux variantes de Sid (*debootstrap+sid32* et
*debootstrap+sid64*) ne s'installent pas à cause d'histoires de clés GPG
incorrectes et de dépôts apt absents. Si jamais quelqu'un trouve ça grave on
essaiera de corriger.

## Note au 2019-04-10

Il faut actuellement rajouter `-n r4p17.fdn.fr:c3px.fdn.fr` à la commande
à cause d'un bug sur ganeti. N'est pas dans les exemple car c'est voué
à disparaître et non recommendé dès lors que ganeti sera mis à jour.

## Et cette nouvelle VM, elle ressemble à quoi ?

Un peu en vrac :

  * Par défaut, une CPU virtuelle et 512 Mo de RAM. (pour changer ça, ajouter -B memory=1G, par exemple, à la création.)
  * Un disque virtuel avec une seule partition et un système de fichiers ext3 dessus. Pas de swap, donc.
  * Elle boote avec [[http://www.syslinux.org/wiki/index.php/EXTLINUX|extlinux]], pas Grub. Ça a le bon goût de fonctionner. Ceci dit, une fois la VM installée, on peut tout à fait installer Grub dedans si on veut ; c'est juste à l'installation que ça fait une différence.
  * Une console série (pour *gnt-instance console*).
  * Une interface réseau virtuelle, accrochée par défaut au pont réseau *br3* (le VLAN 3, celui des serveurs de FDN).
  * SSH n'accepte pas les connexions par mot de passe.
  * *root* a un mot de passe vide, ce qui veut dire qu'on peut se connecter à la VM directement par *gnt-instance console*. Il a aussi la clé publique du *root* du cluster, histoire qu'on puisse se connecter aux VM depuis les socles. Ça sert à se connecter sur une VM pour la remettre en face des trous en cas de pépin. J'ai piqué l'idée à Tetaneutral, chez eux, ça marche. **TODO** blinder un peu la config PAM pour interdire l'usage de *su*.

  * Pour les VM FDN, utiliser [[adminsys:puppet|Puppet]] pour faire configurer tout ce qui va bien pour les accès ssh etc.
  * Pour la supervision, utiliser [[adminsys:munin|Munin]] et nagios sur leia.
  * Penser à ajouter la VM à la liste des [[adminsys:serveurs:serveurs|serveurs]].

## Et si je veux autre chose qu'une Debian ?

*Ce bout de doc est très largement pompé [[http:*chiliproject.tetaneutral.net/projects/tetaneutral/wiki/Cluster_Ganeti|chez Tetaneutral]].//

Ganeti sait importer une image disque déjà installée (testé avec un NetBSD 6.0 installé dans une VM chez moi, il faut juste faire gaffe à configurer la VM pour qu'elle tourne sur notre cluster, essentiellement tout en VirtIO et une console série à 115200 bauds). On part d'une image disque *raw* ; si on a un autre format (*qcow2* dans mon cas) il faut d'abord la convertir.

    qemu-img convert paploo.qcow2 -O raw paploo.raw

Ensuite on crée un volume LVM de la bonne taille et on y copie l'image :

    size=$(qemu-img info paploo.raw | sed -n -e 's/^virtual size:[^(]*(\([[:digit:]]*\).*)/\1/gp')
    lvcreate -L ${size}b -n lv_migration_paploo vg1
    dd if=paploo.raw of=/dev/vg1/lv_migration_paploo

On importe la VM :

    gnt-instance add --no-start -t plain -n $(hostname) --disk 0:adopt=lv_migration_paploo \
    -o debootstrap+default paploo.fdn.fr

Ensuite on convertit le disque de la VM en DRBD :

    gnt-instance modify -t drbd -n c3po.fdn.fr paploo.fdn.fr

Dans la ligne précédente, on bosse sur *r2d2*, le *-n c3po.fdn.fr* désigne la 2ème machine du DRBD.

Voilà, c'est fait, on peut allumer la VM.

## Et si je veux installer ma VM à la main (pour la chiffrer par exemple) ?

On crée une VM de type debootstrap+default avec les modes --no-install et --no-start :

    gnt-instance add -s 90G -t drbd -B memory=1G --no-install --no-start -o debootstrap+default exegetes.eu.org
  
On lance la VM en lui passant une ISO comme support de démarrage :

    gnt-instance start -H cdrom_image_path=/root/isos/debian-8.2.0-amd64-netinst.iso,boot_order=cdrom,vnc_bind_address=127.0.0.1 exegetes.eu.org

Si l'iso voulue n'est pas disponible dans /root/isos/, vous pouvez la télécharger sur un des droides puis utiliser la commande suivante pour l'envoyer sur tous les autres droides :

    gnt-cluster copyfile /root/isos/mon.iso
  
Pour voir la liste des machines, leur port vnc (*aka* network port) ainsi que la machine sur laquelle elle est lancée (c'est sur celle-ci que le port vnc est ouvert) :

```bash
$ sudo gnt-instance list -o +network_port
```

On fait un tunnel SSH (depuis sa machine locale) vers le port VNC du socle ganeti sur lequel tourne la VM (vérifier avec gnt-instance list):

    elfabixx@arthur2:~$ ssh -L 11051:localhost:11051 r4p17.fdn.fr
  
On peut récupérer ce numéro de port avec netstat, ou bien en regardant dans :

    gnt-instance info exegetes.eu.org
  
Sur sa machine locale, on ouvre un client VNC (ici par exemple, vinagre) :

    elfabixx@arthur2:~$ vinagre localhost:11051

Et hop, on se retrouve sur le debian-installer, comme à la maison.

# Déplacer une VM entre plusieurs machines 

## Pour une machine (exemple avec chewie.fr des anciens droïdes aux nouveaux)

  * État initial : primaire: c3po / secondaire: r2d2
  * État final : primaire: r4p17 / secondaire: c3px


D'abord déplacer le secondaire :

    gnt-instance replace-disks --new-secondary r4p17.fdn.fr chewie.fdn.fr

Ensuite switcher le primaire :

  * soit à chaud :

        gnt-instance migrate chewie.fdn.fr 

  * soit à froid :

        gnt-instance failover chewie.fdn.fr 

Puis redéplacer le secondaire :

    gnt-instance replace-disks --new-secondary c3px.fdn.fr chewie.fdn.fr


=## Déplacer toutes les VM en secondaire d'un nœud vers un autre 

  * État initial : primaire: r2d2 / secondaire: c3po
  * État final : primaire: r2d2 / secondaire: c3px

    gnt-node evacuate --new-secondary=c3px.fdn.fr --secondary-only c3po.fdn.fr


# Migration d'une VM Xen existante

La migration se fait avec pas mal de downtime (le temps de copier les disques) et demande un peu d'espace sur le disque de la machine de destination (temporairement 2 fois le stockage). Une paire de liens :

http://blogs.glou.org/arnaud/2012/01/17/migrer-une-vm-de-xen-vers-kvm/

[[adminsys:ganeti:migrationdepuisxen|Mes (nono) notes]] sur la migration de vpn1 depuis Xen.

## Sur la VM, avant l'arrêt

D'abord on ajoute une ligne série dans ///etc/iniitab// :

   T0:23:respawn:/sbin/getty ttyS0 38400

Elle servira comme console pour KVM.

Ensuite, si la VM est sous Squeeze, on installe un noyau «standard» à la place du noyau Xen. Je l'installe depuis les backports, je ne sais pas si c'est nécessaire mais en tout cas comme ça ça marche. Si la VM est sous Wheezy, c'est a priori inutile (**TODO** : vérifier), le noyau générique doit intégrer le support Xen.

    cat > /etc/apt/sources.list.d/backports.list <<EOF
    deb http://mirrors.ircam.fr/pub/debian-backports/ squeeze-backports main
    EOF
    apt-get update
    apt-get install -t squeeze-backports linux-image-686
    apt-get purge linux-image-2.6.32-5-xen-686

Dans tous les cas, on installe Grub 2 (apt va éventuellement en profiter pour virer grub-legacy s'il est installé) :

    apt-get install grub grub-pc

On en profite pour éditer le fichier ///etc/default/grub// pour configurer la console série :

    GRUB_CMDLINE_LINUX_DEFAULT="console=ttyS0,38400n8"

## Création du disque virtuel sur les droides

Ça se passe sur la machine d'admin du cluster (ici *c3po*, *gnt-cluster getmaster* pour s'en assurer). Dans l'exemple je migre la machine *vpn1*, c'est bien sûr à adapter.

    lvcreate -L4G -n migration-vpn1 vg1
    fdisk /dev/vg1/migration-vpn1
    kpartx -av /dev/vg1/migration-vpn1
    mkswap /dev/mapper/vg1-migration--vpn1p2
    mkfs -j /dev/mapper/vg1-migration--vpn1p1
    mount /dev/mapper/vg1-migration--vpn1p1 /mnt

Explications : on crée un volume logique LVM (ici j'ai taillé large, l'original fait dans les 2 Go). On le partitionne (*kpartx* sert à indiquer au noyau que oui, il y a bien des partitions là-dedans et tu peux t'en servir), on y met des systèmes de fichiers ou du swap et on monte la racine de la future VM sous /*mnt* (dans le cas de plusieurs partitions, il faut toutes les monter).

## Arrêt et copie da la VM

Ça se passe sur le socle Xen (ici *palpa2*). Il faut être root et avoir le droit de se connecter en root sur *c3po* (agent SSH ou autre). On arrête la VM, on monte ses systèmes de fichiers et on copie le tout sur le socle Ganeti.

    xm shutdown vpn
    mkdir /mnt/vpn1-root
    mount /dev/xenvg/vpn-disk /mnt/vpn1-root/
    rsync -av /mnt/vpn1-root/ root@c3po:/mnt/

Une fois que c'est fait on peut démonter les disques virtuels. **Ne pas oublier** de virer le lien vers la config de la VM dans ///etc/xen/auto//, qu'elle ne redémarre pas au prochain reboot.

C'est fini côté Xen.

## Import de la VM côté Ganeti

D'abord éditer ///mnt/etc/fstab* pour y mettre les bonnes partitions (le disque virtuel s'appellera */dev/vda//). Ensuite on peut démonter notre future VM :

    umount /mnt
    kpartx -dv /dev/vg1/migration-vpn1

On peut ensuite importer la VM dans Ganeti. Si on n'est pas très sûr de soi, il peut être utile de garder une copie du volume ///dev/vg1/migration-vpn1// sous le coude ; il sera détruit pendant l'opération.

    gnt-instance add --no-start -t plain -n $(hostname) --disk 0:adopt=migration-vpn1 -o debootstrap+default vpn1.fdn.fr
    gnt-instance modify -t drbd -n r2d2.fdn.fr vpn1.fdn.fr
    gnt-instance modify --net 0:mac=ac:de:48:00:a9:2d vpn1.fdn.fr
    gnt-instance modify -H kernel_path=/boot/vmlinuz-3.2.0-4-amd64,initrd_path=/boot/initrd.img-3.2.0-4-amd64 vpn1.fdn.fr
    gnt-instance start vpn1.fdn.fr

(Oui, je sais, on peut condenser les trois appels à *gnt-instance modify*, mais ça fait une commande interminable et pas lisible).

## Configuration définitive du boot de la VM

### Sur la VM

Si tout va bien (ahem) on a une VM qui «marche à peu près» mais qui ne tourne pas sur le bon noyau (probablement *amd64* au lieu de *i686*) et qui, du coup, n'a pas les modules qui vont avec. En tout cas, elle a une console, des disques et du réseau, ça suffit pour la suite. On se connecte sur la VM (console ou SSH, comme on veut, les deux devraient marcher à ce stade) et on y installe un grub local.

    grub-install /dev/vda
    update-grub

Tant qu'on est là, on peut aussi virer la console Xen de ///etc/inittab*, c'est plus propre. La ligne ressemble à ça (l'important c'est le *hvc0// à la fin) :

    1:2345:respawn:/sbin/getty 38400 hvc0

### Sur le socle

Ensuite, sur *c3po*, on configure notre VM pour la faire booter sur son propre disque et pas sur le noyau de l'hôte.

    gnt-instance shutdown vpn1.fdn.fr
    gnt-instance modify -H kernel_path=,initrd_path= vpn1.fdn.fr
    gnt-instance start vpn1.fdn.fr

C'est prêt ! :-)

# Comment j'installe un nouveau socle ?

## Logiciels

On n'installe pas les logiciels à la main, pour ça on a une [[adminsys:puppet|classe Puppet]]. Dans le détail et vu par Puppet, un noeud du cluster ressemble à ça :

    node "c3po.fdn.fr" {
    include base
    include ntp
    include users::admins
    include ganeti
    class { 'ipmi::host':
      ipaddr         => '10.0.0.32',
      admin_password => 'le_mot_de_passe_admin',
    }
    }

Bien entendu la config IPMI est à adapter pour chaque machine.

À partir de là, on fait le reste «à la pogne».

## Nom d'hôte

Puppet doit positionner le hostname de la machine à son FQDN (ie /etc/hostname doit contenir *mabellemachine.fdn.fr* et pas juste *mabellemachine*). Pas besoin d'y toucher.

On s'assure aussi que l'IP locale est bien dans /etc/hosts, par exemple pour c3po :

    80.67.169.48    c3po.fdn.fr     c3po

## IPMI

Le port IPMI du socle doit être dans le VLAN 801, et on doit choisir une adresse IP dans 10.0.0.0/24 (p. ex. 10.0.0.31 pour *r2d2-ipmi*). L'essentiel de la config IPMI est géré par Puppet, il en reste juste quelques bouts pas finis.

Il faut s'assurer que la console série sur IPMI est activée dans le BIOS et trouver à quel port série elle correspond (sur *r2d2* et *c3po* c'est *ttyS2*). Pour configurer GRUB pour passer les bons paramètres au noyau, éditer la variable GRUB_CMDLINE_LINUX_DEFAULT dans ///etc/default/grub// :

    GRUB_CMDLINE_LINUX_DEFAULT="console=tty0 console=ttyS2,115200n8"

Ne pas oublier de régénérer la config de Grub :

    update-grub

Il n'y a que GRUB à configurer à la pogne, Puppet configure bien un *getty* sur le port série virtuel.

Une fois la machine rebootée, on doit pouvoir accéder à la console depuis *lns01* :

    ipmitool -I lanplus -H r2d2-ipmi -U ADMIN -a sol activate

On peut aussi faire tout plein de choses genre allumer ou éteindre la machine, va lire la doc d'ipmitool pour en savoir plus.

**TODO** finir de mettre tout ça dans Puppet.

## Config réseau

On utilise les deux pattes réseau des machine physiques. On a d'un côté *eth0* qui sert pour l'admin et DRBD, et des VLANs sur *eth1* pour les VM.

Le fichier ///etc/network/interfaces// doit ressembler à ce qui suit :

    # The loopback network interface
    auto lo
    iface lo inet loopback
  
    # The primary network interface
    auto eth0
    iface eth0 inet static
          address 80.67.169.49
          netmask 255.255.255.128
          broadcast 80.67.169.127
          gateway 80.67.169.1
    iface eth0 inet6 static
          address 2001:910:800::49
          netmask 64
          gateway 2001:910:800::1
  
    source /etc/network/interfaces.ganeti-vlan

La dernière ligne sera ajoutée par Puppet si elle est absente. C'est aussi Puppet qui gère le fichier ///etc/network/interfaces.ganeti-vlan//.

Bien entendu, il ne faut pas oublier de configurer le Procurve pour propager tous les VLAN utiles.

### Puppet, c'est bien joli, mais comment je le configure, hein ?

A priori toutes les machines du cluster ont les mêmes VLAN et je pars du principe qu'elles utilisent toutes l'interface eth1 pour ça, du coup la valeur par défaut est codée en dur dans le module *ganeti* (au début du fichier //manifests/init.pp*). Si on veut surcharger les valeurs pour une machine donnée, dans sa config dans le fichier *site.pp* de Puppet, on remplace *include ganeti// par quelque chose de ce genre :

    class { 'ganeti':
    vlan_interface => 'eth2',
    vlans          => ['3', '801'],
    }

## LVM

La machine doit avoir un groupe de volumes LVM avec de l'espace libre. On l'appelle vg1 (Ganeti réclame le même nom sur toutes les machines et il s'appelle comme ça sur c3po).

Le module Puppet *ganeti* s'occupe d'indiquer à LVM de ne pas aller fourrer son nez dans les volumes DRBD.

## Ajout de la machine au cluster

Depuis le maître :

    # gnt-node add le.fqdn.du.nouveau.noeud

Par exemple :

    # gnt-node add r2d2.fdn.fr

On utilise **exclusivement le FQDN** de la nouvelle machine.

Il faut pouvoir se connecter en SSH au noeud d'en face (avec une clé c'est plus simple, *ssh -A* est ton ami). Il faut aussi pouvoir parler sur le port TCP 1811 (c'est là qu'écoute le démon ''ganeti-noded'').

# Administration exceptionnelle

## Éditer le(s) disque(s) d'une VM depuis un socle

    root@c3po:~# gnt-instance activate-disks leia.fdn.fr
    c3po.fdn.fr:disk/0:/dev/drbd0

Ça nous indique que notre disque virtuel est activé comme ///dev/drbd0*. On peut l'attaquer à coups de *kpartx* et le monter sur le socle ; une fois qu'on a fini (sans oublier l'appel à *kpartx -d// qui va bien) :

    root@c3po:~# gnt-instance deactivate-disks leia.fdn.fr

## Agrandir un disque d'une VM

Commencer par trouver le disque à agrandir :
<code bash>
gnt-instance info yoda.fdn.fr
</code>


Supposons qu'on veuille agrandir le 3ème disque (donc le 2, on compte à partir de 0), et qu'on veuille lui ajouter 40 Go.
<code bash>
gnt-instance grow-disk yoda.fdn.fr 2 40G
</code>

Attention, le dernier paramètre, ici *40G*, représente la différence de taille, pas la nouvelle taille absolue.

C'est fini ? Bah non, la modification n'est pas visible instantanément, il faut redémarrer complètement la VM (un *reboot* depuis son OS ne suffit pas).
<code bash>
gnt-instance shutdown yoda.fdn.fr
gnt-instance start yoda.fdn.fr
</code>


## Forcer un changement de maître

Ça se passe **sur la machine qui doit devenir maître** ; si on le fait sur le maître actif, on a une erreur (pas grave, juste l'opération foire).

    gnt-cluster master-failover

## Récupérer un cluster sans maître

Dans certains cas (genre quand on lance un *master-failover* vers un noeud dont les démons *ganeti-** sont arrêtés), on arrive dans une situation à la con où chaque machine croit que l'autre est maître. Ça se voit dans [[http://leia.fdn.fr/cgi-bin/nagios3/status.cgi?host=droides|Nagios]] : la VIP d'admin est down. Quand ça arrive, **on commence par bien s'assurer que c'est bien le cluster qui est en vrac et pas juste un hoquet réseau**, histoire de ne pas tout casser, et si c'est bien le cas **on commence par relancer les démons** si *ganeti-watcher* ne l'a pas déjà fait (///etc/init.d/ganeti restart* et vérifier que *ganeti-confd* et *ganeti-noded// tournent sur tous les noeuds) puis on force un failover :

    gnt-cluster master-failover --no-voting

Une fois que c'est fait, on n'a peut-être pas le maître où on le voulait au départ, mais on a un maître, c'est déjà pas mal.

## Quand la machine d'admin explose...

Situation : *c3po* (le maître) s'est envoyé en l'air, *r2d2* (l'esclave) reste seul. *r2d2* ne devient pas maître tout seul. **TODO :** regarder si c'est une histoire de quorum ou si la bascule n'est jamais automatique.

**Pour forcer r2d2 à devenir maître :**

    # gnt-cluster master-failover --no-voting

**Pour réintégrer c3po au cluster une fois qu'il est remonté :**

C'est un peu pénible vu que les deux machines se croient maîtres. Le plus simple, sur *r2d2* :

    # gnt-cluster redist-conf

Ça synchronise tous les autres noeuds (y compris quand on en a plus de 2) depuis la machine d'admin. (On sait que c'est «la bonne» quand elle a la VIP d'admin).

Si on avait des VM sur la machine plantée, soit on les relance à la pogne à coups de *gnt-instance*, soit on attend que *ganeti-watcher* (lancé par cron toutes les 5 minutes) les relance.

# Historique

Ce qui suit a été fait lors de l'installation du cluster ; normalement on n'a pas à y revenir.

## Configuration initiale

**C'est déjà fait sur c3po et on ne doit pas le refaire ailleurs, c'est ici juste pour mémoire !**

    # gnt-cluster init --nic-parameters link=br3 --vg-name=vg1 --enabled-hypervisors=kvm \
    --master-netdev=eth0 --drbd-usermode-helper=/sbin/drbdadm droides.fdn.fr

## Tests

    gnt-cluster verify

Un peu plus violent :

    /usr/lib/ganeti/tools/burnin -o debootstrap+default --disk-size 10G --mem-size 512M \
    --vcpu-count 2 -p teebo.fdn.fr paploo.fdn.fr chirpa.fdn.fr

On peut ajouter d'autres VM de test ; elles doivent être dans le DNS et ne pas exister sur le cluster (elles seront créées et détruites pendant le test).

