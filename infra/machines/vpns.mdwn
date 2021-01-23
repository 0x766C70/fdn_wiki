[[!meta description="vpns - vms pour les tunnels chiffrés des membres"]]

Machine virtuelle pour les [[tunnels chiffrés des membres|services/tunnel_chiffre]].

Actuellement (2019-04-10) il y a 5 vm pour assurer la redondance du service:

- vpn1
- vpn2
- vpn3
- vpn4
- vpn5

Ils sont accessible via vpnX.fdn.fr ou via vpnX-rw.fdn.fr.

À partir de vpn4 ils ont été créés avec la commande suivante:

    gnt-instance add \
        -B memory=1G,vcpus=2 \
        -t drbd -s 5G \
        --net 0:link=br3 --net 1:link=br800 \
        -o debootstrap+stretch \
        -n r4p17.fdn.fr:c3px.fdn.fr \
        vpnX.fdn.fr

La partie `-n r4p17.fdn.fr:c3px.fdn.fr` n'est présente que parce qu'il
y a actuellement (2019-04-10) un bug connu sur la version de ganeti déployée.
Il ne sera plus nécessaire et non recommendée de la rajouter lorsque ganeti
sera mis à jour.
