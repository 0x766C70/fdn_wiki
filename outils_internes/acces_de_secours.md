# Accès de secours

Nous avons une machine virtuelle chez gitoyen pour nous permettre d'accéder à
notre infrastructure indépendament de nos passerelles. Cette machines est
connecté à différents réseaux :

- vlan 3 (vlan des serveurs de FDN)
- vlan 800 (vieux réseau privé normalement plus utilisé)
- vlan 801 (vlan admin: ipmi et switchs)
- IP public de Gitoyen
- un vlan privé chez gitoyen pour accèder aux nanopi sans
  passer par nos équipements


## Accès

Pour s'y connecter :

- `ssh -p 2222 endor.fdn.fr`
- `ssh -p 2222 endor-admin.fdn.fr`
- `ssh -p 2222 admin-fdn.gitoyen.net`


## Relais ssh

On peut utiliser endor comme rebond ssh pour accèder aux droides ou VMs de fdn:

- Définir endor dans son .ssh/config
```
Host endor
	Hostname fdn.vms-net.gitoyen.net
	Port 2222
```
- utiliser endor en ProxyJump ssh, par exemple: `ssh -J endor palpatine.fdn.fr`

## IPMI des serveurs

On peut également utiliser endor pour accèder à l'ipmi des machines:

- Par exemple: `conman tc14`
- il y a aussi les switchs, e.g. `conman switch-pa3`, via les nanopi
- Le charactère de controle est '&'
  - &? pour l'aide
  - &. pour sortir
  - &L pour rejouer les logs
  - &B pour break (sysrq, tous ne sont pas autorisés)
- Les logs de la console sont dans /var/log/conman, avec 4 archives dans /var/log/conman.old
- On peut aussi rebooter les machines: `ipmitool -I lanplus -H tc14-ipmi.fdn.fr -U ADMIN chassis power status`
  - Les mots de passes sont dans la conf conman :|
     - on peut mettre la conf en ram et dans le pass de FDN, et demander à un admin de la recréer à chaque fois ?
  - replacer status par on, off, cycle (reset avec au moins 1s de poweroff), reset..
  - Et quelques logs de la carte ipmi, replacer `chassis power status` par `sel info` et `sel list`

## nanopis

Les nanopis ont deux interfaces réseau:
 - une sur le vlan admin de FDN (ipmi/hyperviseurs/endor)
 - une sur un vlan local chez gitoyen, si jamais nos switchs sont HS

Elles ne sont donc pas directement sur internet, mais elles peuvent y accéder à travers endor qui les nattent gentilement (pour mises à jour)

Elles ont également le switch FDN local en serie (ttyUSB0)


Il y a un sredird qui tourne sur xinetd (/etc/xinetd.d/sredird) pour rediriger la console serie des switchs en réseau, et réexporter ça sur le conman d'endor.
Il n'y a donc à priori jamais besoin de se connecter aux nanopi directement, mais les comptes des admins noyaux existent en cas de besoin.
