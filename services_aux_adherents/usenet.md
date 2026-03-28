# Usenet / Newsgroups

FDN fournit un accès Usenet à ses adhérents via le serveur **news.fdn.fr**.
Usenet est un système de messagerie distribuée organisé en groupes de discussion
(newsgroups), fonctionnant selon le protocole NNTP (Network News Transfer Protocol).

- **Serveur** : news.fdn.fr
- **Port NNTP** : 119 (non chiffré) / 563 (NNTPS, chiffré)
- **Machine** : hébergé sur [solo](./infra/machines/solo.md)
- **Logiciel** : [INN](https://www.eyrie.org/~eagle/software/inn/) (InterNetNews)

## Côté utilisateur

### Accès

Le serveur `news.fdn.fr` est accessible **sans authentification** depuis toutes
les adresses IP FDN (xDSL, FTTH ou VPN). Depuis le reste du monde, il est accessible
en s'authentifiant avec ses identifiants xDSL ou VPN.

### Clients disponibles

| Plateforme | Client      | Source                                                         |
|------------|-------------|----------------------------------------------------------------|
| Linux      | Thunderbird | `apt-get install thunderbird` ou gestionnaire de paquets       |
| Linux      | slrn        | `apt-get install slrn` (client en ligne de commande)           |
| Linux      | tin         | `apt-get install tin` (client en ligne de commande)            |
| Windows    | Thunderbird | [thunderbird.net](https://www.thunderbird.net/)                |
| macOS      | Thunderbird | [thunderbird.net](https://www.thunderbird.net/)                |
| Android    | Groundhog   | [F-Droid](https://f-droid.org/) / Play Store                   |

### Connexion au serveur

Paramètres de connexion (exemple avec Thunderbird) :

- **Serveur** : `news.fdn.fr`
- **Port** : `563` (NNTPS, recommandé) ou `119`
- **Chiffrement** : SSL/TLS (recommandé)
- **Authentification** : non requise depuis les IPs FDN ; identifiants xDSL/VPN sinon
- **Nom d'utilisateur** : votre login FDN (sous la forme `login@fdn.fr`)

### Statistiques publiques

Un rapport quotidien est généré et disponible sur <http://news.fdn.fr/status/>.

## Côté adminsys

Infos supplémentaires dans [les archives](./archives/archives_dokuwiki/usenet.md).

### Configuration

Les fichiers de configuration d'INN se trouvent dans `/etc/news/` sur solo :

| Fichier                          | Rôle                                            |
|----------------------------------|-------------------------------------------------|
| `/etc/news/inn.conf`             | Configuration principale d'INN                  |
| `/etc/news/newsfeeds`            | Définition des feeds entrants et sortants       |
| `/etc/news/innfeed.conf`         | Configuration du feed NNTP sortant              |
| `/etc/news/incoming.conf`        | Configuration des feeds NNTP entrants           |
| `/etc/news/send-uucp.cf`         | Configuration des feeds UUCP                    |
| `/etc/news/users`                | Utilisateurs statiques (format `user:hash`)     |
| `/etc/news/ssl/`                 | Certificats SSL/TLS pour NNTPS                  |
| `/etc/news/filter/`              | Scripts CleanFeed (filtrage anti-spam)          |

### Gestion du service

```bash
systemctl status inn2
systemctl start inn2
systemctl stop inn2
systemctl restart inn2
systemctl reload inn2
```

Pour recharger la configuration sans redémarrer le service, on peut aussi utiliser
`ctlinnd` :

```bash
ctlinnd reload inn.conf "raison du rechargement"
```

### SSL/TLS

INN exige que la clé du certificat soit en mode `600` avec `news` comme seul
propriétaire. Les fichiers `.crt` et `.key` sont copiés dans `/etc/news/ssl/`.
Les chemins sont spécifiés dans `/etc/news/inn.conf` (section SSL en fin de fichier).

### CleanFeed (filtrage anti-spam)

Usenet est sujet au spam. CleanFeed est un ensemble de scripts Perl appliquant
des bonnes pratiques de filtrage. Il est installé dans `/etc/news/filter/`.
La configuration locale se trouve dans `/etc/news/filter/cleanfeed/etc/cleanfeed.local`.

Documentation de référence : <http://www.mixmin.net/cleanfeed/index.html>

Un rapport quotidien de CleanFeed est accessible sur <http://news.fdn.fr/status/cleanfeed.stats.html>.

### Ajout d'un feed NNTP

1. Éditer `/etc/news/newsfeeds` pour ajouter le feed sortant (prendre exemple
   sur les feeds existants). Ajouter en commentaire les informations de contact
   et l'identité de la personne ayant effectué la configuration côté FDN.
2. Éditer `/etc/news/innfeed.conf` pour le nom d'hôte du feed sortant.
3. Éditer `/etc/news/incoming.conf` pour le nom d'hôte du feed entrant.
4. Recharger la configuration :

```bash
ctlinnd reload newsfeeds "nom-du-feed"
ctlinnd reload incoming.conf nom-du-feed
```

### Ajout d'un feed UUCP

1. Éditer `/etc/news/newsfeeds` (prendre exemple sur un feed existant avec
   `nom-du-site::BUFFCHAN!` dans la première colonne).
2. Éditer `/etc/news/send-uucp.cf` pour ajouter le site concerné.
3. Recharger la configuration :

```bash
ctlinnd reload newsfeeds nom-du-site
```

### Modification d'un feed

Pour modifier la liste des groupes envoyés à un site, éditer `/etc/news/newsfeeds`
puis recharger :

```bash
ctlinnd reload newsfeeds nom-du-site
```

### Ajout d'utilisateur statique

Pour les adhérents qui n'ont pas d'accès xDSL/FTTH/VPN, on peut créer des comptes à la main.

Ajouter une ligne dans `/etc/news/users` sur solo au format `user:hash`,
avec le hash en sha512crypt généré par :

```bash
mkpasswd -m sha512crypt
```

Le login sera `user@fdn.fr` (vérifier l'absence de collision avec une adresse
mail existante d'un autre adhérent).

### Statistiques

Un rapport quotidien est envoyé à <usenet@fdn.fr> (groupe `adminsys`).
La version mise en forme est consultable sur <http://news.fdn.fr/status/>
(pas de login requis pour l'instant — ne pas diffuser ce lien publiquement pour
éviter que des logins d'adhérents soient indexés par les moteurs de recherche).

### Troubleshooting

- Logs INN : `/var/log/news/`
- Vérifier l'état du service : `systemctl status inn2`
- Vérifier la configuration : `inncheck`
- Vérifier les feeds actifs : `ctlinnd feedinfo *`
