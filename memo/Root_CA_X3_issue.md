# fix temporaire pour https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=995432

1. Upgrade ca-certificate
2. Dans /etc/ca-certificates.conf: ajouter un point d'exclamation ! devant mozilla/DST_Root_CA_X3.crt
3. update-ca-certificate
4. regen des certifs
