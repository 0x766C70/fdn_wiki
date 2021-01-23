__**Doc obsolète depuis que c'est géré automatiquement par le SI**__

# Ajout d'une plage IPv6 pour un abonné

Chaque abonné ADSL a droit à un préfixe /48 quand il demande une plage d'IPv6.

Le bloc IPv6 alloué aux ADSL par FDN est 2001:910:1000::/38 (pourquoi /38 ? parce qu'on a un /22 pour toutes les IPv4 ADSL, ce qui fait 10 bits pour adresser tous les abonnés, et comme on attribue un /48 par abonné, on obtient /48 - 10 = /38).

## Calculer le préfixe d'un abonné

Le bloc d'IPv4 alloué aux ADSL est 80.67.176.0/22. On va extraire la "différence" entre 80.67.176.0 et l'adresse IPv4 de l'abonné : par exemple, si l'abonné est 80.67.176.58, on obtient 0.0.0.58, ce qui donne 58, soit 3A en hexa. Autre exemple, si l'IP était plus loin, comme 80.67.178.42, ça serait 0.0.2.42, et donc, 2*256+42=445, soit 22A hexa.

On n'a plus qu'à ajouter ce nombre au préfixe IPv6 cité plus haut pour les ADSL (2001:910:1000::/38), et on obtient 2001:910:103a::/48 pour le 1er exemple, et 2001:910:122a::/48 pour le 2è.

Pour les feignants, ça donne :

  * façon Stéphane :

     perl -e 'sub ip2num { unpack "N", pack "C4", @_ }
      printf "2001:910:\%04x::/48\n", 0x1000 +
      ip2num(split /\./, shift)-ip2num(80,67,176,0);' \
      80.67.176.127

  * ou façon mat :

     ruby -ripaddr -e 'puts "2001:910:%04x::/48\n" % [0x1000 + (IPAddr.new(ARGV[0]).to_i - IPAddr.new("80.67.176.0").to_i)]' 80.67.176.127

## Activer le préfixe d'un abonné

Pour connaître l'adresse IPv4 d'un abonné, et pour "rentrer" son bloc IPv6, tout se fait dans le [[adminsys:si|SI]], qui va s'interfacer avec RADIUS pour extraire/introduire ces informations (l2tpns consulte RADIUS pour connaître les informations relatives à un abonné lors du login PPP).

Il faut pour cela trouver la ligne téléphonique concernée, soit en passant par la fiche de l'adhérant ("client" pour le SI) en entrant son numéro d'adhérant, puis en allant dans "Infos techniques", cliquer sur l'id de la ligne téléphonique conerncée, soit en entrant directement le numéro de la ligne si on le connaît.

Ensuite, on clique sur le compte radius associé, où on trouvera son IPv4. On fait le calcul de son IPv6, et on clique sur "Ajouter" dans Attributs de l'utilisateur. On entre dans les champs :

  * Nom de l'attribut    : Framed-IPv6-Route
  * Opérateur            : = (et pas := )
  * Valeur de l'attribut : 2001:910:10XX::/48
  * Type                 : reply
  * User id              : Ben, on le laisse, il était déjà bon.

Et voilà, à la prochaine connexion, le serveur radius va dire au serveur l2tp "tient, vla un autre attribut, faut mettre cette route ipv6 là vers ton client".

(texte majoritairement issu d'un email de mat 6BBCEE0BBA26CB543D0B064C@pouet.in.mat.cc)

## Voir aussi
L'entrée de la FAQ pour les utilisateurs d'[[support:faq:ipv6]].
