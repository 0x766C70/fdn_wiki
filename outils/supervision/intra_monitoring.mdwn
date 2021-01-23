[[!meta title="Intra Monitoring"]]

# Généralités

Nous disposons de deux nagios chez FDN. Un premier hébergé en interne (sur leia) et un second gentiment hébergé à l'extérieur de l'infra de FDN sur isengard, une VM hébergée chez LDN (merci LDN, merci sebian, voir [page dédiée](/outils/supervision/remote_monitoring/)).

Paramètres pour configurer votre widget nagios préféré :

* *monitor URL* : http://leia.fdn.fr/nagios3
* *monitor CGI URL* : http://leia.fdn.fr/nagios3/cgi-bin
* *username* & *password* : défini dans l'htpassword sur leia dans */etc/nagios3/htpasswd.users*


