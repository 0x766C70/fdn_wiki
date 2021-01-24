# Système d'Information de FDN

Le SI de FDN est le système qui gère plusieurs aspects relatifs à l'organisation de FDN :

  * la liste des adhérents avec les informations relatives à leur compte « client »
  * les lignes ADSL et informations techniques liées
  * les tarifs des services, la gestion des créances, la génération des factures
  * la génération des prélèvements bancaires

Ne sont notamment pas gérés dans le SI

  * la comptabilité (base à part, archives sur http://compta.fdn.fr)
  * les configurations techniques autres qu'ADSL (web, ftp, uucp, news, etc.)

### Accès en consultation :
  - Le demandeur doit fournir un mot de passe au format htpasswd (disponible sur tout système ou apache2 est installé, dont solo.fdn.fr s'il ne l'a pas en local), que les administrateurs colleront à l'endroit qui va bien sur vador.
  - Le SI est accessible à cette adresse : https://vador.fdn.fr/private/
  - On peut chercher un utilisateur par son IP, puis en suivant les liens obtenir son courriel, ce qui peut servir pour transférer un rapport de plainte d'attaque par exemple 8-) Par contre, pour faire une recherche par adresse courriel, il faut le chercher dans la liste ag sur le Sympa 8-O
      - Pour le visualiser par le numéro qui suit ''adhacc-'' utiliser <code>https://vador.fdn.fr/private/view-client.cgi?cid=&do=yes</code> en plaçant le code après ''cid='' 8-)


### Défauts :
  - Le terme "clients" est horrible 8-O
  - Le terme "identifiant" est imprécis dans le formulaire de recherche (il y a au moins trois identifiants par personne chez FDN) 8-o

### Administration :
Les travaux de modification du SI sont organisés et suivi dans [[travaux:si|la page SI de la rubrique travaux]] (pour que cette page soit accessible a des non adminsys)



Voir les [[adminsys:si:howtos]] pour différentes taches.

