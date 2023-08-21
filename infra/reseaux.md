FDN dispose de deux POP (voir [points de presence](./points_de_presence.md)), avec un switch dans
chaque baie :

  * Un Cisco Nexus 3064 en ''11A4'' au Telehouse 2 (TH2)

    - Il se nomme ''SW-TH2-10G'' et étiquetté ''n3k-3064-th2''
    - Sa référence exacte est : cisco Nexus3064 Chassis ("48x10GE + 16x10G/4x40G Supervisor")
    - 10.0.0.50, joignable sur le VLAN 801

  * Un Cisco Nexus 3064 en ''114'' à Equinix PA3

    - Il se nomme ''SW-PA3-10G'' et étiquetté ''n3k-3064-pbo''
    - Sa référence exacte est : cisco Nexus3064 Chassis ("48x10GE + 16x10G/4x40G Supervisor")
    - 10.0.0.51, joignable sur le VLAN 801

Sommaire :

[[_TOC_]]

## Spare

- 1x SFP 10GbE Eth1/1 @ switch-n3k-3064-th2
- 1x 3560G @ PA3

## Les VLAN / subnets

VLANs vus par les switches FDN (à date du 2023-08-21) :

| VLAN | Usage                          | Adresses IPv4     | Adresses IPv6        |
| ---- | ------------------------------ | ----------------- | -------------------- |
| 1    | -                              | -                 | -                    |
| 3    | FDN - infra                    | 80.67.169.0/25    | 2001:910:800::/64    |
| 11   | ???? LNS11 eth0 TH2 (inutilisé)|                   |                      |
| 14   | FDN - LNS & RADIUS             | 80.67.161.120/29  |                      |
|      |                                | 80.67.161.128/25  |                      |
| 16   | Nerim - Livraison DSL          | 80.67.161.112/29  |                      |
| 17   | Nerim - Livraison DSL (pppoe) (ne sert plus) |                   |                      |
| 20   | tetaneutral.net - Collecte DSL | 80.67.161.32/29   | 2001:910:801::/64    |
| 21   | Grenode - Collecte DSL         | 80.67.161.40/29   | 2001:910:801:21::/64 |
| 22   | Sames - Collecte DSL           | 80.67.161.48/29   |                      |
| 119  | Gitoyen - Grand ternet         | 80.67.161.208/29  | 2001:910:0:800::/64  |
| 126  | Liazo - Interco radius TH2     | 185.96.184.130/31 |                      |
| 127  | Liazo - Interco BestEffort TH2 | 185.96.184.132/31 |                      |
| 128  | Liazo - Interco Premium TH2    | 185.96.184.134/31 |                      |
| 129  | Liazo - Interco FTTH TH2       | 185.96.185.93/31  |                      |
| 504  | Aquilenet - Collecte FTTH      | 80.67.161.56/29   |                      |
| 530  | Liazo2 - Interco Radius PA3    | 185.96.184.162/31 |                      |
| 531  | Liazo2 - Interco BestEffort PA3| 185.96.184.164/31 |                      |
| 532  | Liazo2 - Interco Premium PA3   | 185.96.184.166/31 |                      |
| 533  | Liazo2 - Interco FTTH PA3	| 185.96.185.91/31  |                      |
| 800  | FDN - intra                    | 10.2.0.0/25       |                      |
| 801  | FDN - admin                    | 10.0.0.0/24       |                      |
| 802  | FDN - replication              | 10.0.2.0/24       |                      |
| 2019 | Franciliens.net - Collecte DSL | 79.143.245.128/29 |                      |
| 2052 | PCLight - Collecte DSL         | 79.143.245.144/29 |                      |

Autre (niveau 2 fourni par Gitoyen, livré à FDN en mode access, pour l'OOB) :


| VLAN | Usage                          | Adresses IPv4     | Adresses IPv6        |
| ---- | ------------------------------ | ----------------- | -------------------- |
|      | FDN - OOB (consoles switchs)   | 10.0.3.0/24       |                      |


## Les préfixes actuellement utilisés à FDN

### IPv4

2 sources d'infos : /etc/bird.conf sur les LNS/VPN, et conf radius (MySQL sur LNS ou le SI).

La page correspondante [gitoyen](https://doc.gitoyen.net/lir/ra/).

#### Récap

| Prefixe         | Description                     |
| --------------- | ------------------------------- |
| 80.67.160.0/24  | subnets d'adhérents             |
| 80.67.161.0/24  | /29 d'intercos                  |
| 80.67.165.64/26 | vpn openbar                     |
| 80.67.169.0/24  | infra                           |
| 80.67.171.0/26  | vpn openbar                     |
| 80.67.176.0/22  | /32 alloués par le SI (xDSL/FTTH/VPN) |

#### Subnets adhérents

Subnets à la date du 2023-08-22 :

```
mysql> select UATTR_VALUE, UATTR_ID, UATTR.RADUSER_ID, RADUSER_LOGIN, LIGNE_ID, VPN_ID from UATTR left join RADUSER on UATTR.RADUSER_ID = RADUSER.RADUSER_ID where UATTR_ATTR = 'Framed-Route' order by UATTR_VALUE;
+------------------+----------+------------+----------------------------------------+----------+--------+
| UATTR_VALUE      | UATTR_ID | RADUSER_ID | RADUSER_LOGIN                          | LIGNE_ID | VPN_ID |
+------------------+----------+------------+----------------------------------------+----------+--------+
| 80.67.160.104/29 |     8717 |        363 | jean.charles.delepine.1@vpn.fdn.fr     |       -1 |     13 |
| 80.67.160.120/29 |      298 |         84 | philippe.le.brouster@fdn.fr            |       -1 |     28 |
| 80.67.160.128/28 |     1156 |        278 | delphine.rignon@fdn.nerim              |      372 |     -1 |
| 80.67.160.160/27 |     8289 |       2244 | cier@vpn.fdn.fr                        |       -1 |    430 |
| 80.67.160.96/29  |     7536 |       2672 | yvan.vanhullebus@vpn.fdn.fr            |       -1 |    545 |
| 80.67.168.112/29 |     7968 |       2779 | carine.bournez@fdn.ilf.kosc            |     1208 |     -1 |
| 80.67.168.136/29 |     5090 |       1871 | 0299090543@fdn.dslnet.fr               |      778 |     -1 |
| 80.67.168.160/29 |     2121 |        527 | benjamin.duchenne@vpn.fdn.fr           |       -1 |     98 |
| 80.67.168.168/29 |     4748 |        430 | arnaud.gomes-do-vale@vpn.fdn.fr        |       -1 |     42 |
| 80.67.179.96/32  |     7897 |       2773 | association.libre.en.comm@fdn.ilf.kosc |     1334 |     -1 |
+------------------+----------+------------+----------------------------------------+----------+--------+
10 rows in set (0.009 sec)
```

Pour ajouter une telle route, il faut :
 - Côté RADIUS FDN, ajouter un attribut ''Framed-Route'' avec dedans le subnet à router.  
Aller dans le SI, trouver le membre (par son numéro de tel ou d'adhérent) puis sa ligne,
(''view-ligne.cgi?lid=<id>&do=yes'') puis son compte radius (''view-raduser.cgi?uid=<id>&do=yes'')
De là on va pouvoir lui ajouter un bloc d'IP pour son compte :

En face de "Attributs de l'utilisateur" cliquer sur "Ajouter" et remplir le formulaire comme suit :
(page ''new-uattr.cgi?uid=<id>&from=raduser<id>'')

Création/modification d'un attribut radius utilisateur :
```
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

## Ports Cisco Nexus 3064 à TH2

À date du 2023-08-21 :

| Port      | Name              | Status    | Vlan     | Duplex  | Speed   | Type
| -------   | -----             | -------   | -----    | ------  | ------  | -----
| Eth1/1    | --                | sfpInvali | 1        | auto    | 100     | 10Gbase-LR            
| Eth1/2    | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/3    | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/4    | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/5    | FREE              | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/6    | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/7    | tc14 vlans        | connected | trunk    | full    | 10G     | SFP-H10GB-CU1.255M    
| Eth1/8    | tc14 replication  | connected | trunk    | full    | 10G     | SFP-H10GB-CU1.255M    
| Eth1/9    | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/10   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/11   | lns11 - eth0      | connected | trunk    | full    | 1000    | 1000base-T            
| Eth1/12   | nanopi-th2-admin  | connected | 801      | full    | 100     | 1000base-T            
| Eth1/13   | r4p17 replication | connected | trunk    | full    | 1000    | 1000base-T            
| Eth1/14   | r4p17 vlans       | connected | trunk    | full    | 1000    | 1000base-T            
| Eth1/15   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/16   | "Acces pour intervention"| notconnec | 801      | full    | 1000    | 1000base-T            
| Eth1/17   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/18   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/19   | R4P17 IPMI        | connected | 801      | full    | 100     | 1000base-T            
| Eth1/20   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/21   | lns11 IPMI        | connected | 801      | full    | 100     | 1000base-T            
| Eth1/22   | tc14 IPMI         | connected | 801      | full    | 1000    | 1000base-T            
| Eth1/23   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/24   | Acces intervention Internet| sfpAbsent | 3        | full    | 1000    | --                    
| Eth1/25   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/26   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/27   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/28   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/29   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/30   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/31   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/32   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/33   | Interco_collete_xDSL_Nerim| connected | 16       | full    | 1000    | 1000base-T            
| Eth1/34   | FREE              | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/35   | sames via gixe    | connected | trunk    | full    | 1000    | 1000base-SX           
| Eth1/36   | Interco_collete_xDSL_Ielo_LIA-15323| connected | trunk    | full    | 1000    | SFP-1000BX-10-U       
| Eth1/37   | Interco_collete_FTTH_Ielo_LIA-15323| connected | trunk    | full    | 10G     | 10Gbase-LR            
| Eth1/38   | vers gitoyen-n3k-3064-11a4-th2-par Q-in-Q| connected | trunk    | full    | 10G     | 10Gbase-LR            
| Eth1/39   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/40   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/41   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/42   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/43   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/44   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/45   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/46   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/47   | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/48   | upstream-gitoyen  | connected | trunk    | full    | 10G     | SFP-H10GB-CU2.255M    
| Eth1/49/1 |  --               | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/49/2 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/49/3 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/49/4 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/50/1 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/50/2 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/50/3 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/50/4 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/51/1 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/51/2 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/51/3 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/51/4 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/52/1 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/52/2 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/52/3 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| Eth1/52/4 | --                | sfpAbsent | 1        | full    | 10G     | --                    
| mgmt0     | --                | notconnec | routed   | auto    | auto    | --                    

* [dump de la conf du switch TH2 10G](./reseaux/switch-TH2-10G-running-config.text)
* [dump de la conf du switch PA3 10G](./reseaux/switch-PA3-10G-running-config.text)

## Ports Cisco Nexus 3064 à PA3

À date du 2023-08-21 :

| Port      | Name              | Status    | Vlan     | Duplex  | Speed  | Type
| -------   | -----             | -------   | -----    | ------  | ------ | -----
| Eth1/1    | c3po-replication  | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/2    | c3po-vlans        | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/3    | r2d2-replication  | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/4    | r2d2-vlans        | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/5    | c3px replication  | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/6    | c3px vlans        | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/7    | --                | sfpAbsent | 1        | full    | 1000   | --                    
| Eth1/8    | --                | sfpAbsent | 1        | full    | 1000   | --                    
| Eth1/9    | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/10   | FREE              | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/11   | r5d4 vlans        | connected | trunk    | full    | 10G    | SFP-H10GB-CU1.255M    
| Eth1/12   | r5d4 replication  | connected | trunk    | full    | 10G    | SFP-H10GB-CU1.255M    
| Eth1/13   | lns22 - eth0      | connected | trunk    | full    | 1000   | 1000base-T            
| Eth1/14   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/15   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/16   | "Acces pour intervention"     | notconnec| 3       | full   | 1000    1000base-T            
| Eth1/17   | R2D2 IPMI         | connected 801        | full    | 100    | 1000base-T            
| Eth1/18   | C3PO IPMI         | connected 801        | full    | 100    | 1000base-T            
| Eth1/19   | C3PX IPMI         | connected 801        | full    | 100    | 1000base-T            
| Eth1/20   | --                | sfpAbsent | 1        | full    | 1000   | --                    
| Eth1/21   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/22   | r5d4 IPMI         | connected 801        | full    | 1000   | 1000base-T            
| Eth1/23   | LNS22 IPMI        | connected 801        | full    | 100    | 1000base-T            
| Eth1/24   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/25   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/26   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/27   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/28   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/29   | nanopi-pa3-admin  | connected 801        | full    | 100    | 1000base-T            
| Eth1/30   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/31   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/32   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/33   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/34   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/35   | FREE              | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/36   | FREE              | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/37   | Interco_collecte_xDSL-FTTH_Ielo_LIA-15323| connected | trunk    | full    | 10G    | 10Gbase-LR            
| Eth1/38   | vers_gitoyen-n3k-3064-baie114-PA3-Q-In-Q| connected | trunk    | full    | 10G    | 10Gbase-LR            
| Eth1/39   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/40   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/41   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/42   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/43   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/44   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/45   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/46   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/47   | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/48   | upstream-gitoyen  | connected | trunk    | full    | 10G    | 10Gbase-LR            
| Eth1/49/1 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/49/2 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/49/3 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/49/4 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/50/1 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/50/2 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/50/3 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/50/4 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/51/1 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/51/2 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/51/3 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/51/4 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/52/1 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/52/2 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/52/3 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| Eth1/52/4 | --                | sfpAbsent | 1        | full    | 10G    | --                    
| mgmt0     | --                | notconnec | routed   | auto    | auto   | --
