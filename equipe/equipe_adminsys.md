# Équipe Adminsys

> Les pseudos sont contactables sur IRC/Matrix

## Admincore (noyau)

```json:table
{
    "fields" : [
        {"key": "pseudo"  , "sortable": true, "label": "Pseudo"},
        {"key": "services", "sortable": true, "label": "Référent/Accès Services (vue adhérents)"}
    ],
    "items": [
        {"pseudo": "afriqs",    "services": "web mutualisé, RT, Gitlab, PVE, PBS"},
        {"pseudo": "neox",      "services": "XMPP"},
        {"pseudo": "pandaroux", "services": "pad, web mutualisé"},
        {"pseudo": "tom28",     "services": "mail_solo, mailing, UUCP, DNS"},
        {"pseudo": "vlp",       "services": "mail, LDAP, Gitlab, Matrix, botbot"}
    ],
    "markdown" : true
}
```

## Adminsys (root sur au moins une machine)

```json:table
{
    "fields" : [
        {"key": "pseudo"   , "sortable": true, "label": "Pseudo"},
        {"key": "services", "sortable": true, "label": "Référent/Accès Services (vue adhérents)"}
    ],
    "items": [
        {"pseudo": "damfle"        , "services": "Kessel"},
        {"pseudo": "dino"          , "services": "Peertube, Pad, BBB"},
        {"pseudo": "domi"          , "services": "DNS, mail, LNS, SI"},
        {"pseudo": "eric"          , "services": "sites web FDN, capsule Gemini"},
        {"pseudo": "hguilbert"     , "services": "mail, Matrix, DNS, XMPP"},
        {"pseudo": "khrys"         , "services": "sites web FDN, listmaster mailing, capsule Gemini"},
        {"pseudo": "stephaneascoet", "services": "listmaster mailing"},
        {"pseudo": "vianney",        "services": "guri"},
        {"pseudo": "youpi"         , "services": "VPN, LNS, SI"}
    ],
    "markdown" : true
}
```

## Adminsys du SI (root sur le serveur hébergeant le SI)

```json:table
{
    "fields" : [
        {"key": "login", "sortable": true, "label": "Login"}
    ],
    "items": [
        {"login": "domi"},
        {"login": "khrys"},
        {"login": "nicolas"},
        {"login": "perliculteur"},
        {"login": "thy"},
        {"login": "youpi"}
    ],
    "markdown" : true
}
```

Pour l'accès classique au SI (interface Web), voir [les bénévoles du SI](https://git.fdn.fr/fdn/wiki/-/blob/master/pages/liste_benevoles.md?ref_type=heads#groupe-si)
