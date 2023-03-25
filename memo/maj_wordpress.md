# Mise à jour du site Wordpress

### 1 - Faire un snapshot de la vm idoine.

Pour cela, il faut avoir les accès à proxmox via https://tc14.fdn.fr:8006 

Cliquer sur la vm 169052 (chewie.fdn.fr) sur le nœud r5d4. 
Un menu s'affiche, choisir 'Snapshots > Take snapshot' et mettre un nom pour le snapshot (ça doit commencer par une lettre ; éviter les caractères trop "spéciaux") + une description et décocher "Include RAM".


###  2 - Se connecter sur chewie.fdn.fr

Pour ce qui suit, il faut faire partie du groupe **web-admin** de chewie.

### 3 - Mise à jour de Wordpress

#### 3.a - Mise à jour en direct

Taper dans cet ordre les commandes suivantes :
* wp-prod core check-update
* wp-prod core version
* wp-prod core update
* wp-prod plugin status
* wp-prod plugin update --all
* wp-prod theme status
* wp-prod theme update --all
* wp-prod language core update
* wp-prod language theme update --all
* wp-prod language plugin update --all
* wp-prod cli version
* wp-prod cli update

Si après ça, le site n'est plus opérationnel, retourner dans proxmox, cliquer sur le snapshot précédemment effectué puis sur le bouton "Rollback" et relancer la vm (bouton "Start" en haut à droite) ;-) 

Si le site est fonctionnel on peut repousser sur gitlab dans la branche "master" sur https://git.fdn.fr/communication/www :

* sudo -u web-admin -g www-prod -i
* cd /srv/web/www-prod/repo
* git add . && git commit -m 'MAJ repo gitlab www depuis www-prod' && git push origin

#### 3.b - Mise à jour via devel

Resynchroniser devel sur la branche de prod:
* prod2devel

Faire la mise à jour wordpress:
* wp-devel core check-update
* wp-devel core version
* wp-devel core update
* wp-devel plugin status
* wp-devel plugin update --all
* wp-devel theme status
* wp-devel theme update --all
* wp-devel language core update
* wp-devel language theme update --all
* wp-devel language plugin update --all
* wp-devel cli version
* wp-devel cli update

Vérifier que tout va bien sur www-devel.fdn.fr

Pousser sur la branche 'master' de gitlab:
* sudo -u web-admin -g www-devel -i
* cd /srv/web/www-devel/repo
* git add . && git commit -m "MAJ repo gitlab www depuis www-devel" && git push origin HEAD:master

Mettre à jour prod avec:
* upgrade-prod

Vérifier que tout va bien sur www.fdn.fr à nouveau

### 4 - Mise à jour du thème FDN

Voir procédure sur [communication/www](https://git.fdn.fr/communication/www/-/blob/master/README.md)
