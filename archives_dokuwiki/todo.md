# Todo-List Admin-Sys

Pour avoir plus de détails sur une tâche, demandez sur la liste adminsys (ou sur #fdn-adminsys).

Consultez également le [[https://support.fdn.fr|bug tracker]]

## Documentation à produire :
__Wiki :__
  * Documenter la gestion des utilisateurs et des permissions. Note de Stéphane: J'ai créé [[adminsys:gestiondesutilisateurs|La gestion manuelle des utilisateurs]]
  * Documenter la mise à jour de dokuwiki. Documentation officielle disponible [[http://www.dokuwiki.org/install:upgrade|ici]] concernant la mise à niveau de cet outil.


## vieilleries à trier (fait ou pas, toujours d'actualité ou pas, etc.)

  * <del>**[20090422 baronchon]** bind: toutes les zones "slaves" _doivent_ être dans /var/cache/bind et pas dans /etc/bind</del> (fait)
  * **[20090422 baronchon]** bind: virer toutes les vieilles zones inutilisées (confirmer auprès des dinos de FDN et du SI) sur vador (slave) et leia (master)

  * **[2008xxxx jcd]** passage pour sympa de mod_fastcgi (non-free) à mod-fcgid main.

  * <del>**[2008xxxx domi, tom]** paquet l2tpns propre avec les patches de domi + dépôt sur edgard + preferences apt</del> (dépôt sur leia ?)

## Choses à faire et idées en vrac

  * web sur yoda: supprimer les comptes et site inutiles (cf /home/olb/bin/check-dns)
  * web sur yoda: formaliser l'emplacement des log d'apache pour les membres, vérifier que c'est respecté et modifier la conf de logrotate pour enfin supprimer le fichier /etc/logrotate.d/apache-ssl (qui fait peur)
  * web sur yoda: vérifier la conf d'awstats
  * web sur yoda: cloisonner les sites web à l'aide de la directive AssignUserId (se poser la question des cgi exécuter en www-data dans les répertoires WWW et WWWS des membres.
  * web sur yoda: faire le point sur les accès (FTP, SSH, ...) 
  * web sur yoda: IPv6: <del>dupliquer la config IPv4 (ça concerne uniquement les virtual hosts HTTPS, pour le reste tout se passe sur *:80 et ça doit déjà marcher), tester tout ça, mettre le DNS à jour.</del> Ce qui risque de coincer : le contrôle d'accès par IP (va falloir auditer tous les ''.htaccess'') (NdNono: rien vu dans les ''.htaccess'', j'espère ne pas en avoir raté), <del>tous les bouts de code PHP qui manipulent des adresses IP (là, pas de miracle, faut demander aux gens s'il y a des risques sur leurs sites)</del>.
  * <del>yoda: faire le point sur les ip utilisée (et supprimer celles qui sont inutiles).</del>
  * FAQ "comment entrer dans le groupe adminsys"
  * <del>FAQ adminsys "comment créer **les** accès pour un nouvel adminsys"</del>

  * installer et faire vivre un système de gestion de tickets (un Flyspray a été installé par vinci accessible sur [[https://support.fdn.fr]])
  * convertir cette todo-list en autant de tickets que nécessaire

  * mises à jour et suivi dokuwiki (et doc des modifs FDN)
  * passerelle dokuwiki <-> SVN, ou au moins dokuwiki -> SVN, ou bien dokuwiki -> feed RSS [ -> mail ]

  * gros ménage dans les comptes UUCP et feed de news qui ne servent plus
  * envisager sérieusement Puppet (ou équivalent), au moins pour sshd_config, ~root/.ssh/authorized_keys, sudoers, sources.list, etc. (20110920: c'est en cours, voir [[adminsys:puppet|Puppet]])

  * bind: utiliser mieux la séparation named.conf / named.conf.local ("propreté")

  * postfix: <del>entre postgrey et postfix-policymachin, prendre une décision et s'y tenir</del> policyd juste marche sur solo + vérifier la cohérence des MX
  * trouver une solution anti-spam pour bureau@ (problème complexe, cf. précédentes discussions sur bureau@ et ailleurs)

  * <del>cron-apt pour les mises à jour de sécurité ?</del>

  * Faire fonctionner MLPPP.
