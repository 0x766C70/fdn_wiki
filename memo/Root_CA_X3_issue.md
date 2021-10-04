# fix temporaire pour https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=995432

1. Upgrade ca-certificate
2. Dans /etc/ca-certificates.conf: ajouter un point d'exclamation ! devant mozilla/DST_Root_CA_X3.crt
3. update-ca-certificates
4. regen des certifs
5. sudo -u acme /usr/local/bin/acme_renew --config /etc/acme/certif.conf
