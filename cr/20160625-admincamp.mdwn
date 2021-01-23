[[!meta title="Admincamp n°6 - 25/26 juin 2016"]]
[[!meta date="20160625"]]
[[!tag done]]

Admincamp FDN n°6

Dates: 25 et 26 juin à partir de 9h    
Lieu: 60 rue des Orteaux, Paris 20e.    
Wiki: https://adminsys.fdn.fr     

[[!toc levels=2]]

# Présences

**Venir c'est bien, s'inscrire en plus c'est mieux !**

Là : olb, Fabien, Benjamin, sebian, DelTree, blackmoor (mais qu'a partir du samedi après-midi), VG, tom28, 

Pas là : belette, Ben, CapsLock, nono, mat

Groupe trésorerie (dimanche 14h): Thomas, Sylvain, Kevin

# coordination
                                                                       
## Maintenir un changelog global sur le wiki

On met en place un endroit où chaque personne qui fait quelque chose sur
l'infra raconte ce qu'il a fait (et met des liens vers la doc).  C'est pratique
pour se faire idée de se qui se passe, et ne pas être largué quand on essaye de
raccrocher.


## Objectif ménage dans la baie 11A4 de Téléhouse2 au prochain admin camp

Au prochain admincamp, nous pensons intervenir dans la baie de gitoyen à TH2.
Il s'agirait de :

- mettre à la benne un ancien LNS
- éteindre et mettre à la benne vador
- déplacer un nouveau LNS à coté de l'autre et du switch

Pour cela, d'ici là, il est nécessaire de :

- migrer le wiki adhérent (olb)
- migrer le mx secondaire (tom28)
- commander des rails adaptés à la baie télécom en 11A4 à Téléhouse 2 (fsirjean)
- envoyer un mail à Gitoyen quand on est à peu près sûr que ça se passe bien

## Création d'un troisième résolveur DNS hors de l'AS de Gitoyen

Pour ne pas être dépendant uniquement de notre infra, nous voulons
mettre en place un resolveur DNS sur la machine isengard à LDN.

A priori, il sera limité à Gitoyen, l'AS auquel FDN participe. 


# Choses faites dans le weekend

  * 2016-06-25 11:24 (olb) - [tunnels chiffrés] suppression du filtre is_tunnel dans bird
   
    Ce filtre n'est pas tellement nécessaire et nous oblige à le mettre à jour lors de la propagation de nouveaux préfixes. Ça ne regle que partiellement la problématique car on a encore des filtres sur les LNS.
  
  * 2016-06-25 12:24 (fsirjean) - [droides] rétablissement du drbd sur toutes les vm du cluster ganeti.
  
  * 2016-06-25 12:35 (fsirjean) - [machines] supprimé la vm vpn-loutre1 + éléments liés nagios & puppet, le projet étant mort.
  
  * 2016-06-25 12:57 (olb, vg) - [puppet] configuration via puppet de la locale par defaut (la même sur toutes les machines)
  
  * 2016-06-25 13:16 (olb, vg) - [équipage] Création du compte de vg sur obiwan (groupe adminsys) et inscription à la liste adminsys
  
  * 2016-06-25 14:00 (olb) - [droides] Gestion d'un problème sur Ganeti. Probablement encore cette histoire de minor count.
  
  * Ganeti s'est pris les pieds dans le tapis sur une conversion de vm plain -> drbd. Il a fallu remettre dans la conf de ganeti les bons chemins de logical volume lvm. En suivant cette procédure : https://code.google.com/p/ganeti/wiki/EditingTheConfiguration
  
  * 2016-06-25 16:56 (olb) - [équipage] Création du compte de blackmoor sur obiwan (groupe adminsys) et inscription à la liste adminsys
  
  * 2016-06-26 00:14 (olb, fsirjean) - [droides] Mise à jour des droides en jessie. Passage à Ganeti 2.14. Infra is up after 7h of black-out.
    
    On a du refaire un dpkg-reconfigure sur c3px pour que les droïdes démarrent correctement et refaire un dpkg-reconfigure grub sur r4p17 (tout ça à distance avec les outils de supermicro).

  * 2016-06-26 12:19 (fsirjean) - [letsencrypt] Création d'une liste de domaines à passer + --quiet sur les dernières machines.
  
  * 2016-06-26 matin (olb) - [conf web] diminution du nombre de redirections sur fdn.fr
  
  * 2016-06-26 matin (olb, vg) - bug apt-dater & /dev/pts/0 => attendre stretch (screen => tmux)
  
  * 2016-06-26 16h49 (fsirjean) - [droides] gnt-cluster modify --reserved-lvs='vg1/root' done.
  
  * 2016-06-26 18:05 (olb, vg) - [puppet] conf screen & bug fichier /etc/aliases manquant
  
  * 2016-06-26 20:00 (olb, tom28) - [ganeti] réparation des disques de certaines vm.
  
    Nous avions les messages suivants (sudo drdb-overview):
    
    * r4p17 :
      
          12:??not-found??  WFBitMapS Primary/Secondary UpToDate/Consistent 

    * c3px :
    
          12:??not-found??  WFBitMapT  Secondary/Primary Outdated/UpToDate

    Nous avons éteint et redémarré les vm concernées. Et les disques se sont resynchronisés.

  * 2016-06-26 22:00 (olb) - [ganeti] rajout d'un vcpu à chaque vm vpn (il faut les redémarrer).


# Choses à faire (non exhaustif)

* Annoncer adminsys.fdn.fr sur bénévoles/membres
* tunnels chiffrés: alléger les filtres dans bird lns01, lns02
* https: continuer let's encrypt que manque-t-il ?
* web asso: migration de blog.fdn.fr sur obiwan
* etckeeper : faire un mail à admin@ quand /etc change
* migration flyspray sur kilo
* migration wiki sur kilo
* resolver DNS : migration des resolvers DNS sur resolver1 et resolver2
* extinction de vador
* noyau : mettre en place le système de rôles pour les authorisations (olb)
* mails : Passer sur la config SSL/TLS des mails
* tunnels chiffrés : créer une nouvelle vm pour les vpn (2 cpu)
* tunnels chiffrés : ajouter un deuxième cpu aux vm vpn1 et vpn2
* tunnels chiffrés : il faudrait virer l'ancienne allocation dans le reverse DNS de 2001:910:802::/64 qui ne servira pas finalement.
* tunnels chiffrés : ajouter des flags cpuid pour accélérer le chiffrement: `gnt-instance modify -H cpu_type=qemu64,+pclmulqdq,+ssse3,+sse4_1,+sse4_2,+aes,+avx vpn1` et de même pour `vpn2`, `vpn-open1`
* supervision : plein de boutons à tourner, de sondes à ajouter, de trucs et de machins à puppetiser...
* supervision : pertinence d'alertes par mail ? pas pour tout, bien sûr
* gitoyen : nanobsd gitoyen, soucis d'etherchanel (need help)
* gitoyen : livraison gitoyen-fdn pbo, redondance
* ...

