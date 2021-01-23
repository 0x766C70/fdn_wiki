# Les machines virtuelles Xen chez FDN

** DEPRECATED : Nous ne faisons plus tourner de VM de cette manière. Nous utilisons désormais [[adminsys:ganeti]]. Les machines luke et palpa2 ont été éteintes.**

## Les dom0 et les domU

Les dom0 sont les machines physiques, dans notre cas [[adminsys:serveurs:luke|luke]] et [[adminsys:serveurs:palpa2|palpa2]].

### Création d'un domU

Exemple de la machine virtuelle *jabber* hébergée sur *palpa2* (on suppose le DNS déjà mis à jour avec ''jabber IN A 80.67.169.47'') :

    <code>
    xen-create-image --hostname jabber \
        --lvm xenvg \
        --memory 256 \
        --initrd /boot/initrd.img-2.6.18-6-xen-686 \
        --kernel /boot/vmlinuz-2.6.18-6-xen-686 \
        --swap 256 \
        --size 4G \
        --debootstrap \
        --dist etch \
        --ip 80.67.169.47 --netmask 255.255.255.0 --gateway 80.67.169.1 \
        --passwd \
        --mirror http://debian.gitoyen.net/debian/ \
        --verbose
    </code>


(attention, sur *luke* il faudrait utiliser ''--lvm mirror'')

Puis, éditer la ligne ''vif ='' de ''/etc/xen/jabber.cfg'' comme suit :
    <code>
    vif = [ 'mac=AC:DE:48:00:A9:2F,ip=80.67.169.47' ]
    </code>


  * ''AC:DE:48:00'' correspond à un adressage privé
  * ''A9:2F'' est l'équivalent en hexadécimal de ''169.47'' en décimal

Lancer la machine virtuelle par ''xm create jabber.cfg'', puis se connecter sur la console par ''xm console'' pour les petits ajustements indispensables :
  * ''aptitude install ssh iproute postfix metche apt-show-versions'' (je ne détaille pas la configuration Postfix et metche aujourd'hui)
  * ''adduser --ingroup users tom''
  * ''adduser tom adm''
  * Créer (en recopiant celui d'un autre serveur) ''/root/.ssh/authorized_keys''
  * Modifier ''/etc/ssh/sshd_config'' afin d'interdire l'authentification par mot de passe (''PasswordAuthentication no''), redémarrer le serveur SSH (''/etc/init.d/ssh restart'')

Aller boire un café bien mérité.

### Suppression d'un domu

    <code>
    xen-delete-image rmll
    </code>


Résultat attendu :

- suppression de la conf xen
- suppression des volumes lvm

### PyGrub

PyGrub est un outil du paquet xen-tools qui permet à un domU d'exécuter son propre noyau stocké sur son propre espace de stockage. Cela décorelle encore plus le dom0 des domU.

  * http://wiki.xensource.com/xenwiki/PyGrub
  * http://wiki.debian.org/PyGrub

#### Création d'une vm

Il suffit de rajouter l'option ''--pygrub'' à la commande xen-create-image citée ci-dessus.

#### Passage à PyGrub

Sur luke et palpa2, pour passer à PyGrub voici les opérations à effectuer pour chaque domU :

 * Si ce n'est pas déjà fait, réaliser la migration du domU en devices xvda, xvdb etc. (modifier le ''/etc/fstab'' du domU, shutdown, modifier le ''domU.cfg'' (root= et disk=), redémarrer le domU)

 * Si ce n'est pas déjà fait, dans ''/etc/inittab'' du DomU remplacer tty1 par hvc0

 * Sur le domU:
    <code>
    # mkdir /boot/grub
    # apt-get install linux-image-xen-686 grub # (attention, pour squeeze il faut prendre grub-legacy pour ne pas se retrouver avec grub2)
    # update-grub
    </code>

 
 * Sur le dom0, dans le fichier de conf du domU correspondant (''/etc/xen/hostname.cfg''), supprimer les lignes kernel= et ramdisk= et ajouter la ligne suivante :
    <code>
    bootloader = '/usr/lib/xen-default/bin/pygrub'
    </code>


 * vérifier que dans la définition des disques celui qui contient la partition de boot est le premier :
    <code>
    disk    = [
        'phy:mirror/blou-disk,xvda,w',
        'phy:mirror/blou-swap,xvdb,w',
    ]
    </code>


 * redémarrer le domU

