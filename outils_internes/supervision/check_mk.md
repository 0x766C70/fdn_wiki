
# TODO

* Refaire une passe sur les anciens hostgroups et servicegroups nagios et voir ce qu'on garde ou pas,
* vérifier les sondes sur vador et si,
* automatiser l'ajout des clients (probablement plus simple si on avait une PuppetDB),
* sondes ping IPv4 et IPv6,
* superviser BIRD, PostgreSQL, Puppet, Keepalived avec check_mk.

# Généralités
check_mk est une extention de Nagios permettant de sonder en local un serveur (esclave).
L'agent est installé sur chaque serveur à monitorer.
L'interêt principal pour FDN est d'automatiser le monitoring de nouvelles machines via puppet.

# Documentation
check_mk documentation : <http://mathias-kettner.com/checkmk.html>

# Coté client (agent)
### En manuel: 
    apt-get install check-mk-agent xinetd

Créer le fichier /etc/xinetd.d/check.mk
    
    service check_mk
    {
    type           = UNLISTED
    port           = 6556
    socket_type    = stream
    protocol       = tcp
    wait           = no
    user           = root
    server         = /usr/bin/check_mk_agent
    only_from      = 127.0.0.1 80.67.169.12
    log_on_success 
    }

> penser à changer l'adresse 80.67.169.12 lorsque Nagios aura migré autre part

Redémarrer xinetd pour prendre les modifications en compte

	service xinetd restart

### Ajout de sondes sur l'agent
TODO

### En automatique:
Puppet gère l'installation de check_mk, xinetd ainsi que la configuration d'xinetd, rien à faire dans ce cas.

# Coté serveur (Master)
Afin d'automatiser la création de monitoring pour les nouvelles machines, un module check_mk a 
été ajouté:

	/srv/puppet/environments/production/modules/check_mk/manifests/agent.pp
	class check_mk::agent {
	
 	 package { ['check-mk-agent', 'xinetd']:
  	  ensure => present,
	  } ->
 	 file { '/etc/xinetd.d/check_mk':
   	 ensure => file,
   	 source => "puppet:///modules/${module_name}/xinetd.d/check_mk",
   	 owner  => 'root',
  	  group  => 'root',
   	 mode   => '0444',
 	 } ~>
  	service { 'xinetd':
   	 ensure    => running,
   	 enable    => true,
    	hasstatus => false,
   	 pattern   => '/usr/sbin/xinetd',
 	 }
	
	}

**Pour l'instant, l'ajout d'une nouvelle machine nécessite de mettre à jour la liste des 
machines 
gérées par le Master dans /etc/check_mk/main.mk**

	all_hosts = [
	  "ackbar.fdn.fr",
 	 "c3px.fdn.fr",
 	 "chewie.fdn.fr",
  	"fdn2.fdn.fr",
 	 "gchq.fdn.fr",
 	 "jabber.fdn.fr",
  	"leia.fdn.fr",
 	 "lns11.fdn.fr",
 	 "lns22.fdn.fr",
 	 "nsa.fdn.fr",
  	"r4p17.fdn.fr",
  	"resolver0.fdn.fr",
  	"resolver1.fdn.fr",
  	"si.fdn.fr",
  	"solo.fdn.fr",
  	"vador.fdn.fr",
  	"vpn-open1.fdn.fr",
  	"vpn.fdn.fr",
  	"vpn1.fdn.fr",
  	"vpn2.fdn.fr",
	]

Afin de charger la nouvelle machine fraichement ajoutée dans le main.mk:
	
	check_mk -I

Pour charger la configuration et faire un reload de Nagios: 

	check_mk -O

### Changement des seuils par défaut (appliqués à toutes les machines)
Editer le fichier /etc/check_mk/conf.d/params.mk
Exemple pour augmenter le seuil du nombre de mails sur solo à un niveau Warning=500 et Critical=1000

	postfix_mailq_default_levels = (500, 1000) 

### Ajout d'un check spécifique & changement des seuils
Ajouter un fichier du nom de la machine.mk dans /etc/check_mk/conf.d/
Exemple d'ajout du monitoring de process Apache sur solo:
Critical si process<1 or process>50
Warning si process<3 or process>20

	checks += [
  	("solo.fdn.fr", "ps", "Apache", ("/usr/sbin/apache2", 1, 3, 20, 50)),
	]

# Commandes utiles côté serveur
Inventaire et ajout de nouveaux services

	check_mk -I

Compile, prise en compte de la configuration et reload de Nagios

	check_mk -O
