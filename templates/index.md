## Modèle de service/infra

### Utilité

Modèle à suivre autant que faire se peut pour de nouveaux services ou outils internes.

L'objectif est non seulement d'avoir ce qui s'approcherait d'un standard, pour améliorer la lisibilité de cette doc, mais également de ne rien oublier lors de la mise en place d'un nouveau service.

### Mise en place

Idéalement créer un ticket puis une MR associée ;)

1. copier le répertoire *templates/service* : `cp -R templates/service services/mon_service`
1. mettre à jour le fichier *services/mon_service/utilisation.md* : fichier à destination des adhérents pour décrire le service ainsi qu'une FAQ adhérent
1. mettre à jour le fichier *services/mon_service/administration.md* : fichier à destination des adminsys pour détailler le service d'un point vue technique et opérationnel, ainsi qu'une FAQ adminsys
1. mettre à jour le fichier *services/mon_service/buildbook.md* : fichier à destination des adminsys expliquant l'installation et la configuration initiale du service
