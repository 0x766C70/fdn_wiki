
FDN fournit une instance Mumble, mumble est le client disponible sur un grand nombre de plateformes (Linux, MacOS, F-Droid [Plumble]...)

# Mumble
## Côté adminsys
### Installation du serveur:
    sudo apt-get install mumble-server

### Configuration initiale
    dpkg-reconfigure mumble-server
    Autostart mumble-server on server boot? YES
    Allow mumble-server to use higher priority? YES
    Password to set on SuperUser account (dans GNUPass)

### Fichier de configuration (/etc/mumble-server.ini):
    Ajout des certificats Let's Encrypt
    defaultchannel=3 (Lobby)

### Start/Stop Mumble:
    systemctl stop mumble-server
    systemctl start mumble-server

### Logs
    /var/log/mumble-server/mumble-server.log

### SuperUser
En se connectant en SuperUser il est possible de crééer/gérer les salons avec les ACLs correspondants.

## Côté utilisateur
### Installation du client:
     apt-get install mumble
     Plumble (sur F-Droid)

### Configuration:
* Label: FDN
* Serveur: mumble.fdn.fr
* Port: 64738
* Username: `<votre utilisateur>`
* Password: AdminSysFDNUnderground
