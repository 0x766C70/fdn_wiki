# En mode console
Installer strongswan-ikev2

/etc/ipsec.conf
    <code>
    config setup
            # plutodebug=all
            # crlcheckinterval=600
            # strictcrlpolicy=yes
            # cachecrls=yes
            # nat_traversal=yes
            #charonstart=yes
            interfaces="ipsec0=eth0"
            plutostart=no
    
    # Add connections here.
    
    conn %default
            ikelifetime=60m
            keylife=20m
            rekeymargin=3m
            keyingtries=1
            keyexchange=ikev2
            authby=eap
    
    conn fdn
            left=%defaultroute
            leftsourceip=%config
            leftid=jean.charles.delepine@fdn.fr
            eap_identity=jean.charles.delepine@fdn.fr
            leftfirewall=yes
            right=80.67.169.45
            rightcert=vpn.fdn.fr.pem
            rightid=@vpn.fdn.fr
            rightsubnet=0.0.0.0/0
            auto=add''
    </code>        


/etc/ipsec.secrets
    <code>
    jean.charles.delepine@fdn.fr : EAP "tapioca"
    </code>


Mettre [[http://vpn.fdn.fr/certs/vpn.fdn.fr.pem]] dans /etc/ipsec.d/certs/

Installer ca-certificates pour cacert.org.pem

Lancement du vpn : ipsec up fdn

Arrêt du vpn : ipsec down fdn

# Avec NetworkManager (gnome/kde) :

Installer le paquet network-manager-strongswan la version 1.1.2 fonctionne.

{{:adminsys:modifier_vpn.png?300|Configurer le VPN}}

{{:adminsys:choisir_vpn.png?300|}}

{{:adminsys:appliquer_vpn.png?300|}}

Suivant les version il peut être nécessaire de cocher le bouton "Disponible pour tout les utilisateurs"

Il va falloir rendre vpn.fdn.fr.pem accessible, pour l'instant il est sur vpn.fdn.fr:/etc/ipsec.d/certs/vpn.fdn.fr.pem

{{:adminsys:lancement_du_vpn.png?300|}}

Il peut arriver que la connexion ne veuille pas démarrer. Si la version console est installée, ipsec (charon) tourne déjà et il peut falloir l'arrêter.
