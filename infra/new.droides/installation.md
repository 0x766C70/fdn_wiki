* Installation de Debian Base.
* Passage de Puppet Base.
* Apt-get update
* echo "deb http://download.proxmox.com/debian/pve stretch pve-no-subscription" > /etc/apt/sources.list.d/pve-install-repo.list
* wget http://download.proxmox.com/debian/proxmox-ve-release-5.x.gpg -O /etc/apt/trusted.gpg.d/proxmox-ve-release-5.x.gpg
* chmod +r /etc/apt/trusted.gpg.d/proxmox-ve-release-5.x.gpg
* apt update
* apt dist-upgrade
* apt install proxmox-ve postfix open-iscsi
* Selectionner Satelitte system, laisser System mail name et mettre mail.fdn.fr pour SMTP Relay host
* shutdown -r now
* proof : check uname -ar : le kernerl doit etre celui de PVE
* Connection via https://r5d4.fdn.fr:8006 & https://tc14.fdn.fr:8006
* Utilisation du compte root local pour commencer
* Groups : Create Name : admins
* Permissions -> Add Group Permission Path / Group admins Role Administrator
* Users : ajouter son user PAM, changer le groupe pour admins
* Datacenter > Host > Certificates > Edit Domains : ajouter le nom de la machine > Register Account > Accept TOS > email : adminsys@fdn.fr puis Order Certificate and that's it !
* Users : Edit user root : Uncheck Enabled
* Suppression du warning de licence : sudo sed -Ezi.bak "s/(Ext.Msg.show\(\{\s+title: gettext\('No valid sub)/void\(\{ \/\/\1/g" /usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js && sudo systemctl restart pveproxy.service
