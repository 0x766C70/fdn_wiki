# Utilisation du service

[[_TOC_]]

Avant toutes choses, pour pouvoir bénéficier du service d'hébergement de zone DNS, il faut faire une demande de création de dépôt Gitlab qui servira dans le reste de ce document (que vous pouvez lire avant).

## Zone primaire

Dans votre dépôt, chaque zone est représenté par un fichier nommé avec le nomenclature suivante: `db.<zone>`

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
:warning: Attention: la valeur du `serial` sera ignoré dans le processus de déploiement mais il **doit** être présent.

## Zone secondaire

La gestion des zones secondaires n'est pas possible de façon autonome.
Il faut faire les demandes de changement à un admin DNS en envoyant un mail à services [at] fdn.fr en précisant les informations suivantes:
- le nom de la zone concernée
- la ou les adresses IP des serveurs primaires pouvant fournir la zone

## Délégation interne de zone

Fonctionnalité à developper.

## Autoriser le transfert de zone

Pour le moment, la configuration du transfert de zone doit se faire manuellement par un admin DNS.

## Gestion de la signature des zones (DNSSEC)

### Commencer à signer une zone

Pour commencer à signer votre zone, l'entrée DS ne doit pas être publié dans le registre. Dans le cas contraire n'hésitez pas à demander conseil sur IRC/Matrix.

Pour demander la signature de la zone, vous devez créer le fichier `2bsigned` à la racine de votre dépôt si il n'existe pas déjà.
Dans ce dernier, ajoutez une ligne qui sera le nom de votre zone (une zone par ligne, sensible à la casse).

Poussez les modifications et, si cela ne se fait pas automatiquement, lancez un pipeline en allant dans votre dépôt -> Build -> Pipelines -> Run pipeline. À la fin du déploiement, votre zone sera signée mais la signature sera ignorée par les résolveurs, c'est tout à fait normal.

Avant de passer à l'étape suivante, il est conseillé de vérifier que votre zone est bien signée. Vous pouvez le faire avec la commande suivante (en remplaçant le nom de la zone `example.com` par la votre):
```console
$ dig @nsa.fdn.fr example.com SOA +dnssec +short
```

Vous devez avoir un résultat resemblant à celui ci-dessous:
```console
nsa.fdn.org. hostmaster.fdn.fr. 2023100105 28800 7200 604800 86400
SOA 13 2 86400 20231015120452 20231001110452 30619 example.com. UfLGpFWfGwW60YJ68SDPwTyhP/zIYtkC3Uu98vQqdmfRqDgZTxJN3pIa j2X1qi6JAuL+9anu16s28ROnMni3bw==
```

L'étape suivante consiste à activer la délégation de signature par le registre, pour cela il faut que ce dernier publie une entrée de type `DS`. Dans la plupart des cas, cela se fait via une interface fourni par le registraire.Chacun ayant un fonctionnement différent, il est préférable de vous référer à la documentation de ce dernier.

Toutefois, dans la plupart des cas, il vous sera demandé les informations de la clé de signature de clé (KSK). Vous pouvez les obtenir avec la commande suivante:
```console
$ dig @nsa.fdn.fr example.com CDS example.com CDNSKEY +dnssec +short
7674 13 2 FA26B0A8017E4274449A188461E92716209340285A92A24134A06875 A72AA328
257 3 13 MTJE8jPPnqJ8tA7zgiZ0IDcQY/MQrzKoTCquZX5MhFtvdmvCxO0AqDrI LCBpPA5jE7zslC/OuwDHZV5/9Pzuew==
```
La première ligne du résultat sont les informations de l'empreinte  de la clé (`(C)DS`), tandis que la seconde est la clé elle-même (`(C)DNSKEY`). Vous trouverez toutes les informations nécessaires pour lire le résultat [ici](https://www.dynu.com/fr-FR/Resources/DNS-Records/DS-Record) et [là](https://www.dynu.com/Resources/DNS-Records/DNSKEY-Record).

**:warning: Les informations sur les clés ne seront publiées dans les serveurs FDN que 24h après l'activation de la signature afin de ne pas provoquer d'indisponibilité de votre zone par la mise en place prématurée de la délégation de signature.**

### Arrêter de signer une zone

## FAQ
