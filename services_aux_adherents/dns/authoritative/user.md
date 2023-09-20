# Utilisation du service

[[_TOC_]]

Avant toutes choses, pour pouvoir bénificier du service d'hébergement de zone DNS, il faut faire une demande de création de dépôt Gitlab qui servira dans le reste de ce document (que vous pouvez lire avant).

## Zone primaire

Dans votre dépôt, chaque zone est représenté par un fichier nommé avec le nomencalture suivante: `db.<zone>`

Le contenu doit ressembler à cela:
```dns
TTL 1D
@	IN	SOA	nsa.fdn.org.	hostmaster.fdn.fr. (
		1970010100	; Serial number
		28800		; Refresh 8 hours
		7200		; Retry 2 hours
		604800		; Expires 7 days
		86400 )		; Minimum 1 day

	IN	NS	nsa.fdn.org.
	IN	NS	gchq.fdn.org.
```
<span style="color:orange">Attention: la valeur du sérial sera ignoré dans le processus de déploiement mais il **doit** être présent.</span>

## Zone secondaire

La gestion des zones seondaires n'est pas possible de façon autonome, il faut en faire les demandes de changement à un admin dns.

## Délégation interne de zone

Fonctionnalité à developper.

## Autoriser le transfert de zone

Pour le moment, la configuration du transfert de zone doit se faire manuellement par un admin DNS.

## Gestion du DNSSEC

### Commencer à signer une zone

### Arrêter de signer une zone

## FAQ
