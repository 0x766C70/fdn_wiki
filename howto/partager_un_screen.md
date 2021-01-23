
Quand on travaille à plusieurs sur une machine, il est utile d'avoir une console partagée. Il y a deux cas de figure, expliqués ci-dessous.

## Tout le monde est root sur la machine

Une personne créée un screen :

    root@mamachine:~# screen -S monscreen

Puis les autres le rejoignent :

    root@mamachine:~# screen -x monscreen

## Tout le monde n'est pas root sur la machine

Il faut alors utiliser la fonctionnalité "multiuser" de screen pour partager un screen entre plusieurs comptes unix. (Attention : on tue tous les screens existants sur la machine au passage...)

On configure screen pour accepter ce mode :

    fabien@mamachine:~$ sudo chmod u+s $(which screen)
    fabien@mamachine:~$ sudo chmod 755 /var/run/screen
    fabien@mamachine:~$ sudo rm -fr /var/run/screen/*

Puis on crée le screen et on le partage :

    fabien@mamachine:~$ screen -S monscreen
    Ctrl-a :multiuser on
    Ctrl-a :acladd mon-copain
    Ctrl-a :acladd mon-autre-copain

Et les camarades peuvent attacher le screen :

    mon-copain@mamachine:~$ screen -x fabien/monscreen

Enjoy :)



## Quelques pointeurs sur screen :

 - [Screen quick reference](http://aperiodic.net/screen/quick_reference)
 - [How to share a screen](http://wiki.networksecuritytoolkit.org/nstwiki/index.php/HowTo_Share_A_Terminal_Session_Using_Screen#Sharing_A_Screen_Session_With_Another_User)
