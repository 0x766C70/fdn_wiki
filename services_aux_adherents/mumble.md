# Mumble

FDN fournit une instance Mumble, un logiciel de téléphonie sur IP libre et open-source disponible sur de nombreuses plateformes (Linux, macOS, Windows, Android via F-Droid [Plumble]...).

- **Serveur** : mumble.fdn.fr
- **Port** : 64738

## Côté adminsys

### Installation du serveur

```bash
sudo apt-get install mumble-server
```

### Configuration initiale

```bash
dpkg-reconfigure mumble-server
```

Répondre aux questions :

- **Autostart mumble-server on server boot?** YES
- **Allow mumble-server to use higher priority?** YES
- **Password to set on SuperUser account** : (stocker dans GNUPass)

### Fichier de configuration

Le fichier de configuration principal est `/etc/mumble-server.ini` :

```ini
# Certificats Let's Encrypt
sslCert=/etc/letsencrypt/live/mumble.fdn.fr/fullchain.pem
sslKey=/etc/letsencrypt/live/mumble.fdn.fr/privkey.pem

# Salon par défaut (Lobby)
defaultchannel=3
```

### Gestion du service

```bash
systemctl status mumble-server
systemctl start mumble-server
systemctl stop mumble-server
systemctl restart mumble-server
```

### Logs

```
/var/log/mumble-server/mumble-server.log
```

### SuperUser

En se connectant en SuperUser (via le client Mumble avec le nom d'utilisateur `SuperUser` et le mot de passe stocké dans GNUPass), il est possible de créer et gérer les salons ainsi que leurs ACLs.

Pour se connecter en SuperUser depuis le client Mumble :

1. Aller dans **Serveur** > **Se connecter**
2. Saisir `SuperUser` comme nom d'utilisateur
3. Entrer le mot de passe SuperUser (cf. GNUPass)

### Gestion des ACLs

Les ACLs permettent de gérer les droits d'accès aux salons. Pour modifier les ACLs d'un salon :

1. Faire un clic droit sur le salon > **Éditer**
2. Onglet **Groupes** : gérer les groupes d'utilisateurs
3. Onglet **ACL** : définir les permissions par groupe

Permissions courantes :

- `Traverser` : accéder au salon (nécessaire pour entrer dans les sous-salons)
- `Entrer` : rejoindre le salon
- `Parler` : prendre la parole
- `Chuchoter` : chuchoter à des utilisateurs spécifiques
- `Écrire les ACLs` : modifier les permissions

### Troubleshooting

- Vérifier les logs : `tail -f /var/log/mumble-server/mumble-server.log`
- Vérifier que le service tourne : `systemctl status mumble-server`
- Vérifier que le port est ouvert : `ss -tlnp | grep 64738`

## Côté utilisateur

### Clients disponibles

| Plateforme | Client   | Source                                                        |
|------------|----------|---------------------------------------------------------------|
| Linux      | Mumble   | `apt-get install mumble` ou gestionnaire de paquets           |
| Windows    | Mumble   | [mumble.info](https://www.mumble.info/)                       |
| macOS      | Mumble   | [mumble.info](https://www.mumble.info/)                       |
| Android    | Plumble  | [F-Droid](https://f-droid.org/packages/info.mumble.plumble/) |
| iOS        | Mumblefy | App Store                                                     |

### Installation (Linux)

```bash
sudo apt-get install mumble
```

### Connexion au serveur FDN

Paramètres de connexion :

- **Label** : FDN
- **Serveur** : mumble.fdn.fr
- **Port** : 64738
- **Nom d'utilisateur** : `<votre login FDN>`
- **Mot de passe** : (demander à un adminsys)

### Configuration audio recommandée

- Activer la **suppression du bruit** pour améliorer la qualité audio
- Configurer le **push-to-talk** ou la **détection automatique de la voix** selon votre préférence
- Régler le **volume du microphone** via l'assistant de configuration audio de Mumble

### Premier lancement

Au premier lancement, Mumble propose un assistant de configuration audio :

1. Suivre l'assistant pour calibrer le microphone et les haut-parleurs
2. Configurer le push-to-talk si souhaité
3. Se connecter au serveur FDN avec les paramètres ci-dessus
