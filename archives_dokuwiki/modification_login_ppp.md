Sur Vador, exécuter la commande SQL suivante 

''update RADUSER set RADUSER_LOGIN = 'nouveau.login@fdn.nerim' where RADUSER_LOGIN = 'ancien_login';''

Ou encore

''update RADUSER, LIGNE set RADUSER.RADUSER_LOGIN = 'nouveau.login@fdn.nerim' where RADUSER.LIGNE_ID = LIGNE.LIGNE_ID and LIGNE.LIGNE_TEL = '0000000000';''

où 0000000000 est à remplacer par le numéro de la ligne de téléphone concernée.

*NB: RADUSER_ID n'est ni le numéro d'adhérent, ni le numéro client*
