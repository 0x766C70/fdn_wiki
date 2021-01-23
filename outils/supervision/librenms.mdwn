[[!meta title="LibreNMS"]]

LibreNMS tourne sur boba (comme Boba Fett, le chasseur de primes, qui a « trop la classe »), on peut voir la sortie sur <https://librenms.fdn.fr/>

L'accès est réservé aux personnes disposant d'un htpassword.


# Note sur l'installation/configuration

Sur chaque machine gérée par les adminsys de FDN ayant une ip dans le vlan "FDN - intra", un daemon snmpd est automatiquement installé et écoute dans ce réseau.

librenms utilise les alias des interfaces pour les catégoriser : https://docs.librenms.org/#Extensions/Interface-Description-Parsing/

## Alias sur les intefaces statiques

Dans le fichier `/etc/network/interfaces`, on rajoute par exemple la ligne `up ip link set $IFACE alias "Cust: Resolveurs DNS (resolver0.fdn.fr)"`.

## Alias des interfaces sur les hyperviseurs

Le script /etc/ganeti/kvm-vif-bridge a été modifié pour rajouter des alias aux interfaces tap créées par ganeti.

