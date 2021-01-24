# Le mail chez FDN
## Mail entrant (MX)
Le nom « mail.fdn.fr » c'est le MX de fdn.fr
Le nom « smtp.fdn.fr » c'est le relai pour les utilisateurs
Dans le but de laisser disponible le service de relai quand le MX se
fait matraquer par des spameurs.

Le MX primaire est *mail.fdn.fr*, aka *[[adminsys:serveurs:solo]]*. C'est du Postfix tout ce qu'il y a de standard.
Il y a un MX de backup, *mx2.fdn.fr*, aka *[[adminsys:serveurs:leia]]*.
Une fois le mail arrivé, il peut être traité de pleins de façons suivant les désirs de chaque adhérent :
  * UUCP (voir [[adminsys:gestionuucpadherents|là]])
  * procmail
  * SMTP (simple forward, par exemple)
  * IMAP (Cyrus)
### Statistiques :
http://munin.fdn.fr/fdn.fr/solo.fdn.fr/postfix_mailstats.html

### Lutter contre les pourriels avec Policyd sur Solo :
  - Le fichier de configuration est ''/etc/postfix-policyd.conf'' 8-)
  - Pour se connecter à la base : ''mysql --user=postfix-policyd --password=u0lXAc9Vdcfm postfixpolicyd'' 8-O
#### Recharger la configuration :
  - ''sudo /etc/init.d/postfix-policyd reload'' 8-)
  - ''ps -C postfix-policyd'' afin de vérifier que le service tourne bien 8-O
#### Le spamtrap :
Il ne semble pas être utilisé, voici ce que la documentation en dit: \\
The spamtrap module should be very effective, especially in
really large environments. Previously baited spamtraps would
require that the mail actually enters the network and gets
delivered into a mailbox. Any attempted deliveries to any of
the spamtrap addresses will cause that host/net block to be
blacklisted for N amount of hours. Using the spamtrap module
the host gets blacklisted without having to accept or transfer
any mail so resources are kept to a minimum. \\

Spamtrap format: \\

    INSERT INTO spamtrap (_rcpt,_active) VALUES ('spam@trap.com', 1);
  
    1=active
    0=inactive (strictly for production purposes/testing)
#### Blacklist Helo :
Il est activé mais ne semble pas être configuré, voici ce que la documentation en dit : \\
The blacklist helo module allows you to blacklist hosts or
net blocks (c-class) who use HELO and attempt to identify
themselves using your own hostname/ip address. This will allow
you to quickly build up a list of known spammer networks.
This module is effective because its completely automated
and can be used to permanently ban networks even if they
stop identifying themselves with your hostnames at a later
stage.

    INSERT INTO blacklist_helo (_helo) VALUES ('192.168.0.2');
    INSERT INTO blacklist_helo (_helo) VALUES ('[192.168.0.2]');
    INSERT INTO blacklist_helo (_helo) VALUES ('localhost.machine.com');
    INSERT INTO blacklist_helo (_helo) VALUES ('localhost');
  
In order for this to work properly. You want to INSERT the
hostname of your machine, your MX hostname, your MX ip address
and the IP address of your machine (this includes virtual ips
that reside on your switch)

    NO REMOTE HOST SHOULD IDENTIFY THEMSELVES WITH YOUR MACHINES
    INFORMATION!
#### Liste noire des expéditeurs :
    INSERT INTO blacklist_sender (_blacklist,_description) \
      VALUES ('camis@mweb.co.za','# blacklist single address');
    INSERT INTO blacklist_sender (_blacklist,_description) \
      VALUES ('@mweb.co.za','# blacklist entire domain');

    Note: blacklisting @mweb.co.za will *not* blocklist subdomains
        like @subdomain.mweb.co.za.

### La lutte continue avec Postscreen sur Solo

Postscreen est un processus optionnel de Postfix destiné à filtrer les envahisseurs en amont, avant même que tout autre traitement n'aie lieu - le but étant d'éviter de charger inutilement le serveur avec du courrier indésirable.

Pour ce faire, différentes stratégies sont employées :

#### Tests pré-220

== Liste noire ==

Si l'on a une liste d'opportuns sous la main, on peut demander à Postscreen de les envoyer promener séance tenante. Exemple :

    <code>
    # mynetworks autorisé par défaut, le reste est traité dans une map.
    postscreen_access_list = permit_mynetworks, cidr:/etc/postfix/postscreen_access.cidr
    postscreen_blacklist_action = enforce
    </code>


Un exemple de map :

    <code>
    # Rules are evaluated in the order as specified.
    # Blacklist 192.168.* except 192.168.0.1.
    127.0.0.1       permit
    192.168.1.1     permit
    192.168.1.0/24  reject
    </code>


== Real-Time Blackhole Lists (RBLs) ==

Un grand classique mais pas du goût de tout le monde. Exemple :

    <code>
    postscreen_dnsbl_sites =
            zen.spamhaus.org*3
            bl.spameatingmonkey.net*2
            bl.spamcop.net
            dnsbl.sorbs.net
    postscreen_dnsbl_threshold = 5
    postscreen_dnsbl_action = enforce
    </code>


Ici, si le seuil dépasse 5, le mail sera rejeté. Les valeurs de Spamhaus comptent triple et celles de Spameatingmonkey double.

== Pre-Greet Banner ==

Ici, il s'agit d'une petite subtilité du protocole SMTP. La RFC spécifie que le serveur peut envoyer une bannière de bienvenue sur plusieurs lignes. Postscreen envoie une première ligne, attend 6 secondes puis envoie la suivante. Si le client se conforme au protocole, il attendra la dernière ligne pour parler. Un robot de spam ne s'encombrera pas de cela (son but étant d'envoyer le maximum de messages en un minimum de temps) et sera rejeté. Exemple :

    <code>
    postscreen_greet_banner = Que la Force soit avec toi
    postscreen_greet_action = enforce
    </code>


Ce que le serveur va faire :

    <code>
    $ telnet solo.fdn.fr 25
    Trying 2001:910:800::19...
    Connected to solo.fdn.fr.
    Escape character is '^]'.
    220-Que la Force soit avec toi
    [... attente de 6 secondes ...]
    220 solo.fdn.fr ESMTP Postfix (Debian/GNU)
    </code>


Le tiret après le premier 220 indique que la réponse est multi-lignes, le client doit attendre que le serveur aie fini de se présenter. Postscreen met ce temps à profit pour interroger les RBLs si elles ont été configurées.

#### Tests post-220

== Pipelining ==

Avant la publication de la norme ESMTP, SMTP était half-duplex - le client et le serveur parlaient chacun leur tour. Le pipelining permet lui au client d'envoyer un train de commandes. Postscreen ne supportant pas ESMTP, il n'enverra pas cette extension au client. Si ce dernier se conforme au protocole, il enverra donc ses commandes une par une en attendant la réponse du serveur entre chaque - là encore, un robot de spam ne s'occupera pas de ce que lui envoie le serveur et cherchera à délivrer son message le plus vite possible. Exemple :

    <code>
    postscreen_pipelining_enable = yes
    postscreen_pipelining_action = enforce
    </code>


== Commandes non-SMTP ==

Il s'agit ici de surveiller la présence de commandes CONNECT, GET ou POST dans le flux de connexion - typiquement employées par les robots de spam lorsqu'ils passent par des proxys. Un client légitime ne fera pas cela. Exemple :

    <code>
    postscreen_non_smtp_command_enable = yes
    postscreen_non_smtp_command_action = enforce
    </code>


== Bare newline test ==

Il s'agit là encore d'une subtilité du protocole SMTP qui impose que chaque ligne se termine par <CR><LF>. La plupart des robots de spam se contentent d'envoyer des <LF> et peuvent donc se faire jeter sans état d'âme. Exemple :

    <code>
    postscreen_bare_newline_enable = yes
    postscreen_bare_newline_action = enforce
    </code>


#### Greylisting

Si un client passe tous les tests, il se fera quand même rejeter par un 450. Ce n'est pas une erreur, le client est à ce stade sur une liste blanche. S'il se reconnecte dans la foulée (ce qu'un serveur légitime fera à la différence généralement des robots spammeurs), Postscreen passera cette fois la connexion directement au process smtpd pour le traitement "ordinaire" du courrier.

#### Actions

Dans les exemples ci-dessus, l'action enforce a toujours été utilisée. Cette dernière indique à Postscreen de rejeter la connexion au dernier moment, le but étant de faire perdre du temps au robot de spam (accessoirement, cela permet de voir à qui il aurait essayer de délivrer un message). Il en existe toutefois deux autres :
  * ignore : utile pour les tests, Postscreen se contente de logger l'évènement mais ne rejette pas le message
  * drop : clair, net et limpide - le client est jeté séance tenante.

#### Configuration

Les options souhaitées sont à ajouter dans le fichier main.cf. Il faut encore activer le process Postscreen dans master.cf :

    <code>
    ##smtp      inet  n       -       -       -       -       smtpd
    smtp      inet  n       -       -       -       1       postscreen
    smtpd     pass  -       -       -       -       -       smtpd  
    dnsblog   unix  -       -       -       -       0       dnsblog 
    tlsproxy  unix  -       -       -       -       0       tlsproxy
    </code>


... suivi d'un reload et le tour est joué. :-)

**Nota :** Attention dans le cas de Solo à laisser l'IP de smtp.fdn.fr exclue, sans quoi les adhérents ne peuvent plus utiliser leurs MUAs sur le port 25 !

## Mail sortant (SMTP)

Il s'agit (surprise !) de *smtp.fdn.fr*, aka *[[adminsys:serveurs:solo]]*, sur une autre adresse IP que pour le mail entrant. Toutefois, la possession d'un compte courriel est indispensable pour utiliser ce [[http://www.cdr-pays-brest.infini.fr/index.php/Clients_de_messagerie|MTA]]. Le compte permettra alors de s'identifier, quelque que soit l'adresse courriel d'expédition.
## Webmail

http://webmail.fdn.fr/

## Être MX secondaire pour le domaine d'un adhérent

    Sur *solo*, dans ''/etc/postfix/relay_domains'', ajouter la ligne <code>sondomaine.org OK</code> puis lancer la commande <code>postmap /etc/postfix/relay_domains</code>. Enfin, dire à l'adhérent qu'il peut modifier son DNS pour y ajouter *mail.fdn.fr* (et seulement ce nom-là) comme MX secondaire.

