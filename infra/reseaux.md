FDN dispose de deux POP (voir [points de presence](./points_de_presence.md)), avec un switch dans
chaque baie :

  * Un Cisco c2970 en ''11A4'' au Telehouse 2

    - Il s'appelle ''switch-th2-11a4.fdn.fr''
    - Sa référence exacte est WS-C2970G-24TS-E
    - 10.0.0.39, joignable sur le VLAN 801

  * Un Cisco c3560 en ''Z1A11'' à Paris Bourse (pbo)

    - Il s'appelle ''cisco.fdn.fr''
    - 10.0.0.38, joignable sur le VLAN 801

Sommaire :


## Spare

1x SFP 10GbE Eth1/1 @ switch-n3k-3064-th2

## Les VLAN / subnets

VLANs vus par les switches FDN :

| VLAN | Usage                          | Adresses IPv4     | Adresses IPv6        |
| ---- | ------------------------------ | ----------------- | -------------------- |
| 1    | -                              | -                 | -                    |
| 3    | FDN - infra                    | 80.67.169.0/25    | 2001:910:800::/64    |
| 11   | ????                           |                   |                      |
| 14   | FDN - LNS & RADIUS             | 80.67.161.120/29  |                      |
|      |                                | 80.67.161.128/25  |                      |
| 16   | Nerim - Livraison DSL          | 80.67.161.112/29  |                      |
| 17   | Nerim - Livraison DSL (pppoe) (ne sert plus) |                   |                      |
| 20   | tetaneutral.net - Collecte DSL | 80.67.161.32/29   | 2001:910:801::/64    |
| 21   | Grenode - Collecte DSL         | 80.67.161.40/29   | 2001:910:801:21::/64 |
| 22   | Sames - Collecte DSL           | 80.67.161.48/29   |                      |
| 119  | Gitoyen - Grand ternet         | 80.67.161.208/29  | 2001:910:0:800::/64  |
| 126  | Liazo - Interco radius         | 185.96.184.130/31 |                      |
| 127  | Liazo - Interco BestEffort     | 185.96.184.132/31 |                      |
| 128  | Liazo - Interco Premium        | 185.96.184.134/31 |                      |
| 504  | Aquilenet - Collecte FTTH      | 80.67.161.56/29   |                      |
| 530  | Liazo2 - Interco Radius        | 185.96.184.162/31 |                      |
| 531  | Liazo2 - Interco BestEffort    | 185.96.184.164/31 |                      |
| 532  | Liazo2 - Interco Premium       | 185.96.184.166/31 |                      |
| 800  | FDN - intra                    | 10.2.0.0/25       |                      |
| 801  | FDN - admin                    | 10.0.0.0/24       |                      |
| 802  | FDN - replication              | 10.0.2.0/24       |                      |
| 2019 | Franciliens.net - Collecte DSL | 79.143.245.128/29 |                      |
| 2052 | PCLight - Collecte DSL         | 79.143.245.144/29 |                      |

Autre (niveau 2 fourni par Gitoyen, livré à FDN en mode access, pour l'OOB) :

|      | FDN - OOB (consoles switches)  | 10.0.3.0/24       |                      |


## Les préfixes actuellement utilisés à FDN

### IPv4

2 sources d'infos : /etc/bird.conf sur les lns/vpn, et conf radius (mysql sur lns ou si)

la page correspondante [gitoyen](https://doc.gitoyen.net/lir/ra/)

#### Récap

| Prefixe         | Description                     |
| --------------- | ------------------------------- |
| 80.67.160.0/24  | subnets d'adhérents             |
| 80.67.161.0/24  | /29 d'intercos                  |
| 80.67.165.64/26 | vpn openbar                     |
| 80.67.169.0/24  | infra                           |
| 80.67.171.0/26  | vpn openbar                     |
| 80.67.176.0/22  | /32 alloués par le SI (dsl/vpn) |

#### Subnets adhérents:

Subnets à la date du 2022-11-05:

```
mysql> select UATTR_VALUE, UATTR_ID, UATTR.RADUSER_ID, RADUSER_LOGIN, LIGNE_ID, VPN_ID from UATTR left join RADUSER on UATTR.RADUSER_ID = RADUSER.RADUSER_ID where UATTR_ATTR = 'Framed-Route' order by UATTR_VALUE;
+------------------+----------+------------+----------------------------------------+----------+--------+
| UATTR_VALUE      | UATTR_ID | RADUSER_ID | RADUSER_LOGIN                          | LIGNE_ID | VPN_ID |
+------------------+----------+------------+----------------------------------------+----------+--------+
| 80.67.160.104/29 |     4563 |       1688 | jean.charles.delepine@fdn.dslnet.fr    |      917 |     -1 |
| 80.67.160.120/29 |      298 |         84 | philippe.le.brouster@fdn.fr            |       -1 |     28 |
| 80.67.160.128/28 |     1156 |        278 | delphine.rignon@fdn.nerim              |      372 |     -1 |
| 80.67.160.144/30 |     8503 |       2895 | feraud.dimitri@fdn.ilf.kosc            |     1287 |     -1 |
| 80.67.160.160/27 |     8289 |       2244 | cier@vpn.fdn.fr                        |       -1 |    430 |
| 80.67.160.96/29  |     7536 |       2672 | yvan.vanhullebus@vpn.fdn.fr            |       -1 |    545 |
| 80.67.168.112/29 |     7968 |       2779 | carine.bournez@fdn.ilf.kosc            |     1208 |     -1 |
| 80.67.168.136/29 |     5090 |       1871 | 0299090543@fdn.dslnet.fr               |      778 |     -1 |
| 80.67.168.160/29 |     2121 |        527 | benjamin.duchenne@vpn.fdn.fr           |       -1 |     98 |
| 80.67.168.168/29 |     4748 |        430 | arnaud.gomes-do-vale@vpn.fdn.fr        |       -1 |     42 |
| 80.67.179.96/32  |     7897 |       2773 | association.libre.en.comm@fdn.ilf.kosc |     1206 |     -1 |
+------------------+----------+------------+----------------------------------------+----------+--------+
11 rows in set (0.01 sec)
```

Pour ajouter une telle route, il faut:
 - Côté RADIUS FDN, ajouter un attribut Framed-Route avec dedans le subnet à router.  
Aller dans le SI, trouver le membre (par son numéro de tel ou d'adhérent) puis sa ligne,
(view-ligne.cgi?lid=<id>&do=yes) puis son compte radius (view-raduser.cgi?uid=<id>&do=yes)  
De là on va pouvoir lui ajouter un bloc d'IP pour son compte:

En face de "Attributs de l'utilisateur" cliquer sur "Ajouter" et remplir le formulaire comme suit :
(page new-uattr.cgi?uid=<id>&from=raduser<id>)

```
Création/modification d'un attribut radius utilisateur

Nom de l'attribut    Framed-Route
Opérateur         =
Valeur de l'attribut    80.67.160.96/29
Type                    reply
User id                (prérempli)
```

ATTENTION: Pour ajouter plusieurs attributs 'Framed-Route', les suivants (dans l'odre de `UATTR_ID`) doivent utiliser l'opérateur `+=`, et non pas `=`, faute de quoi le radius ne renvoit que la première route.


- Côté routage, il n'y à à priori rien à faire chez FDN (vérifier que le nouveau subnet appartient bien à un subnet qu'on accepte déjà de router dans nos confs bird).  
Chez Gitoyen, il faut qu'ils rajoutent le subnet aux prefixs autorisés à sortir de FDN si ce n'est pas déjà le cas.

- Enfin, côté abonné, il n'y a plus qu'à utiliser les IP de ce subnet (simplement attribuer les IPs en static au routeur par exemple et gérer leurs forwarding directement, ou bien les faire router dans un sous-réseau interne)

#### Historique:

UATTR 'Framed-Route' retirés le 2020-03-22 :

```
|      256 | Framed-Route | =        | 80.67.160.104/30 | reply      |          4 |
|      257 | Framed-Route | =        | 80.67.160.108/30 | reply      |         16 |
|     1813 | Framed-Route | =        | 80.67.165.0./26  | reply      |        451 |
|      656 | Framed-Route | +=       | 80.67.166.128/27 | reply      |        142 |
|      657 | Framed-Route | +=       | 80.67.166.160/27 | reply      |        169 |
|      700 | Framed-Route | =        | 80.67.166.192/27 | reply      |        214 |
|      832 | Framed-Route | =        | 80.67.166.224/27 | reply      |        253 |
|     1214 | Framed-Route | +=       | 80.67.166.96/27  | reply      |        272 |
|      735 | Framed-Route | =        | 80.67.168.112/29 | reply      |          8 |
|      343 | Framed-Route | =        | 80.67.168.128/29 | reply      |        103 |
|      623 | Framed-Route | =        | 80.67.168.152/29 | reply      |        181 |
|     1058 | Framed-Route | =        | 80.67.168.160/29 | reply      |        267 |
|     1219 | Framed-Route | =        | 80.67.168.168/29 | reply      |         34 |
|     1300 | Framed-Route | =        | 80.67.168.176/29 | reply      |        192 |
|     1184 | Framed-Route | =        | 80.67.175.128/28 | reply      |        295 |
|     1185 | Framed-Route | =        | 80.67.175.144/28 | reply      |       1434 |
|     1334 | Framed-Route | =        | 80.67.175.160/28 | reply      |        325 |
|     3429 | Framed-Route | +=       | 80.67.175.176/28 | reply      |        295 |
|      255 | Framed-Route | +=       | 80.67.179.0/24   | reply      |         76 |
|     1339 | Framed-Route | =        | 80.67.180.0/24   | reply      |        321 |
|     2262 | Framed-Route | =        | 80.67.183.0/24   | reply      |        561 |
|     3681 | Framed-Route | =        | 80.67.184.0/23   | reply      |       1444 |
|     2408 | Framed-Route | =        | 80.67.184.0/23   | reply      |        598 |
|     4078 | Framed-Route | =        | 80.67.186.0/23   | reply      |       1575 |
```


### IPv6


/etc/bird6.conf:

```
function abonne() {
        return
                (net ~ 2001:910:800::/48)
 -> les infras
                ||
                (net ~ 2001:910:1000::/38 && net.len = 48)
 -> les subnets adhérents
                ||
                (net = 2001:910:8ff:ffff::/64)
 -> 2001:910:8ff:ffff::1/64 pour les l2tp
```

Rien de plus (les /48 sont donnés par le SI en fonction de l'ipv4, en vrai il faudrait faire le calcul du range ipv6 couvert par le /22 et regarder dehors...):

```
mysql>  select * from UATTR where UATTR_ATTR like 'Framed-IPv6-Route' and not UATTR_VALUE like '%::/48'  order by UATTR_VALUE;
Empty set (0.01 sec)
```

## Ports Cisco c2970 - à TH2

| Port | Description                | Mode   | Vlans                     |
| ---- | -------------------------- | ------ | ------------------------- |
| 01   | interv admin               | access | 801                       |
| 02   | lns11 - eth1               | trunk  | -                         |
| 03   | -                          |        |                           |
| 04   | lns22 - eth1               | trunk  | -                         |
| 05   | -                          |        |                           |
| 06   | nerim - PPPoE (down)       |        |                           |
| 07   | lns11 - ipmi               | access | 801                       |
| 08   | lns11 - ipmi               | access | 801                       |
| 09   | lns11 - eth0               | trunk  | *                         |
| 10   | lns22 - eth0               | trunk  | *                         |
| 11   | -                          |        |                           |
| 12   | -                          |        |                           |
| 13   | -                          |        |                           |
| 14   | -                          |        |                           |
| 15   | -                          |        |                           |
| 16   | Gitoyen 1/0/5 3750         | trunk  | 3,20-22,119,801,2019,2052 |
| 17   | -                          |        |                           |
| 18   | nerim - livraison adsl 1G  | access | 16                        |
| 19   | -                          |        |                           |
| 20   | -                          |        |                           |
| 21   | -                          |        |                           |
| 22   | -                          |        |                           |
| 23   | -                          |        |                           |
| 24   | interv internet            | access | 3                         |
| 25   | sames via gixe (sfp lc sx) | trunk  | 22                        |
| 26   | liazo (sfp gx)             | trunk  | 126-128 530-532           |
| 27   | -                          |        |                           |
| 28   | -                          |        |                           |

* [dump de la conf du switch TH2 du 20160925](./reseaux/switch-fdn-th2-11a4-config-20160925.text)
* [dump de la conf du switch TH2 10G du 20171014](./reseaux/switch-fdn-th2-10g-config-20171014.text)
* [dump de la conf du switch PBO 10G du 20171014](./reseaux/switch-fdn-bourse-10g-config-20171014.text)

## Ports c3560-brs - à PBO

| Port | Mode | Description              |
| ---- | ---- | ------------------------ |
| 1    | On   | C3PO admin               |
| 2    | On   | C3PO vlans               |
| 3    | On   | R2D2 admin               |
| 4    | On   | R2D2 vlans               |
| 5    | On   | C3PX admin               |
| 6    | On   | C3PX vlans               |
| 7    | On   | R4P17 admin              |
| 8    | On   | R4P17 vlans              |
| 9    | On   | RMLL                     |
| 10   | On   |                          |
| 11   | On   |                          |
| 12   | On   |                          |
| 13   | On   | R2D2 ipmi                |
| 14   | On   | C3PO ipmi                |
| 15   | On   |                          |
| 16   | On   |                          |
| 17   | On   |                          |
| 18   | On   |                          |
| 19   | On   |                          |
| 20   | On   |                          |
| 21   | On   |                          |
| 22   | On   |                          |
| 23   | On   |                          |
| 24   | On   | Accès pour interventions |
| 25   | On   | Lien Gitoyen Z1B09 fibre |
| 26   | On   |                          |
| 27   | On   |                          |  
| 28   | On   |                          |
