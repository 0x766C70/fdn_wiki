
Le fait de "backporter" un paquet signie de le compiler pour une version
précédente de debian. Quand il n'y a pas de problème de dépendance, c'est assez
simple de backporter un paquet debian.

* [[https://www.debian.org/doc/manuals/maint-guide/build.fr.html]]
* [[https://pbuilder-docs.readthedocs.org/en/latest/faq.html]]

Cela peut se faire sur son ordinateur, même si celui-ci n'est pas dans la
version cible debian souhaitée.

    DIST=jessie
    BASETGZ=/var/cache/pbuilder/$DIST-base.tgz
    
Création d'un environement de compilation :

    sudo apt-get install pbuilder debootstrap devscripts
    sudo pbuilder create --distribution $DIST --basetgz $BASETGZ

Récupération du paquet :

    apt-get source mon_paquet
    
Compilation du paquet :

    cd mon_paquet*
    sudo pbuilder update --distribution $DIST --basetgz $BASETGZ
    dch --local ~fdn+ --distribution jessie-backports "compilé pour jessie."
    pdebuild -- --basetgz $BASETGZ --buildresult ..
    cd ..
    ls *.deb

