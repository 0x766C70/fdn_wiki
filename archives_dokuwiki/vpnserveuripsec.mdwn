Le serveur : vpn.fdn.fr

Le serveur ipsec : strongswan-ikev2

La conf :

/etc/strongswan.conf

    charon {
        threads = 16
  
        load = curl openssl gmp random x509 pubkey hmac xcbc stroke kernel-netlink eapradius updown
        plugins {
                eap_radius {
                        secret = Va8XLW
                        server = radius1
                }
        }
        dns1 = 80.67.169.12
        dns2 = 80.67.169.40
    }

/etc/ipsec.conf 

    config setup
          strictcrlpolicy=no
          plutostart=no
    conn %default
          ikelifetime=60m
          keylife=20m
          rekeymargin=3m
          keyingtries=1
          keyexchange=ikev2
          authby=rsasig
          eap=radius
          left=80.67.169.45
          leftsubnet=0.0.0.0/0
          leftcert=/etc/ssl/vpn.fdn.fr.pem
          leftfirewall=yes
          rightsendcert=never
          right=%any
    conn jcd
          rightid=jean.charles.delepine@fdn.fr
          rightsourceip=80.67.179.1
          auto=add
    conn vanhu
          rightid=vanhullebus.yvan@fdn.fr
          rightsourceip=80.67.179.2
          auto=add
    conn cursys
       right=%any
       rightid=cursys@fdn.fr
       rightsourceip=80.67.176.41
       auto=add
    include /var/lib/strongswan/ipsec.conf.inc

La clef de vpn.fdn.fr est dans /etc/ipsec.d/certs
