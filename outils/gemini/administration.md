# Administration du service

> À destination des adminsys : comment adminsitrer le service

## Caractéristiques VM

* 2 cores
* 1GB RAM
* /var/ de 10GB

## Administration

### Tâches spécifiques

Suivre les updates du repo

### Logs

`grep gemini /var/log/syslog`

### Base de données

N/A

### Sauvegarde

Les datas de la capsule sont stockées dans:

* /srv/gemini/content/

Les datas sont placées dans le repo:

* https://git.fdn.fr/communication/capsule

### En cas de pépins

`sudo systemctl status gemini.service`
