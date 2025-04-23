# Format de l'empreinte attendue

> A Modular Crypt Format method with 16 character salt and 86 character hash based on the SHA-512 hash function.
> A hash based on SHA-2 with 512-bit output, originally developed by Ulrich Drepper for GNU libc.
> The default CPU time cost parameter is 5000, which is too low for modern hardware.

Pour le mot de passe "Mot de passe" et le grain de sel "poivre",
l'empreinte attendue est :  
`$6$poivre$9.6kqkgiGYE/EvQl7S1IKoQ0nrd0/ThrTEgOPEUA.BKpRNeApF8j.90YH4jZSMnopwLfbStsQAG3ssA7a1IEL/`  
ou  
`$6$rounds=5000$poivre$9.6kqkgiGYE/EvQl7S1IKoQ0nrd0/ThrTEgOPEUA.BKpRNeApF8j.90YH4jZSMnopwLfbStsQAG3ssA7a1IEL/`  
où
 - `6` désigne une fonction de hachage basée sur SHA-2 avec 512 bits (SHA512),
 développée par [Ulrich Drepper](https://www.akkadia.org/drepper/SHA-crypt.txt)
 - `rounds=5000` désigne le nombre de boucles à effectuer,
 entre 1 000 et 999 999 999, 5 000 par défaut ;
 - `poivre` est le grain de sel tronqué à 16 caractères ;
 - `9.6kqkgiGYE/EvQl7S1IKoQ0nrd0/ThrTEgOPEUA.BKpRNeApF8j.90YH4jZSMnopwLfbStsQAG3ssA7a1IEL/` est l'empreinte sur 86 caractères.


# Différentes options pour créer une empreinte

## [openssl-passwd](https://docs.openssl.org/master/man1/openssl-passwd/)

Version reproductible pour test :  
`openssl passwd -6 -salt 'poivre' 'Mot de passe'`
ou  
`openssl passwd -6 -salt 'rounds=5000$poivre' 'Mot de passe'`

Version avec grain de sel aléatoire,
nombre d'itérations par défaut à 5 000 et
saisie du mot de passe sécurisée :  
`openssl passwd -6`

## [doveadm-pw](https://doc.dovecot.org/main/core/man/doveadm-pw.1.html)

`doveadm pw -p 'Mot de passe' -r 5000 -s SHA512-CRYPT`

`doveadm pw -s SHA512-CRYPT`

## [mkpasswd](https://manpages.debian.org/unstable/whois/mkpasswd.1.en.html)

La commande `mkpasswd` est comprise dans le [paquet `whois`](https://packages.debian.org/stable/net/whois).

**Attention, `mkpasswd` n'accepte pas les grains de sel de moins de huit caractères.**

Version reproductible pour test :  
`mkpasswd --method=sha512crypt --salt='poivreblanc' 'Mot de passe'`
ou  
`mkpasswd --method=sha512crypt --salt='poivreblanc' --rounds=5000 'Mot de passe'`
pour obtenir :  
`$6$poivreblanc$5P92EXuwQwf4TdxK/lPcssasL3XFs1jI/igabFczdtGTHSWgrGWrikHjMW0HfBMK.NSYJy7TOYs26U2QtAdk81`

Version avec grain de sel aléatoire,
nombre d'itérations par défaut à 5 000 et
saisie du mot de passe sécurisée :  
`mkpasswd --method=sha512crypt`

## Python 3

### Avec le [module `crypt`](https://docs.python.org/3.12/library/crypt.html#crypt.crypt)

**Le module `crypt` de la bibliothèque standard est déprécié depuis Python 3.11
et sera supprimer en Python 3.13.**

**La méthode `crypt.METHOD_SHA512` n'est disponible que sous Linux.**

Version reproductible pour test :  
`python3 -c 'import crypt; print(crypt.crypt("Mot de passe", salt="$6$poivre"))'`  
ou  
`python3 -c 'import crypt; print(crypt.crypt("Mot de passe", salt=f"${crypt.METHOD_SHA512.ident}$rounds=5000$poivre"))'`

Version avec grain de sel aléatoire,
nombre d'itérations par défaut à 5 000 et
saisie du mot de passe sécurisée :  
`python3 -c 'import crypt,getpass; print(crypt.crypt(getpass.getpass(), crypt.METHOD_SHA512))'`

### Avec le [paquet `passlib`](https://passlib.readthedocs.io/en/stable/lib/passlib.hash.sha512_crypt.html)

**Attention, il est nécessaire d'installer le paquet `passlib` préalablement.**

Version reproductible pour test :  
`python3 -c 'from passlib.hash import sha512_crypt; print(sha512_crypt.hash("Mot de passe", salt="poivre", rounds=5000))'`

Version avec grain de sel aléatoire,
nombre d'itérations par défaut à 656 000 et
saisie du mot de passe sécurisée :  
`python3 -c 'import getpass; from passlib.hash import sha512_crypt; print(sha512_crypt.hash(getpass.getpass()))'`

## Perl ([fonction crypt](https://perldoc.perl.org/functions/crypt))

**Attention, le résultat est différent sous macOS.**

Version reproductible pour test :  
`perl -le 'print crypt "Mot de passe", "\$6\$poivre"'`  
ou  
`perl -le 'print crypt "Mot de passe", "\$6\$rounds=5000\$poivre"'`
