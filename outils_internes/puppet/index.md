# Introduction

Nous utilisons actuellement [Puppet](https://fr.wikipedia.org/wiki/Puppet) (puppet5) provenant des dépôt de puppetlabs.

`puppetserver` et `puppetdb` sont installés sur la machine palpatine qui leur est dédiée.

Sur chaque serveur l'agent puppet est installé à partir des dépôts de la distribution pour simplifier l'administration.

La configuration puppet est stockée dans deux dépôts :
- `palpatine.fdn.fr:/srv/puppet/users.git` pour la gestion des accès (administration des serveurs) cf. [doc](users.md)
- `palpatine.fdn.fr:/srv/puppet/fdn.git` pour la configuration des serveurs cf. [doc](fdn.md)

Voir la [documentation](https://puppet.com/docs/) officielle pour en savoir plus sur Puppet.
