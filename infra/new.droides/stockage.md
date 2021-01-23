# Espace de stockage

LVM + chiffrement, cf. #9

```
r5d4

  514  lvcreate -n data -L 2400g vg1
    515  apt install cryptsetup
      518  cryptsetup luksFormat /dev/vg1/data
        519  cryptsetup luksOpen /dev/vg1/data data
          521  mkfs.ext4 /dev/mapper/data
            525  mkdir /mnt/gluster
              526  mount /dev/mapper/data /mnt/gluster
                528  apt install glusterfs-server 
                  530  gluster peer probe tc14.fdn.fr
                    531  gluster peer list
                      532  gluster peer status
                        533  touch /var/lib/glusterd/secure-access
                          534  cd /etc/ssl/
                            535  sudo openssl genrsa -out glusterfs.key 4096
                              536  sudo openssl req -new -x509 -key glusterfs.key -days +3650 -subj "/CN=r5d4.fdn.fr" -out glusterfs.pem
                                537  cat glusterfs.pem 
                                  538  cat > glusterfs.ca # contenu des glusterfs.pem des deux nœuds
                                    542  systemctl restart glusterfs-server
                                      -> devenu glusterd en buster
                                        544  gluster volume create data replica 2 transport tcp r5d4.fdn.fr:/mnt/gluster/brick tc14.fdn.fr:/mnt/gluster/brick
                                          -> r5d4-repli, tc14-repli ; et puis c'est plus logique d'avoir le volume 'data' crypt dans /mnt/data donc on renomme un peu...
                                            gluster volume create data repli 2 transport tcp tc14-repli:/mnt/data/gluster-data r5d4-repli:/mnt/data/gluster-data
                                              555  gluster volume get data all
                                                556  gluster volume set data auth.ssl-allow 'r5d4.fdn.fr,tc14.fdn.fr'
                                                  557  gluster volume set data client.ssl on
                                                    558  gluster volume set data server.ssl on
                                                      xxx  gluster volume set data ssl.cipher-list 'HIGH:!SSLv2:!SSLv3:!TLSv1:!TLSv1.1:TLSv1.2:!3DES:!RC4:!aNULL:!ADH'
                                                        545  gluster volume start data


                                                        tc14

                                                          500  lvcreate -n data -L 2400g vg1
                                                            501  apt install cryptsetup
                                                              502  cryptsetup luksFormat /dev/vg1/data
                                                                503  cryptsetup luksOpen /dev/vg1/data data
                                                                  504  mkfs.ext4 /dev/mapper/data
                                                                    506  mkdir /mnt/gluster
                                                                      507  mount /dev/mapper/data /mnt/gluster
                                                                        508  apt install glusterfs-server
                                                                          513  touch /var/lib/glusterd/secure-access
                                                                            514  cd /etc/ssl
                                                                              515  openssl genrsa -out glusterfs.key 4096
                                                                                516  openssl req -new -x509 -key glusterfs.key -days +3650 -subj "/CN=tc14.fdn.fr" -out glusterfs.pem
                                                                                  517  cat glusterfs.pem 
                                                                                    520  cat > glusterfs.ca # meme contenu que l'autre
                                                                                      521  systemctl restart glusterfs-server
                                                                                      ```


                                                                                      Façon alternative de générer les certifs:

                                                                                      ```
                                                                                      # les deux
                                                                                        539  openssl genrsa 4096 > glusterfs.ca.key
                                                                                          541  openssl req -sha512 -new -x509 -nodes -days 3650 -key glusterfs.ca.key > glusterfs.ca
                                                                                          # par nœud
                                                                                            555  openssl req -new -key glusterfs.key -subj "/CN=tc14.fdn.fr" -out glusterfs.csr
                                                                                              558  openssl x509 -req -in glusterfs.csr -days 3650 -CA glusterfs.ca -CAkey glusterfs.ca.key -set_serial 01 -out glusterfs.pem

                                                                                              # en bonus, une dhparam (vue dans les logs, a partager)
                                                                                              openssl dhparam -out /etc/ssl/dhparam.pem 2048
                                                                                              ```

                                                                                              Une manière encore plus "coolz" avec des alt names, pour la partie par nœud
                                                                                              ```

                                                                                                606  openssl req -new -key glusterfs.key -subj "/CN=tc14.fdn.fr" -config glusterfs-ssl.conf -out glusterfs.csr
                                                                                                  607  openssl x509 -req -in glusterfs.csr -days 3650 -CA glusterfs.ca -CAkey glusterfs.ca.key -set_serial 01 -extensions req_ext -extfile glusterfs-ssl.conf -out glusterfs.pem
                                                                                                  $ cat glusterfs-ssl.conf
                                                                                                  [ req ]
                                                                                                  default_bits       = 4096
                                                                                                  distinguished_name = req_distinguished_name
                                                                                                  req_extensions     = req_ext

                                                                                                  [ req_distinguished_name ]
                                                                                                  countryName                 = Country Name (2 letter code)
                                                                                                  countryName_default         = FR
                                                                                                  stateOrProvinceName         = State or Province Name (full name)
                                                                                                  stateOrProvinceName_default = Paris
                                                                                                  localityName                = Locality Name (eg, city)
                                                                                                  localityName_default        = 
                                                                                                  organizationName            = Organization Name (eg, company)
                                                                                                  organizationName_default    = FDN
                                                                                                  commonName                  = Common Name (e.g. server FQDN or YOUR name)
                                                                                                  commonName_max              = 64
                                                                                                  commonName_default          = tc14.fdn.fr

                                                                                                  [ req_ext ]
                                                                                                  subjectAltName = @alt_names

                                                                                                  [alt_names]
                                                                                                  DNS.1 = tc14.fdn.fr
                                                                                                  DNS.2 = tc14-repli
                                                                                                  ```


                                                                                                  ## tunings

                                                                                                  gluster a énormément de tunings.

                                                                                                  On applique ceux suggérés pour la virtu: https://github.com/gluster/glusterfs/blob/master/extras/group-virt.example
                                                                                                  ```
                                                                                                  # il y a probablement mieux que de le faire à la main, mais comme ça on archive les settings placés...
                                                                                                  gluster volume set data performance.quick-read off
                                                                                                  gluster volume set data performance.read-ahead off
                                                                                                  gluster volume set data performance.io-cache off
                                                                                                  gluster volume set data performance.low-prio-threads 32
                                                                                                  gluster volume set data network.remote-dio disable
                                                                                                  gluster volume set data performance.strict-o-direct on
                                                                                                  gluster volume set data cluster.eager-lock enable
                                                                                                  gluster volume set data cluster.quorum-type auto
                                                                                                  gluster volume set data cluster.server-quorum-type server
                                                                                                  gluster volume set data cluster.data-self-heal-algorithm full
                                                                                                  gluster volume set data cluster.locking-scheme granular
                                                                                                  gluster volume set data cluster.shd-max-threads 8
                                                                                                  gluster volume set data cluster.shd-wait-qlength 10000
                                                                                                  gluster volume set data features.shard on
                                                                                                  gluster volume set data user.cifs off
                                                                                                  gluster volume set data cluster.choose-local off
                                                                                                  gluster volume set data client.event-threads 4
                                                                                                  gluster volume set data server.event-threads 4
                                                                                                  gluster volume set data performance.client-io-threads on
                                                                                                  ```

                                                                                                  Vu que nos disques sont assez rapide j'ai également augmenté la shard size de 64MB par défaut à 128MB (il s'agit des chunks pour les fichiers d'image: si une IO se passe sur une VM pendant que l'un des serveurs est injoignable, seulement les chunks modifiés doivent être resynchronisés ; la contrepartie d'avoir des plus petits fichiers est d'en avoir plus... Note: un changement de ce tuning n'affecte que les fichiers créés après le changement, il faut recréer les disques existants si on veut avoir un effet immédiat (mv hors puis dans le gluster à VM éteinte par exemple))
                                                                                                  ```
                                                                                                  gluster volume set data features.shard-block-size 128MB
                                                                                                  ```