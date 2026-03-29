Machine virtuelle (temporaire) d'archivage d'autres machines de FDN (jira, kamino, etc.).

# Caractéristiques

- machine virtuelle (proxmox)
- DNS : jabba.fdn.fr

> Empreintes SSH du serveur :

	256 SHA256:hANbecDTY1rPMyqZTWvb85bCWEQgg9R4lzMWwn/H7H4 MD5:74:8a:ba:02:c7:61:9c:37:3f:9b:4e:70:30:32:a9:e4 (ECDSA)
	2048 SHA256:dCVV+ToSbf3I9CSotvi7r1cL0tTPOImRP/Azc4aCbaQ MD5:b3:6e:ad:84:9d:52:8c:be:ed:60:f5:6f:29:f7:bc:3b (RSA)
	256 SHA256:irMfXBC02Ibyxhx279EU/CRCN8i9rFp089zCjQYEOYY MD5:b2:0d:20:b6:6b:9b:ae:cd:1a:0c:a6:87:6e:14:d7:62 (ED25519)

# Principe

Cette VM a pour unique but de stocker des archives d'autres VMs de FDN, l'archivage se faisant via rsync+ssh.

Chaque VM étant archivée a son propre dossier dans **/srv**.

# Utilisation

## Création d'un espace de stockage pour une VM

Soit la VM *vm2backup* à archiver.

Aller sur la machine *vm2backup* et y créer une paire de clés SSH pour l'utilisateur qui effectue la sauvegarde, sans mot de passe :

	ssh-keygen -b 4096 -t rsa

Se connecter à *jabba* et créer l'utilisateur *vm2backup* :

	sudo adduser --home /srv/vm2backup --quiet --disabled-password --gecos vm2backup vm2backup
	chmod 700 /srv/vm2backup

Puis copier la clé publique SSH à la racine de l'utilisateur *vm2backup* :

	sudo su - vm2backup
	mkdir .ssh
	vi .ssh/authorized_keys
	# coller la clé SSH publique

Se connecter en SSH depuis *vm2backup* vers jabba pour authentifier le serveur :

	ssh vm2backup@jabba.fdn.fr
	# vérifier l'empreinte du serveur (voir plus haut)

## Mise en place de l'archivage

Se connecter sur *vm2backup* et mettre en place l'archivage dans la crontab, par exemple :

	#!/bin/bash

	RSYNC=`which rsync`
	OPTIONS="-a --delete-after"
	REMOTE="jira@jabba.fdn.fr"

	# Archive de vm2backup:/local/path vers jabba:/srv/vm2backup/remote/path
	$RSYNC $OPTIONS /local/path $REMOTE:~/remote

> Rappel : `rsync [options] source destination`, attention au `/` à la fin de *source* :

- `rsync -a /path/source /path/destination` : crée un répertoire **source** dans `/path/destination`
- `rsync -a /path/source/ /path/destination` : archive le **contenu** du répertoire **source** dans `/path/destination` sans créer de répertoire **source**

# Buildbook

Rien de particulier à faire !
