**Cluster**
Utilisons le VLAN 802 qui est notre VLAN Replication pour que les Hosts échangent hors du réseau de prod.

**Pré-requis**
Il faut que /etc/hosts inclue l'IP de chaque host et non pas simplement localhost sinon ça ne fonctionne pas ! (https://pve.proxmox.com/wiki/Cluster_Manager#_preparing_nodes)

**Pour tc14** :

```
127.0.0.1	localhost
#127.0.0.1	tc14.fdn.fr tc14
80.67.169.80	tc14.fdn.fr tc14
10.0.2.80	tc14.fdn.fr tc14
10.0.2.81	r5d4.fdn.fr r5d4

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
2001:910:800::80 tc14.fdn.fr tc14
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```

**Pour r5d4** :

```
127.0.0.1	localhost
#127.0.0.1	r5d4.fdn.fr r5d4
80.67.169.81	r5d4.fdn.fr r5d4
10.0.2.81	r5d4.fdn.fr r5d4
10.0.2.80	tc14.fdn.fr tc14

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
2001:910:800::81 r5d4.fdn.fr r5d4
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
```
L'IP VLAN 802 du node en face a été aussi ajouté à /etc/hosts chaque host (ce n'est normalement pas utile car les nodes ont été configurées par leur IP des VLAN 802 et non des hostname, simple précaution)

**Création du Cluster**

**Sur tc14** :

Datacenter -> Cluster -> Create Cluster -> Nom : FDN et IP : (mettre l'IP du VLAN 802 de tc14, 10.0.2.80 )

**Sur r5d4** :

Datacenter -> Cluster -> Join Cluster et copier les information depuis tc14 et bien penser à mettre IP du VLAN 802 de r5d4, 10.0.2.81

Le node est bien ajouté dans la liste des Hosts dans l'arborescence de gauche sous *Datacenter (FDN)* mais il est injoignable (Connection Error) -> voir ci-dessous

**Spécificité FDN depuis utilisation du QiQ Gitoyen**
Il faut que l'on règle un problème de multicast (même problème que pour nos LNS). 

Le clustering Proxmox utilise aussi le multicast pour faire parler ses nodes, et donc ça ma valu 1h pour comprendre (Communication Error était mon seul indice) FAIL !

Il y a une méthode pour utiliser de l'unicast, l'ordre des commandes est importante :

*  se connecter en ssh sur chaque node
*  mettre les nodes en quorate state : `pvecm e 1` sinon la modfication des fichiers est impossible (le repertoire /etc/pve n'est peuplé que quand le cluster existe, si on stop de cluster, tous les fichier dans ce repertoire disparaissent.
*  editer /etc/pve/corosync.conf et ajouter   *transport: udpu* dans la section *totem* et augmenter la version de *config_version:*
* repeter la même opération sur le node voisin  
*  `systemctl restart corosync` sur chaque node (`killall -9 corosync` si ça ne marche pas)
*  enfin `/etc/init.d/pve-cluster restart` sur chaque node et Voilà
 
 