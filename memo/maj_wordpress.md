# Mise à jour du site Wordpress

### 1 - Faire un snapshot de la vm idoine.

Pour cela, il faut avoir les accès à proxmox via https://tc14.fdn.fr:8006 


Cliquer sur la vm 169052 (chewie.fdn.fr) sur le nœud r5d4. 
Un menu s'affiche, choisir 'Snapshots > Take snapshot' et mettre un nom pour le snapshot (ça doit commencer par une lettre ; éviter les caractères trop "spéciaux") + une description et décocher "Include RAM".


###  2 - Se connecter sur chewie.fdn.fr

Pour ce qui suit, il faut faire partie du groupe **web-admin** de chewie.
Taper `sudo -u web-admin -g www-prod -i`

### 3 - Mise à jour de Wordpress

Taper dans cet ordre les commandes suivantes :
* wp-prod core check-update
* wp-prod core version
* wp-prod core update
* wp-prod plugin status
* wp-prod plugin update --all
* wp-prod theme status
* wp-prod theme update --all
* wp-prod language theme update --all
* wp-prod language plugin update --all
* wp-prod cli version
* wp-prod cli update

Si après ça, le site n'est plus opérationnel, retourner dans proxmox, cliquer sur le snapshot précédemment effectué puis sur le bouton "Rollback" et relancer la vm (bouton "Start" en haut à droite) ;-) 

### 4 - Mise à jour de Gitlab

Une fois que Wordpress est à jour, il faut resynchroniser les fichiers de la branche "master" sur https://git.fdn.fr/communication/www

* cd /srv/web/www-prod/repo
* git add .; git commit -m 'MAJ repo gitlab www depuis www-prod'; git push origin

### 5 - Mise à jour du thème FDN

Voir procédure sur [communication/www](https://git.fdn.fr/communication/www/-/blob/master/README.md)
