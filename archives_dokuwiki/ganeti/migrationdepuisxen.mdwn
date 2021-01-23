# Notes en vrac

À nettoyer et à remettre dans l'ordre (genre, installer ce qu'il faut sur la VM d'origine avant de l'arrêter).

----

http://blogs.glou.org/arnaud/2012/01/17/migrer-une-vm-de-xen-vers-kvm/

Ajouter ça dans inittab :

    c1:2345:respawn:/sbin/getty 38400 tty1
    T0:23:respawn:/sbin/getty ttyS0 38400

Arreter la VM.

Sur c3po :

    lvcreate -L4G -n migration-vpn1 vg1
    fdisk /dev/vg1/migration-vpn1

Creer une partition racine et une pour le swap (comme sur l'original).

    kpartx -av /dev/vg1/migration-vpn1

Ça crée les partitions dans /dev/mapper/

    mkswap /dev/mapper/vg1-migration--vpn1p2
    mkfs -j /dev/mapper/vg1-migration--vpn1p1
    mount /dev/mapper/vg1-migration--vpn1p1 /mnt

Sur palpa2 :

    mkdir /mnt/vpn1-root
    mount /dev/xenvg/vpn-disk /mnt/vpn1-root/
    rsync -av /mnt/vpn1-root/ root@c3po:/mnt/

Sur c3po, éditer /mnt/etc/fstab et mettre les partitions en face
des trous (les disques vus de la VM s'appelleront vda, vdb...).


    umount /mnt
    kpartx -dv /dev/vg1/migration-vpn1

    gnt-instance add --no-start -t plain -n $(hostname) --disk 0:adopt=migration-vpn1 -o debootstrap+default vpn1.fdn.fr
    gnt-instance modify -t drbd -n r2d2.fdn.fr vpn1.fdn.fr
    gnt-instance modify  --net 0:mac=ac:de:48:00:a9:2d  vpn1.fdn.fr
    gnt-instance modify -H kernel_path=/boot/vmlinuz-3.2.0-4-amd64,initrd_path=/boot/initrd.img-3.2.0-4-amd64 vpn1.fdn.fr
    gnt-instance start vpn1.fdn.fr


############### Là, ça marche ########################

Sauf que la VM n'a pas les modules qui vont avec le noyau, du coup il y a des
trucs qui risquent de ne pas marcher.

Sur la VM, configurer le depot backports :

    cat > /etc/apt/sources.list.d/backports.list <<EOF
    deb http://mirrors.ircam.fr/pub/debian-backports/ squeeze-backports main
    EOF
    apt-get update

puis installer un noyau récent et grub2, et virer le noyau xen :

    apt-get install -t squeeze-backports linux-image-686
    apt-get purge linux-image-2.6.32-5-xen-686
    apt-get install grub
    grub-install /dev/vda

Changer la valeur de GRUB_CMDLINE_LINUX_DEFAULT dans /etc/default/grub :

    GRUB_CMDLINE_LINUX_DEFAULT="console=ttyS0,38400n8"

Puis :

    update-grub
    poweroff

Sur c3po, on vire le noyau local et on laisse grub vivre sa vie :

    gnt-instance modify -H kernel_path=,initrd_path= vpn1.fdn.fr

Ayé, c'est gagné, plus qu'à relancer la VM.
