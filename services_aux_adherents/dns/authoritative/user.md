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
:warning: Attention: la valeur du sérial sera ignoré dans le processus de déploiement mais il **doit** être présent.

## Zone secondaire

La gestion des zones secondaires n'est pas possible de façon autonome.
Il faut faire les demandes de changement à un admin dns en envoyant un mail à services [at] fdn.fr en précisant les informations suivantes:
- le nom de la zone concernée
- la ou les adresses IP des serveurs primaires pouvant fournir la zone

## Délégation interne de zone

Fonctionnalité à developper.

## Autoriser le transfert de zone

Pour le moment, la configuration du transfert de zone doit se faire manuellement par un admin DNS.

## Gestion du DNSSEC

### Commencer à signer une zone

Pour commencer à signer votre zone, l'entrée DS ne doit pas être publié dans le registre. Dans le cas contraire n'hésitéz pas à demander conseil sur IRC/Matrix.

Pour demander la signature de la zone, vous devez créer le fichier `2bsigned` à la racine de votre dépôt.
Dans ce dernier, ajoutez une ligne qui sera le nom de votre zone (une zone par ligne, sensible à la casse).

Poussez les modifications et si cela ne se fait pas automatiquement, lancez un pipeline en allant dans votre dépôt -> Build -> Pipelines -> Run pipeline. À la fin du déploiement, votre zone sera signée mais la signature sera ignorée.

Avant de passer à l'étape suivante, il est conseillé de vérifier que votre zone est bien signée. Vous pouvez le faire avec la commande suivante (en remplaçant le nom de la zone `example.com` par la votre):
```console
$ dig @nsa.fdn.fr example.com SOA +dnssec +short
```

Vous devez avoir un résultat resemblant à celui ci-dessous:
```console
sa.fdn.org. hostmaster.fdn.fr. 2023100105 28800 7200 604800 86400
SOA 13 2 86400 20231015120452 20231001110452 30619 example.com. UfLGpFWfGwW60YJ68SDPwTyhP/zIYtkC3Uu98vQqdmfRqDgZTxJN3pIa j2X1qi6JAuL+9anu16s28ROnMni3bw==
```

L'étape suivante consiste à activer la délégation de signature par le registre, pour cela il faut que ce dernier publie une entrée de type `DS`. Dans la plupart des cas, cela se fait via une interface fourni par le registraire. Pour avoir une

### Arrêter de signer une zone

## FAQ
