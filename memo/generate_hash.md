# Différentes options pour créer un hash

# openssl

`openssl passwd -6 -salt xyz  yourpass`

# doveadm

`doveadm pw -s SHA512-CRYPT`

# mkpasswd dans le paquet whois

`mkpasswd -m sha512crypt`

# Python3

`python3 -c 'import crypt,getpass; print(crypt.crypt(getpass.getpass(), crypt.METHOD_SHA512))'`

# Perl

`perl -le 'print crypt "desiredPassword", "\$6\$customSalt\$"'`
