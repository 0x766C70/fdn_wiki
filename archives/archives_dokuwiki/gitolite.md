**Gitolite était installé sur leia, il a été remplacé par [[adminsys:gitlab]].**

Tous les *root* de leia (à la date de l'installation le 20 avril 2013) y ont accès, y compris *root@leia* lui-même (plus simple pour gérer la config Puppet).

# Ajouter un utilisateur

    git clone gitolite@leia.fdn.fr:gitolite-admin.git
    cd gitolite-admin
    cp /la/clé/SSH/de/l/utilisateur.pub keydir/user.pub
    git add keydir/user.pub
    git commit
    git push

Si l'utilisateur a déjà une clé, on peut en ajouter d'autres dans des fichiers *user@nimportequoi.pub* ; gitolite ne tient pas compte de ce qui suit l'arobase.

Tant qu'on y est on peut ajouter l'utilisateur au groupe @admins dans //conf/gitolite.conf// si on veut, ou y gérer ses droits à part.

# Ajouter un dépôt

    git clone gitolite@leia.fdn.fr:gitolite-admin.git
    cd gitolite-admin
    $EDITOR conf/gitolite.conf
    # Copier sur les voisins.
    git commit
    git push

# Les logs

Ils sont dans ///var/lib/gitolite/.gitolite/logs//.
