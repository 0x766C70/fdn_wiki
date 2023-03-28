## Suppression d'un service

1. Arrêt de la supervision :
    - sur [skytop](https://status.fdn.fr/dashboard/components) : désactiver ou supprimer le composant correspondant ;
    - sur [nagios](https://status.fdn.fr/nagios4) : désactiver via l'IHM ou supprimer sur skytop [^1] les sondes correspondantes ;
1. Nettoyage du DNS : chercher toutes les occurences du service et les supprimer, puis pousser les modifications
1. Arrêt du service :
    - si service, l'arrêter sur la machine physique ou la machine virtuelle ;
1. Puppet : faire le ménage :sweat_smile: .

## Suppression d'un serveur/d'une VM

1. Arrêt de la supervision :
    - sur [skytop](https://status.fdn.fr/dashboard/components) : désactiver ou supprimer le composant correspondant ;
    - sur [nagios](https://status.fdn.fr/nagios4) : désactiver via l'IHM ou supprimer sur skytop [^1] les sondes correspondantes ;
    - sur [munin](https://munin.fdn.fr/) : supprimer la configuration du serveur [^2].
1. Nettoyage du DNS : chercher toutes les occurences de la vm et les supprimer, puis pousser les modifications
1. Arrêt de la vm :
    - si machine physique, l'arrêter ;
    - si machine virtuelle, se connecter au cluster proxmox de prod :
        - arrêter la machine virtuelle ;
        - supprimer la machine virtuelle et les disques associés ;
        - [option] supprimer les sauvegardes associées.
1. Puppet :
    - dans le dépôt :
        - supprimer le fichier correspondant dans `hieradata/hosts/` ;
        - supprimer les occurences de *myserver.fdn.fr* (cf. roles et/ou autorisations) ;
    - sur palpatine :
        - supprimer le certificat : `puppetserver ca clean --certname my_server.fdn.fr`
        - faire le ménage dans *puppetdb* : `puppet node deactivate my_server.fdn.fr`

[^1] sur skytop :
1. supprimer `/etc/nagios4/objects/hosts/<my_server>.conf` ;
1. tester la configuration nagios : `sudo nagios4 -v /etc/nagios4/nagios.cfg` ;
1. si OK, recharger nagios : `sudo systemctl reload nagios4`.

[^2] sur cecinestpasleia :
1. supprimer la conf du serveur : `rm /etc/munin/munin-conf.d/<my_server>.conf`
1. [optionnel] supprimer les données du serveur : `rm -f /var/lib/munin/fdn.fr/<my_server>.fdn.fr-*.rrd`
1. redémarrer munin : `systemctl restart munin`
1. redémarrer Apache : `systemctl restart apache2`
