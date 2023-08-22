
# Généralités

Nous disposons de deux Nagios chez FDN.
Un premier non maintenu (voir le ticket [#5 de monitoring2.0](https://git.fdn.fr/adminsys/monitoring2.0/-/issues/5)) hébergé en interne (sur [cecinestpasleia](./machines/leia.md)) et un second gentiment hébergé à l'extérieur de l'infra de FDN sur skytop, une VM hébergée chez Grenode (voir [page dédiée](./outils_internes/supervision/remote_monitoring.md)).

Paramètres pour configurer votre widget Nagios préféré :

* *monitor URL* : http://cecinestpasleia.fdn.fr/nagios3
* *monitor CGI URL* : http://cecinestpasleia.fdn.fr/nagios3/cgi-bin
* *username* & *password* : défini dans l'htpassword sur leia dans */etc/nagios3/htpasswd.users*


