# Les serveurs physiques

## Les droïdes (cluster Proxmox de prod)

- [tc14](./machines/tc14.md) (cluster de prod à TH2)
- [r5d4](./machines/r5d4.md) (cluster de prod à PA3)

## Les droïdes (cluster Proxmox de sauvegardes)

- [r4p17](./machines/r4p17.md) (PBS - Proxmox Backup Server)
- [c3px](./machines/c3px.md) (PBS - Proxmox Backup Server)

## Les NanoPis (supervision locale)

- [nanopi-pa3](./machines/nanopi-pa3.md) (PA3)
- [nanopi-th2](./machines/nanopi-th2.md) (TH2)

# Les machines virtuelles

## LNS (routeurs et L2TP)

- [lns31](./machines/lns31.md)
- [lns32](./machines/lns32.md)
- [lns22](./machines/lns22.md)
- [lns11](./machines/lns11.md) (legacy)
- [gw1](./machines/gw1.md) (passerelle)
- [gw2](./machines/gw2.md) (passerelle)

## Les serveurs de nom

- [dgsi](./machines/dgsi.md)
- [nsa](./machines/nsa.md)
- [gchq](./machines/gchq.md)

## Les résolveurs DNS

- [resolver0](./machines/resolver0.md)
- [resolver1](./machines/resolver1.md)

## RADIUS

- [radius0](./machines/radius0.md)
- [radius1](./machines/radius1.md)

## Tunnels chiffrés (OpenVPN)

- [vpns](./machines/vpns.md) vpn[1-10][-rw]
- [vpn-open1](./machines/vpn-open1.md) (openbar)

## Web & contenu

- [rey](./machines/rey.md) (web mutualisé *reloaded*)
- [chewie](./machines/chewie.md) (sites web FDN)
- [ackbar](./machines/ackbar.md) [(tracker torrent + media.fdn.fr)](https://ackbar.fdn.fr/) *(non présent dans Puppet)*
- [tiree](./machines/tiree.md) [(peertube)](https://tube.fdn.fr/)

## Communication

- [solo](./machines/solo.md) (old-mail + listes Sympa)
- [taslin](./machines/taslin.md) (nouvelle infra mail)
- [jyn](./machines/jyn.md) (serveur jabber)
- [neo](./machines/neo.md) (matrix)
- [talk](./machines/talk.md) (jitsi - visioconférence)
- [turn](./machines/turn.md) (TURN/STUN pour WebRTC)
- [pz4co](./machines/pz4co.md) (mumble - voix)

## Outils internes

- [coruscant](./machines/coruscant.md) [(gitlab)](https://git.fdn.fr/)
- [sebulba](./machines/sebulba.md) (gitlab runner CI)
- [si](./machines/si.md) (SI FDN)
- [palpatine](./machines/palpatine.md) (puppetmaster)
- [anakin](./machines/anakin.md) [(SSO - sso.fdn.fr)](https://sso.fdn.fr/)
- [sabe](./machines/sabe.md) (serveur LDAP)
- [padme](./machines/padme.md) (serveur LDAP)
- [pad](./machines/pad.md) [(etherpad - pad.fdn.fr)](https://pad.fdn.fr/)
- [jabba](./machines/jabba.md) (archivage)
- [gardulla](./machines/gardulla.md) (cluster MariaDB Galera)
- [zorba](./machines/zorba.md) (cluster MariaDB Galera)
- [sandbox2](./machines/sandbox2.md) (bac à sable)
- [capsule](./machines/capsule.md)
- [mustafar](./machines/mustafar.md)
- [guri](./machines/guri.md) (reverse proxy Headscale)

## Supervision

- [governor](./machines/governor.md) (Prometheus)
- [supervisor](./machines/supervisor.md) (Grafana + Prometheus + Loki + Alertmanager)
- [skytop](./machines/skytop.md) (supervision externe - VM Grenode)
- [cecinestpasleia](./machines/cecinestpasleia.md) (ancien serveur de supervision)
- [boba](./machines/boba.md) (LibreNMS)

## Sauvegarde

- [scarif](./machines/scarif.md) (Proxmox Backup Server)

## Ticketing

- [jira](./machines/jira.md)

# Machines décommissionnées

- [vador](./machines/vador.md) *(éteinte et mise au rebut en 2016)*
- [lns01](./machines/lns01.md) *(non présent dans Puppet, remplacé par lns11)*
- [lns02](./machines/lns02.md) *(non présent dans Puppet, remplacé par lns11)*
- [korr](./machines/korr.md) *(non présent dans Puppet)*
- [kylo](./machines/kylo.md) *(non présent dans Puppet)*

# Les machines virtuelles non gérées par FDN

- [geeknode2](./machines/geeknode2.md) : asso Geeknode - `bureau@geeknode.org`
- [unefede](./machines/unefede.md) : Fédération FDN - `adminsys@ffdn.org`
