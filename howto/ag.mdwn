[[!meta title="Comment gérer les AG dans le SI"]]

Pour quelqu'un ayant les droits sur si (si@fdn.fr) :

Les différentes actions sont à faire en root.
Elles sont décrites dans le fichier `/etc/fdn/adsl/adhs/ag.cfg`

On recopie ici le mode d'emploi :

*  Ajouter une section `[ag-2042]` pour l'année voulue
`status = new`

*  Quand la date de l'AG est fixée et annoncée, passer le status à "open", les adhérent·e·s peuvent dire s'ils veulent une convocation papier ou pas et donner procuration.
    *  Ajouter dans la section `[ag-2042]`:
`date = la date de l'AG`
    *  Ajouter une colonne dans la table CONVOCATION, sinon ça pas-marche (exemple pour 2042) :
`mysql> alter table CONVOCATION add column CONVOCATION_2042 varchar(20) not null default 'pdf' after CONVOCATION_2041;`
    *  Faire un template spécifique pour la convocation à l'AG
 (exemple: ag2042.tpl dans templates/tex dans le git, à installer dans /usr/share/fdn/templates/adsl/tex)
    *  Modifier /etc/fdn/adsl/tex-tmp.cfg pour donner à LaTeX les infos dont il a besoin
          *  On peut le tester avec `sudo -u www-data ag-convocation-test.pl <annee> <id_client>`
(prendre 20 comme id client, c'est le sieur Bayart, il devrait rester adhérent un moment) 
Exemple : taper sudo -u www-data ag-convocation-test.pl 2042 20
         *  Vérifier les résiliations récentes, les changements d'adresse récents adressés au bureau etc. pour avoir une base aussi propre que possible à ce moment là.
     *  le script `sudo -u www-data ag-convocation-papier.pl <annee>` produit le gros PDF avec toutes les convocations papier dedans, à imprimer recto/verso, les adhérent·e·s qui n'ont pas demandé de papier ne sont pas dedans


*  Une fois les convocations papier envoyées, il faut passer le status de "open" à "convoc".  Il n'est alors plus possible de choisir le format de la convocation qu'on recevra.
   * Pour savoir combien de gens ont demandé la version papier: taper mysql adsl puis `select * from CONVOCATION where CONVOCATION_2042 like "papier%";`
   *  Le script `sudo -u www-data ag-convocation-pdf.pl <annee>` produit tous les PDF individuels, que les  adhérent·e·s aient demandé du papier ou non.
   *  Le script `sudo -u www-data ag-liste.pl <annee>` produit la liste des gens convoqués.

*  La veille de l'AG, quand la liste des procurations est close, passer le status de "convoc" à "close"
     *  Se mettre dans `/tmp` pour que l'utilisateur `www-data` puisse écrire les résultats des commandes ci-dessous.
     *  Le script `sudo -u www-data ag-liste-procu.pl <annee>` produit un fichier PDF de la liste des procurations.
     *  Le script `sudo -u www-data sign-ag.pl <annee>` produit un fichier PDF d'émargement
     *  Le script `sudo -u www-data ag-liste-presents.pl <annee>` produit une liste des présences

*  Quand le CR de l'AG, quel que soit sa forme, est disponible en ligne, ajouter le 'link' avec l'URL dans [ag-2042], passer le status en "old".



*  Les AG en 'old' ne sont plus éditables, le PDF de convocation est toujours là.

<br/>

    [ag-2014]
    	status = old
    	date = 2014-03-30
    	link = http://lien.vers.le.cr/ag.html

 *  Les AG en 'open' sont éditables, le PDF n'est pas encore là.

*  Les AG en 'convoc' sont éditables pour la procuration, mais plus pour le format. Le PDF est là, le link pas encore.

Exemple : <br/>

    [ag-2015]  
    	status = old    
    	date = 2015-03-28    
    	link = https://wiki.fdn.fr/cr-ag:copie-pad2015   

*  Les AG en 'close' ne sont plus editables, le PDF est là, le link n'est pas encore là.

*  Les AG en 'new' ne sont pas encore éditables, pas encore de PDF, pas encore de link, pas encore de lien.

*  Le fichier ag.cfg sert également de configuration pour que les AG soient visibles dans l'espace adhérent.


On retrouve avec la commande suivante les templates latex des AG:
`root@si:~# ls -l /usr/share/fdn/templates/adsl/tex`


Pour une nouvelle AG il faut copier le fichier de l'an dernier avec la nouvelle année :  ag20XX.tpl 

S'il y a besoin d'éditer la colonne de gauche des convocations, il faut éditer le fichier :
`/usr/share/fdn/templates/adsl/tex/fdnhead2.sty`


debug avec benj: `ls -l /var/lib/fdn/adsl/stock-pdf | less`

Generation convoc benj: en tant que www-data: `sudo -u www-data ag-convocation-test.pl <annee> <id_client>`

gen all pdf: en tant que www-data: `sudo -u www-data ag-convocation-pdf.pl 2042`

Attention, si vous avez lancé ag-convocation-test.pl en tant qu'utilisateur non-www-data, il traîne un /tmp/ag2042, à supprimer pour que www-data puisse le recréer.

S'il faut regénérer les pdf de convocation (parce qu'on a changé le .tpl), il faut supprimer les pdfs déjà générés:

`rm -f /var/lib/fdn/adsl/stock-pdf/adhacc-*/ag2042.pdf`

S'il faut remettre à zéro les réponses des gens (parce que la date a changé), on peut utiliser:

`mysql> update CONVOCATION set CONVOCATION_2042='pdf'`
