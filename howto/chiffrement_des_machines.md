[[!meta title="Chiffrement des machines"]]

Certaines machines de FDN sont chiffrées. Cela veut dire que les données sur le
disque dur sont chiffrées et que une fois la machine éteinte il est très
difficile d'y avoir accès sans le secret qui permet de déchiffrer les données.

## Procédures

### démarrer une machine chiffrée (via ssh)

Les machines chiffrées de FDN ont un petit serveur ssh dans l'initramfs. Ce
serveur ssh écoute juste avant d'avoir besoin d'accéder au disque. Ainsi pour
démarrer une machine chiffrée, il faut se connecter en ssh et taper la
passphrase et déverrouiller les disques :

    ssh -t -o UserKnownHostsFile=~/.ssh/boot-known_hosts root@kamino.fdn.fr "/lib/cryptsetup/askpass 'FDN Passphrase : ' > /lib/cryptsetup/passfifo"

La phrase de passe est stockée avec les autres secrés partagés de FDN.

### démarrer un machine chiffrée (via la console ganeti)

Pour les vm du cluster ganeti, c'est aussi possible de taper la passphrase via
la console ganeti à partir du master ganeti :

    gnt-instance console <la machine>

### ajouter des accès au server ssh de l'initramfs

Le mini serveur ssh, c'est dropbear et le fichier `authorized_keys` se trouve
ici :

    /etc/dropbear-initramfs/authorized_keys

Pour y ajouter l'admin toto, il faut faire comme cela :

    cat /home/todo/.ssh/authorized_keys >> /etc/dropbear-initramfs/authorized_keys
    update-initramfs -u -k all
    etckeeper commit "ajout de l'utilisateur toto à dropbear"


## Installation

### cryptsetup

Se fait à l'installation de la machine dans un debian-installer.

### serveur ssh

Sous stretch :

    apt install dropbear-initramfs
    cat authorized_keys >> /etc/dropbear-initramfs/authorized_keys
    update-initramfs -u -k all

### configuration grub

Pour l'ip du ssh et la console ganeti pour l'init :

    # rajouter la ligne suivante à /etc/default/grub (en l'adaptant)
    # GRUB_CMDLINE_LINUX="ip=address::gateway:mask:hostname:interface:"
    cat >>/etc/default/grub <<EOF
    GRUB_CMDLINE_LINUX="ip=80.67.169.73::80.67.169.1:255.255.255.128:kamino:eth0: console=ttyS0,115200n8"
    EOF
    update-grub


