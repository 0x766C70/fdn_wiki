# Différentes options pour créer un hash

# openssl

`openssl passwd -6 -salt xyz  yourpass`

# doveadm

`doveadm pw -s SHA512-CRYPT`

# mkpasswd dans le paquet whois

`mkpasswd -m sha512crypt`

# Python3

## Avec crypt (déprécié et METHOD_SHA512 ne fonctionne que sur Linux)

`python3 -c 'import crypt,getpass; print(crypt.crypt(getpass.getpass(), crypt.METHOD_SHA512))'`

## Avec passlib (fonctionne partout)

`python3 -c 'import getpass; from passlib.hash import sha512_crypt; print(sha512_crypt.hash(getpass.getpass(), rounds=5000))'`

# Perl

`perl -le 'print crypt "desiredPassword", "\$6\$customSalt\$"'`
