
L'ensemble des services fournis au public ou aux membres. Les outils internes,
tels que les backups ou la supervision, sont documentés dans la section
[[outils]].


## État des services FDN

Les différentes colonnes correspondent aux questions suivantes :

|Colonne      | Signification
|-------------|----------------------------------------
| Date        | Date à laquelle on établit l'état du service.
| Prioritaire | Est-ce que le service est prioritaire pour FDN (par son activité, pour une raison politique...) ?
| Fonctionnel | Est-ce que le service est fonctionnel, au sens où "ça marche" aujourd'hui ?
| Maintenu    | Est-ce que le service est maintenu, sur du long terme (pas en mode pompier), par des personnes identifiées ?
| Réparable   | Est-ce que si le service tombe en panne demain, on est en mesure de réparer rapidement (mode pompier) ?
| ToDo        | Est-ce qu'il y a du travail identifié, en attente, à faire sur ce service pour l'améliorer (sécurité, nouvelles fonctionnalités...) ?


### Accès à Internet pour les abonné·e·s

| Service          | Date    | Prioritaire | Fonctionnel | Maintenu | Réparable | ToDo | Commentaires
|------------------|:-------:|:-----------:|:-----------:|:--------:|:---------:|:----:|---
| ADSL             | 2016-08 | oui         | oui         | plutôt   | oui       | oui  | Il faut mettre en place la collecte Liazo.
| VPN              | 2016-08 | oui         | oui         | oui      | oui       | non  | 
| RTC (abonné·e)   | 2016-08 | non         | oui         | non      | non       | non  | Les accès RTC avec login perso, ça marche, mais pas avec l'IP fixe.
| VPN événementiel | 2016-08 | oui         | oui         | oui      | oui       | non  | Routage de blocs IP sur un VPN pour des événements. On s'en sert régulièrement.


### Services ouverts au public

| Service          | Date    | Prioritaire | Fonctionnel | Maintenu | Réparable | ToDo | Commentaires
|------------------|:-------:|:-----------:|:-----------:|:--------:|:---------:|:----:|---
| RTC (public)     | 2016-08 | ???         | non         | non      | ???       | oui  | Du ressort de NNX. Voir ce qu'on fait de ce service ?
| DNS ouvert       | 2016-08 | oui         | oui         | oui      | oui       | oui  | Il y a un gros travail à faire sur le rate-limit (et sa documentation). Reste encore du taf sur la séparation des serveurs faisant autorité des serveurs récursifs.
| VPN openbar      | 2016-08 | oui         | oui         | oui      | oui       | oui  | Documentation et communication à terminer. Modèle de financement de la bp ? Ouvrir la bp à plus que 1Mbps ?


### Sites web publics

| Service          | Date    | Prioritaire | Fonctionnel | Maintenu | Réparable | ToDo | Commentaires
|------------------|:-------:|:-----------:|:-----------:|:--------:|:---------:|:----:|---
| www.fdn.fr       | 2016-08 | oui         | oui         | ???      | oui       | oui  | Contenu à compléter. Maintenance : qui fait les mises à jour de wordpress ?
| www.fdn2.org     | 2016-08 | oui         | oui         | ???      | oui       | oui  | Transféré sur chewie en statique. Comment les bénévoles peuvent éditer le contenu ?
| blog.fdn.fr      | 2016-08 | oui         | oui         | non      | oui       | oui  | À transférer sur chewie. Qui fait les mises à jour de dotclear ? Modifs sales pour le spam empêchent de mettre à jour ? 
| media.fdn.fr     | 2016-08 | oui         | oui         | oui      | oui       | oui  | Projet de mediakit ? Faire une jolie page web avec les liens direct et torrent ?
| www.open.fdn.fr  | 2016-08 | oui         | non         |          |           | oui  | En cours de réalisation. Site explicatif pour le vpn openbar.
| isengard.fdn.fr  | 2016-08 | non         | non         | oui      | oui       | oui  | En cours de réalisation. Mire pour les services FDN.
| wikileaks.fdn.fr | 2016-08 | non         | oui         | non      | ???       | oui  | Miroir wikileaks. À couper ou à mettre à jour, c'est selon. À priori plutôt couper.


### Services pour les membres

| Service          | Date    | Prioritaire | Fonctionnel | Maintenu | Réparable | ToDo | Commentaires
|------------------|:-------:|:-----------:|:-----------:|:--------:|:---------:|:----:|---
| Mail             | 2016-08 | non (+)     | oui         | non      | oui       | oui  | Il faudrait reconstruire une infra mail cohérente, en changeant quelques technos. Réel besoin d'avoir un antispam correct. Actuellement niveau de sécurité moyen. Webmail ?
| Mailing-lists    | 2016-08 | non (+)     | oui         | ???      | oui       | oui  | À intégrer à la future plateforme de mail.
| Web mutualisé    | 2016-08 | non (-)     | oui         | non      | ???       | oui  | Couper le service tel qu'existant. Proposer des pages perso statiques aux abonné·e·s. Renvoyer vers d'autres structures ou une VM pour des besoins plus larges (cgi, php, mysql...).
| DNS (pri/sec)    | 2016-08 | non (+)     | oui         | oui      | oui       | oui  | A fait l'objet d'un gros travail (nettoyage, git-ification...). Reste à finir la séparation authoritatives / recursives.
| Jabber           | 2016-08 | non (-)     | oui         | non      | ???       | oui  | Service fonctionnel mais non maintenu. Supervision ? On sait qu'il y a du spam dessus, problème non traité. Qui s'en occupe ?
| Tracker torrent  | 2016-08 | non (-)     | oui         | non      | ???       | ???  | Est-ce qu'il sert ? Qui s'en occupe ? Où est-ce installé (si c'est leïa, il faut le déplacer).
| NewsGroups       | 2016-08 | non (??)    | ???         | non      | ???       | ???  | Service non maintenu. Potentiellement à moitié fonctionnel (blocs IP en écriture pas à jour ?). Des demandes en attente. Qui s'en occupe ? Est-ce qu'on ferme le service (objet de l'asso, usenet...) ?
| x.fdn.fr         | 2016-08 | oui         | oui         | non      | oui       | oui  | Raccourcisseur d'URL. Utilisé pour la com et publication (exégètes). À nettoyer, et ranger sur chewie ?




