# L'accounting à FDN

La bande passante que nous évaluons actuellement est uniquement celle issue des lignes ADSL et VPN. Il faudrait, à terme, évaluer celle de tous les abonnés, quel que soit le moyen d'accès.

  * Pour l'ADSL
    * Depuis les LNS, l2tpns compte les paquets émis et reçus pour chaque abonné, dans un fichier qui contient le timestamp du moment, dans /var/run/l2tpns/acct
  * Pour les VPNs
    * Depuis ''vpn'', openvpn compte les paquets émis et reçus pour chaque login, en vrac dans ''/var/log/openvpn-{udp,tcp}-status.log'' . C'est en nombre d'octets depuis le début de la connexion.
    * Un cron est lancé sur ''vpn'' toutes les 5 minutes (cf ''/etc/cron.d/pourcentile'') pour collecter ces nombres, en stockant la dernière valeur de chaque session dans "/var/run/openvpn/login starttime", et en mettant le delta dans "/var/run/openvpn/acct/time" (tout cela en gardant un verrou sur le fichier "login starttime" pour éviter la concurrence avec le script de déconnexion qui stocke le nombre des derniers octets transmis) au même format que ce que produit l2tpns.

  * Sur vador, un cron (cf /etc/cron.d/pourcentile) exécute /usr/local/bin/syncrrd.sh qui est chargé de récupérer (par rsync+ssh) ces fichiers toutes les 5 minutes, pour en générer un fichier RRD par abonné, contenant toute sa consommation depuis un an. Les fichiers générés se trouvent dans /var/lib/rrd/, classés par login utilisé. On les fichiers @fdn.nerim pour l'ADSL, et @vpn.fdn.fr pour les VPNs.
  * Un autre efface les fichiers rapatriés des LNS dans /var/spool/rrd (attention, ils ne sont pas au format RRD) de plus d'un an, et un autre envoie un mail chaque jour à suivi-adsl@fdn.fr avec un résumé du trafic du jour
  * Les graphiques sont visibles par l'adhérent dans une page sur https://vador.fdn.fr/adherents/ , les images sont générées à la volée depuis les fichiers .rrd

Ancien script, plus utile a priori:

  * Un autre (/usr/local/bin/graphrrd.sh) script est lancé toutes les 5 minutes également, afin de créer les graphs dans /var/www/rrd/images
