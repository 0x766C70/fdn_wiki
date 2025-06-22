# Construction du service

[[_TOC_]]

## Implémentation

### Installation du Keycloak

L'installation du service Keycloak se fait via Puppet, un [module](https://git.fdn.fr/adminsys/puppet/-/tree/production_gitlab/modules/keycloak) a été créé pour en gérer la configuration.

### Configuration du domaine

Le domaine par défaut `master` ne doit être utilisé que pour créer le ou les domaines nous avons besoin.

Dans notre cas, nous n'avons besoin que d'un seul domaine (fdn).


## FAQ
