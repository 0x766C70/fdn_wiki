# Proxmox

## Présentation

FDN utilise Proxmox Virtual Environment ([PVE](https://www.proxmox.com/en/proxmox-ve)) comme hyperviseur pour la gestion de ses machines virtuelles. PVE utilise KVM pour les machines virtuelles et LXC pour les conteneurs. À ce jour FDN n'administre que des machines virtuelles.

FDN administre deux [*clusters*](https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pvecm) de deux machines physiques chacun :
- **prod** qui héberge tous les services opérés par FDN, à destination du public, des adhérents ou des bénévoles
- **backup** qui héberge une machine virtuelle sur laquelle est installé Proxmox Backup Server ([PBS](https://www.proxmox.com/en/proxmox-backup-server)), utilisé pour sauvegarder non seulement les machines virtuelles de **prod** mais également d'autres machines virtuelles pouvant faire tourner le [client PBS](https://pbs.proxmox.com/docs/backup-client.html)

## Table des matières

- [cluster de prod](./proxmox_prod/index.md)
- [cluster de backup](./proxmox_backup/index.md)
- [Proxmox Backup Server](./pbs.md)

## En savoir plus

- [doc PVE](https://pve.proxmox.com/pve-docs/)
- [doc PVE (html)](https://pve.proxmox.com/pve-docs/pve-admin-guide.html)
- [doc PBS](https://pbs.proxmox.com/docs/)
