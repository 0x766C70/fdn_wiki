# Ajouter une adresse IP supplémentaire pour un utilisateur :
## Qui doit s'en occuper ?


En réalité FDN n'est plus LIR.


Mais FDN et Gitoyen n'ont pas assez réfléchi la chose pour qu'elle fonctionne. Il y a une bonne manière de faire, c'est que Gitoyen délègue à FDN un bloc d'adresses dans 
lequel FDN jouera le rôle d'un LIR à la place de Gitoyen. C'est prévu,
du moins en ipv4, ça existe, ça s'appelle des adresses SUB-ALLOCATED.
Ça demande de la part de Gitoyen (faute d'avoir des idées sur la
manière de faire leur job, ou la réactivité utile) d'avoir confiance 
en FDN pour cette sous-traitance.


Pour cela,

ceux qui veulent se former au boulot de LIR, gérer avec les demandeurs
ce genre de demandes et agir dans Gitoyen, il faut faire un peu de lecture :

  - http://www.ripe.net/data-tools/support/documentation/ripe-database-fast-facts
  - http://www.ripe.net/data-tools/support/documentation/ripe-database-query-reference-manual
  - http://www.ripe.net/data-tools/support/documentation/update-ref-manual

  - http://www.ripe.net/internet-coordination/ipv4-exhaustion/faq
  - http://www.ripe.net/lir-services/resource-management/faq/resource-request
  - http://www.ripe.net/ripe/docs/ipv4-policies.html
  - http://www.ripe.net/lir-services/resource-management/contact/ipv4-evaluation-procedures

  - http://www.ripe.net/lir-services/resource-management/number-resources/ipv6
  - http://www.ripe.net/lir-services/resource-management/number-resources/ipv4
  - http://www.ripe.net/lir-services/resource-management/number-resources/as-numbers
  - http://www.ripe.net/data-tools/dns/reverse-dns

Et pour un accès général : http://www.ripe.net/db/docs.html

Il est également recommandé d'avoir quelques notions de routage (avec BGP v4).
## Procédure :
  - Les adminsys reçoivent les requêtes des adhérents qui prennent FDN pour leur LIR.
  - Le principe n'est pas d'attribuer un bloc, mais nous devons justifier l'utilisation des IP auprès de notre LIR, Gitoyen. Nous avons un bloc (80.67.176.0/22) qui est réservé pour les abonnés, mais une seule est autorisée par abonné dans ce bloc. Et
nous avons un autre bloc réservé pour ceux qui veulent plus d'IP, où
nous devons alors justifier auprès du RIPE pourquoi nous en donnons plus
à quelqu'un.

  - Ne pas confier le formulaire au demandeur,
car s'il n'est pas correctement rempli ça finira pas poser des problèmes à
Gitoyen et même au demandeur qui risque de se voir retirer ses IPs.

Selon Sylvain Vallerot: "Gitoyen est le LIR et donc Gitoyen doit traiter 
avec les utilisateurs finaux, c'est le travail d'un LIR."

Ensuite il faut se rapprocher de son LIR préféré pour obtenir des accès au
LIR Portal :
  - En général si la demande est assez petite pour que Gitoyen, notre LIR, n'ait
même pas besoin de demander son avis au Ripe, il fait donc les commit
dans le whois de son propre chef. S'agissant de PA, uniquement.
  - Gitoyen met alors à jour sa configuration pour affecter le bloc
  - Adminsys répond au demandeur
