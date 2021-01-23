Le tracker est installe sur yoda, il est lancé par l'init venant du package ''bittorrent-tracker''.

La configuration est dans ''/etc/default/bittorrent-tracker''.

Les torrents autorisés sont à déposer dans ''/var/lib/bittorrent'' . Le démon regarde dedans tous les 1/4 d'h par défaut. 

Le port par défaut est 6969, hostname ''tracker.fdn.fr''.

Les logs sont dans ''/var/log/bittorrents'' .

Pour fabriquer un torrent: lancer

    btmakemetafile lefichier http://tracker.fdn.fr:6969/announce

(ou l'inverse, selon la variante de ''btmakemetafile'' qu'on utilise)
