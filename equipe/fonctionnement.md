
# Fonctionnement groupe Adminsys

## Rejoindre l'équipe

Il y a plusieurs manières de s'impliquer dans FDN, l'une d'entre elles est de
rejoindre l'équipe adminsys. Cela peut paraître au premier abord très technique
mais l'ensemble des choses à y faire est au final assez divers. Cela va du
routage dynamique BGP à la maintenance de VM en passant par de l'animation du groupe.

- Voici la liste actuelle des membres du [groupe adminsys](./equipe_adminsys.md)
- Un guide des premières étapes en tant que [nouveau adminsys](./nouveau_membre_adminsys.md)

## Organisation

Le groupe adminsys est organisé en plusieurs niveaux.

Chaque niveau donne accès à un ensemble de droits dans l'infrastructure FDN.

Les niveaux s'organisent ainsi:

**Niveau Membre FDN:**

* Depuis le gitlab FDN, accès au groupe de projets **adminsys** en mode Reporter
* Vous pouvez commencer à prendre part aux échanges en ouvrant des Issues ou en en commantant d'autres

**Niveau AdminSys:**

* Vous avez le niveau Developper dans le groupe de projet **adminsys**
* Vous pouvez gérer vos propres projets:
 * Vous êtes Maintainer sur vos projets Gitlab
 * Vous êtes root sur la machaine associé

**Niveau AdminCore:**

* Avoir accès aux droides
* Accès aux VM sensibles (SI, LNS, ...)
* Créer de nouvelles VM
* Être admin sur gitlab
* Avoir son nom enregistré pour accéder aux DC

## Admincamps

Le plus facile pour s'intégrer à l'équipe adminsys est de venir à un admincamp.
Les admincamps sont des weekends lors desquels nous nous coordonnons et nous avançons concrètement dans une ambiance conviviale.

Il y a en a environ 4 à 6 par an.  Les admincamps sont annoncés sur les listes benevoles@fdn.fr et ag@fdn.fr et leurs dates sont généralement prévues au moins 6 mois à l'avance et publiées sur ce wiki. N'hésitez pas à vous annoncer si vous souhaitez y participer : `benevoles@fdn.fr`

## Pérennité dans les groupes

Être Adminsys ne se fait que sur des "mandats" renouvelables d'un an.

Avant chaque AG, il sera demandé de confirmer ou pas sa volonté et sa dispo.

En cas de non réponse ou si l'Admin exprime le fait d'avoir moins de temps, son AdminRank sera alors adapté à son implication.

## Documentation

Il y a une différence entre installer un logiciel chez soi, en mode standalone/one shot et faire tourner un service chez FDN. La mise en service d'un nouveau service nécessite qu'une documentation soit effecuée avant la proposition du service à nos adhérent·e·s.

Cette documentation doit se faire sur le git en rapport avec le projet sous la forme:

* buildbook : à destination des adminsys, pour remonter un services en cas de besoin et voir comment il a été monté à l'origine
* administration : à destination des adminsys, pour les actions courantes à effectuer sur le service (maj, ajout compte, etc.) et une FAQ
* utilisation : à destination des adhérents, des informations concernant le service et son utilisation au quotidien avec FAQ

C'est une étape indispensable afin que le service soit maintenu et que nos futur·e·s adminsys puissent prendre la main sur le service et comprendre l'historique.

Dans la mesure du possible, terminer la documentation sur le projet sur lequel on travaille avant d'en démarrer un autre.
