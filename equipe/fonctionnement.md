[[!meta title="Fonctionnement de l'équipe"]]

##Fonctionnement groupe Adminsys

Le groupe adminsys est organisé en plusieurs niveaux (ou AdminRank).

Chaque AdminRank donne accès à un ensemble de droits dans l'infrastructure FDN.

Être dans un des différents AdminRank, n'impose aucunement de vouloir passer à celui du dessus. Un AdminRookie peut par exemple très bien vouloir continuer avancer sur ses projets sans avoir à devenir adminSys.

Les niveaux s'organisent ainsi:

**Niveau AdminGuest (Période probatoire de 3 mois):**

* Accès à #adminsys (chan publique IRC)
* Compte gitlab Guest adminsys/suivi + accès à des projets précis en Guest
* Possibilité d'assister au Standup call mensuel du groupe
* Un adminGuest est parrainé par un AdminSys

**Niveau AdminRookie (AdminGuest actif + période probatoire de 3 mois + présence à un camp):**

* Être visible en tant qu'AdminGuest
* Accès au salon privé fdn-adminsys-internal sur [m]
* Possibilité de root sur des machines de tests
* Rank Dev sur gitlab
* Intégration au mailing adminsys@

**Niveau AdminSys (AdminRookie actif + période probatoire de 3 mois + 1 camp + qq bières IRL):**

* Possibilité de root sur des machines de prod de projets où iel a participé
* Rank Maintainer sur ses projets Gitlab
* Accompagner des nouveaux AdminGuest
* Possibilité de participer aux réunions de bureau comme porte parole du groupe

**Niveau AdminCore (être AdminSys actif + période probatoire de 3 mois + vote à la majorité sans veto des AdminCore):**

* Avoir accès aux droides
* Accès aux VM sensibles (SI, LNS, ...)
* Créer de nouvelles VM
* Être admin sur gitlab
* Avoir son nom pour accéder aux DC
* Participer aux orientations stratégico-techniques de l'asso

##Pérennité dans les groupes

Être Admin ne se fait que sur des "mandats" renouvelables d'un an.

Avant chaque AG, il sera demandé de confirmer ou pas sa volonté et sa dispo.

En cas de non réponse ou si l'Admin exprime le fait d'avoir moins de temps, son AdminRank sera alors adapté à son implication.

## Documentation

Il y a une différence entre installer un logiciel chez soi, en mode standalone/one shot et faire tourner un service chez FDN. La mise en service d'un nouveau service nécessite qu'une documentation soit effecuée avant la proposition du service à nos adhérent·e·s.

Cette documentation doit inclure:

* Les étapes d'installation
* Les étapes de configuration
* Les étapes de maintenance

C'est une étape indispensable afin que le service soit maintenu et que nos futur·e·s adminsys puissent prendre la main sur le service et comprendre l'historique.

Dans la mesure du possible, terminer la documentation sur le projet sur lequel on travaille avant d'en démarrer un autre.
