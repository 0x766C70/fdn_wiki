# Service Web

Le service web est hébergé sur [[adminsys:serveurs:yoda|yoda]]. Il fait actuellement l'objet d'un gros travail de migration et de nettoyage comme présenté [[travaux:maj_de_yoda_et_menage|ici]].

## Configuration

Dans les grandes lignes

### modules activés

### sites déclarés
|              ^ contact ^ HTTPS ^ Listen ^ configuration ^ remarques ^
^ [[http://blog.fdn.fr|blog.fdn.fr]] | bureau@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/blog | Je ne comprend pas trop cette regle; ne va-t-on pas risquer de rediriger des requetes HTTPS vers HTTP ? ''RewriteRule ^/(post.*)$ http://blog.fdn.fr/?$1 [QSA,L]'' |
^ [[http://compta.fdn.fr|compta.fdn.fr]] | tresorier@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/compta |  |
^ [[http://howto.fdn.fr|howto.fdn.fr]] | bureau@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/howto |  
^ [[http://news.fdn.fr|news.fdn.fr]] | newsmaster@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/news |  |
^ [[http://usenet-fr.fdn.fr|usenet-fr.fdn.fr]] | newsmaster@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/usenet-fr |  |
^ [[http://wiki.fdn.fr|wiki.fdn.fr]] | webmaster@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/wiki | Redirigé de façon permanente vers https://vador.fdn.fr/wiki |
^ www.fdn.fr | webmaster@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/inc/www-common | ce site est activé depuis /etc/apache2/sites-available/fdn/www. Le SSL pour l'ensemble des sites est géré ici avec les regles de rewriting |
^ www.fdn.fr/~user |  | OUI | *:80, 80.67.169.18:443 | /etc/apache2/sites-available/fdn/www | HTTP pointe vers WWW et HTTPS vers WWWS dans le répertoire de l'utilisateur, Les certificats SSL sont déclarés ici |
^ [[http://www.fdn2.org|www.fdn2.org]] | bureau@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/fdn2 |  |
^ [[http://x.fdn.fr|x.fdn.fr]] | bureau@fdn.fr | NON | *:80 | /etc/apache2/sites-available/fdn/x |  |




### répertoires utilisé

#### Configuration globale
  * **/etc/apache2/conf.d/** : ce répertoire contient des fichiers de configuration qui sont appliquées à l'ensemble du service apache.
#### Gestion des sites

répertoire racine de l'ensemble des sites disponibles 

  * **/etc/apache2/sites-available/** : répertoire contenant l'ensemble des site disponibles pour le service apache.
  * **/etc/apache2/sites-available/autres/** : répertoire contenant les fichiers de configuration de sites "autres" :)
  * **/etc/apache2/sites-available/fdn/** : répertoire dédié aux fichiers de configuration des sites de l'association (et également des sites en www.fdn.fr/~user/)
  * **/etc/apache2/sites-available/membres/** : répertoire dédié aux fichiers de configuration des sites des membres ayant un VirtualHost dédié. Chaque membre dispose d'un répertoire nominatif contenant les différents VirtualHost qu'il gère.

	/etc/apache2/sites-available/membres/
	├── username
	│   └── www.domain.net

Voir [[adminsys:gestionwebadherents|ici]] pour le détail sur la gestion de l'espace web d'un adhérant.

Pour activer un site il faut utiliser la commande a2ensite (a2dissite pour désactiver) puis recharger le service apache2. Une fois le site activé on observe qu'un lien symbolique est créé dans le répertoire **/etc/apache2/sites-enabled/** :
	yoda:~$ ls -l /etc/apache2/sites-enabled/fdn/
	lrwxrwxrwx 1 root root 37  8 mai    2011 blog -> /etc/apache2/sites-available/fdn/blog
	lrwxrwxrwx 1 root root 39  8 mai    2011 compta -> /etc/apache2/sites-available/fdn/compta
	lrwxrwxrwx 1 root root 37  8 mai    2011 fdn2 -> /etc/apache2/sites-available/fdn/fdn2
	...


#### Gestion des modules

L'ensemble des modules disponibles est présent dans le répertoire **/etc/apache2/mods-available/**

Pour activer un module on utilise a2enmod (a2dismod pour désactiver) puis recharger le service apache2. Une fois le site activé on observe qu'un lien symbolique est créé dans le repertoire /etc/apache2/mods-enabled/ :

### SSL

La gestion du SSL est mise en œuvre avec une règle de réécriture positionnée dans le fichier de configuration /etc/apache2/sites-available/fdn/inc/www-common permettant à l'ensemble des sites déclarés de disposer du SSL (j'ai un p'tit doute sur le fait qu'il s'agisse de la configuration désirée).

C'est donc un unique certificat avec un Common Name à *.fdn.fr qui est utilisé pour l'ensemble des sites faisant appel à SSL.

il s'agit de la déclaration suivante :
	#
	# Redirections https
	#
	RewriteEngine on
	RewriteCond %{HTTPS}    !^on$
	...
	RewriteRule ^(.*)$      https://%{SERVER_NAME}$1        [R=permanent,L]

La déclaration des certificats est quant à elle faite dans le fichier ainsi :
	SSLEngine On
	SSLCertificateFile /etc/ssl/private/star.fdn.fr.crt
	SSLCACertificateFile /etc/ssl/private/star.fdn.fr.chain
	SSLCertificateKeyFile /etc/ssl/private/star.fdn.fr.key
	SSLCaCertificatePath /etc/ssl/certs	

NOTE : La règle de réécriture active le SSL pour n'importe quel site du moment qu'il est déclaré. hors il n'y a pas de déclarations _default_. Cela implique que si un VirtualHost ne dispose pas d'une entrée explicite pour le SSL, alors l'utilisateur est redirigé vers le premier site déclaré. exemple : https:*howto.fdn.fr redirige sur https:*blog.fdn.fr


### Gestion des logs
#### FDN
Les logs relatifs aux sites FDN sont stockés ici :
	/var/log/apache2/
Nous en sommes à une période de 196 jours de rétention et le volume est donc susceptible de relativement augmenter.
	$ du -sh /var/log/apache2/
	520M	/var/log/apache2/
on trouve également les traces des sites n'ayant pas fixés leur propre gestion de logs. ces dernières sont stockées dans des fichiers other_vhosts_access.log.


la rotation de l'ensemble des fichiers *.log contenue dans le repertoire /var/log/apache2/ est assurée ici :
	yoda:~$ cat /etc/logrotate.d/apache2
	/var/log/apache2/*.log {
		daily
		missingok
		rotate 370
		compress
		delaycompress
		notifempty
		create 640 root www-data
		sharedscripts
		postrotate
			/etc/init.d/apache2 reload > /dev/null
		endscript
	}

#### Membres
Pour les sites des membres; les traces sont déclarées dans chacun des VirtualHost. La règle pour le moment semble être la suivante :
/home/username/log/errors-www.domain.com.log

Pour le moment l'ensemble des traces de tous les utilisateurs est géré par le fichier /etc/logrotate.d/apache-ssl
	yoda:~$ cat /etc/logrotate.d/apache-ssl 
	/home/agomes/log/access-www.fourmis-acidulees.fr.log /home/agomes/log/errors-www.fourmis-acidulees.fr.log /home/ahulin/log/access-www.cartophilie-viroflay.org.log /home/ahulin/log/access-www.hulin.net.log /home/ahulin/log/access-www.labourhakan.org.log /home/ahulin/log/error-www.cartophilie-viroflay.org.log /home/ahulin/log/error-www.hulin.net.log /home/ahulin/log/error-www.labourhakan.org.log /home/arenevier/annelaure/log/access-alaure.renevier.net.log /home/arenevier/annelaure/log/errors-alaure.renevier.net.log /home/arenevier/thomas/log/access-thomas.renevier.net.log /home/arenevier/thomas/log/errors-thomas.renevier.net.log /home/arpajon/log/access-www.arpajon.fdn.fr.log /home/arpajon/log/error-www.arpajon.fdn.fr.log /home/aschmitt/log/access-www.as-ci.net.log /home/aschmitt/log/access-www.freefoundation.org.log /home/aschmitt/log/access-www.gratin.org.log /home/aschmitt/log/access-www.infiniteCD.org.log /home/aschmitt/log/access-www.puppetpresident.net.log /home/aschmitt/log/access-www.TheBit.org.log /home/aschmitt/log/errors-www.as-ci.net.log /home/aschmitt/log/errors-www.freefoundation.org.log /home/aschmitt/log/errors-www.gratin.org.log /home/aschmitt/log/errors-www.infiniteCD.org.log /home/aschmitt/log/errors-www.puppetpresident.net.log /home/aschmitt/log/errors-www.TheBit.org.log /home/avauquel/log/access-www.guzzilande.fdn.fr.log /home/avauquel/log/errors-www.guzzilande.fdn.fr.log /home/cpaulus/log/access-www.calife.org.log /home/cpaulus/log/access-www.quesaco.org.log /home/cpaulus/log/errors-www.calife.org.log /home/cpaulus/log/errors-www.quesaco.org.log /home/dchampeimont/log/access-aikidojodobures.fdn.fr.log /home/dchampeimont/log/errors-aikidojodobures.fdn.fr.log /home/fpargami/log/access-www.abyara.org.log /home/fpargami/log/errors-www.abyara.org.log /home/hgbamy/log/access-www.zzsmiley-family.fdn.fr.log /home/hgbamy/log/errors-www.zzsmiley-family.fdn.fr.log /home/jblamy/log/access-laterrevuedailleurs.fdn.org.log /home/jblamy/log/errors-laterrevuedailleurs.fdn.org.log /home/jcrobert/log/access-www.jcrobert.com.log /home/jcrobert/log/error-www.jcrobert.com.log /home/jybarthel/log/access-www.aquapassion.org.log /home/jybarthel/log/error-www.aquapassion.org.log /home/mherinx/log/access-johannespoteries.eu.org.log /home/mherinx/log/access-www.suna.fdn.fr.log /home/mherinx/log/errors-johannespoterie.eu.org.log /home/mherinx/log/errors-www.suna.fdn.fr.log /home/picnat/log/access-picardie-nature.org.log /home/picnat/log/error-picardie-nature.org.log /home/sdescarp/log/access-sdescarp.fdn.fr.log /home/sdescarp/log/errors-sdescarp.fdn.fr.log /home/svallerot/log/access-as31576.geix.net.log /home/svallerot/log/access-ether.geix.net.log /home/svallerot/log/access-geix.net.log /home/svallerot/log/access-group.passworld-solidaire.org.log /home/svallerot/log/access-lulu.gixe.net.log /home/svallerot/log/access-peering.geix.net.log /home/svallerot/log/access-remote.geix.net.log /home/svallerot/log/access-vallerot.fr.log /home/svallerot/log/access-www.gixe.net.log /home/svallerot/log/errors-as31576.geix.net.log /home/svallerot/log/errors-ether.geix.net.log /home/svallerot/log/errors-geix.net.log /home/svallerot/log/errors-group.passworld-solidaire.org.log /home/svallerot/log/errors-lulu.gixe.net.log /home/svallerot/log/errors-peering.geix.net.log /home/svallerot/log/errors-remote.geix.net.log /home/svallerot/log/errors-vallerot.fr.log /home/svallerot/log/errors-www.gixe.net.log /home/teleplaisance/log/access-www.teleplaisance.org.log /home/teleplaisance/log/errors-www.teleplaisance.org.log /home/ykerbiriou/log/access-www.auvr.fdn.fr.log /home/ykerbiriou/log/errors-www.auvr.fdn.fr.log /var/log/apache-ssl/access-blog.fdn.fr.log /var/log/apache-ssl/access-compta.fdn.fr.log /var/log/apache-ssl/access-ffdn.org.log /var/log/apache-ssl/access-howto.fdn.fr.log /var/log/apache-ssl/access.log /var/log/apache-ssl/access-news.fdn.fr.log /var/log/apache-ssl/error.log /var/log/apache-ssl/errors-blog.fdn.fr.log /var/log/apache-ssl/errors-compta.fdn.fr.log /var/log/apache-ssl/errors-ffdn.org.log /var/log/apache-ssl/errors-howto.fdn.fr.log /var/log/apache-ssl/errors-news.fdn.fr.log /var/log/apache-ssl/ssl.log  {
	daily
	missingok
	rotate 370
	compress
	delaycompress
	notifempty
	create 640 root www-data
	sharedscripts
	postrotate
	   if [ -f /var/run/apache-ssl.pid ]; then \
	     if [ -x /usr/sbin/invoke-rc.d ]; then \
		invoke-rc.d apache-ssl stop > /dev/null ; \
		sleep 5; \
		killall -q -9 apache-ssl ; \
		invoke-rc.d apache-ssl start > /dev/null ; \
	     else \
	        /etc/init.d/apache-ssl stop > /dev/null ; \
		sleep 5; \
		killall -q -9 apache-ssl ; \
	        /etc/init.d/apache-ssl start > /dev/null ; \
	     fi; \
	   fi;
	endscript
	}
ATTENTION : le script logrotate embarque à la fois les traces sites en SSL gérés par FDN ainsi que les traces des sites membres (qu'ils soient en SSL ou pas)

NOTE : si le choix de la syntaxe actuelle n'est pas volontaire, il est possible dans un premier temps et pour alléger le fichier d'employer la syntaxe suivante :
	/home/*/log/errors-*.log
	/home/*/log/access-*.log
On s'épargne un paquet de ligne. Par contre, on pert en traçabilité et il est possible d'embarquer des choses non souhaitées.

De plus il est apparemment inutile de conserver toutes les directives pointant vers le repertoire /var/log/apache-ssl/ ce dernier n'existant plus.
	yoda:~$ ls -l /var/log/apache-ssl/
	ls: impossible d'accéder à /var/log/apache-ssl/: Aucun fichier ou dossier de ce type
