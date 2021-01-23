[[!meta title="Munin"]]

Munin tourne sur leia, on peut voir la sortie sur <https://munin.fdn.fr/>

L'accès est réservé aux personnes disposant d'un htpassword.

Pour ajouter une machine à la supervision:

  * Sur le client
    * ajouter à /etc/nagios/nrpe_local.cfg ce qu'on veut superviser en plus de la config par défaut
    * modifier /etc/nagios/nrpe.cfg pour ajouter l'ip de leia dans allowed_hosts, 80.67.169.12
    * redémarrer nagios-nrpe-server.
    * modifier /etc/munin/munin-node.conf pour ajouter l'ip de leia sur une ligne allow
    * redémarrer munin-node

  * Sur leia
    * ajouter la machine à /etc/munin/munin.conf

Note: il faut quelques minutes pour que ça soit visible sur l'interface web.
