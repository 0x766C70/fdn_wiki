# Équipe Adminsys

> Les pseudos sont contactables sur IRC/Matrix, et les mails sont du type `pseudo@fdn.fr`

## Admincore (noyau)

```json:table
{
    "fields" : [
        {"key": "login"   , "sortable": true, "label": "Login"},
        {"key": "services", "sortable": true, "label": "Référent/Accès Services (vue adhérents)"}
    ],
    "items": [
        {"login": "afriqs", "services": "web mutualisé, RT, Gitlab, PVE, PBS"},
        {"login": "pandaroux", "services": "pad, web mutualisé"},
        {"login": "tom28", "services": "mail_solo, mailing, UUCP, DNS"},
        {"login": "vlp", "services": "mail, LDAP, Gitlab, Matrix, botbot"}
    ],
    "markdown" : true
}
```

## Adminsys (root sur au moins une machine)

```json:table
{
    "fields" : [
        {"key": "login"   , "sortable": true, "label": "Login"},
        {"key": "services", "sortable": true, "label": "Référent/Accès Services (vue adhérents)"}
    ],
    "items": [
        {"login": "damfle"        , "services": "Kessel"},
        {"login": "dino"          , "services": "Peertube, Pad, BBB"},
        {"login": "domi"          , "services": "DNS, mail, LNS, SI"},
        {"login": "eric"          , "services": "sites web FDN, capsule Gemini"},
        {"login": "hguilbert"     , "services": "mail, Matrix, DNS, XMPP"},
        {"login": "khrys"         , "services": "sites web FDN, listmaster mailing, capsule Gemini"},
        {"login": "stephaneascoet", "services": "listmaster mailing"},
        {"login": "youpi"         , "services": "VPN, LNS, SI"},
        {"login": "neox"          , "services": "XMPP"}
    ],
    "markdown" : true
}
```

## Admin du SI (Système d'Information Vador)

```json:table
{
    "fields" : [
        {"key": "login", "sortable": true, "label": "Login"}
    ],
    "items": [
        {"login": "nicolas"},
        {"login": "domi"},
        {"login": "perliculteur"},
        {"login": "thy"},
        {"login": "youpi"},
        {"login": "khrys"}
    ],
    "markdown" : true
}
```
