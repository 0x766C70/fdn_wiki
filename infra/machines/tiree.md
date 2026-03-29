Machine virtuelle pour l'instance Peertube de FDN.

# Caractéristiques

- Machine : virtuelle
- Distribution : Debian Buster
- Noyau : `Linux tiree.fdn.fr 4.19.0-6-amd64 #1 SMP Debian 4.19.67-2 (2019-08-28) x86_64 GNU/Linux`
- Processeurs : 4 vCPU
- RAM : 4 Go
- Mount :

```
/dev/vda1 on / type ext4 (rw,relatime,errors=remount-ro)
/dev/vdb on /srv type ext4 (rw,relatime)
/dev/vdc on /var type ext4 (rw,relatime)
```

- DF :

```
root@tiree:~# df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            2.0G     0  2.0G   0% /dev
tmpfs           395M  576K  395M   1% /run
/dev/vda1       4.9G  1.4G  3.2G  31% /
tmpfs           2.0G  8.0K  2.0G   1% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           2.0G     0  2.0G   0% /sys/fs/cgroup
/dev/vdb         40G   15G   23G  39% /srv
/dev/vdc        9.8G  680M  8.7G   8% /var
tmpfs           395M     0  395M   0% /run/user/2058
```

# Système

```
apt update
apt upgrade
apt install ca-certificates apt-transport-https whois
apt install curl sudo unzip vim
```

# Dépendances
## Certbot
```
apt install certbot python-certbot-nginx
```

## Node.js v10.x
```
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt install -y nodejs
```

## Yarn
```
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
apt update
apt install yarn
```

## Autre
```
apt update
apt install nginx ffmpeg  openssl g++ make git python-dev npm wget
ffmpeg -version # Doit être >= 4.x
g++ -v # Doit être >= 5.x
```

# Redis
```
apt update
apt install redis-server
systemctl start redis
```

# Postgresql
```
apt update
apt install postgresql postgresql-contrib
systemctl start postgresql
```

# Peertube

## Utilisateur `peertube`

```
useradd -m -d /var/www/peertube -s /bin/bash -p peertube peertube
passwd peertube
mkdir -p /srv/peertube/{config,storage,versions}
chown -R peertube: /srv/peertube/
ln -s /srv/peertube/*/ /var/www/peertube/
```

Ajouter les droits postgres à l’utilisateur peertube:

```
sudo -u postgres createuser -P peertube
sudo -u postgres createdb -O peertube peertube_prod
sudo -u postgres psql -c "CREATE EXTENSION pg_trgm;" peertube_prod
sudo -u postgres psql -c "CREATE EXTENSION unaccent;" peertube_prod
```

## Installation
Télécharger la dernière version

```
VERSION=$(curl -s https://api.github.com/repos/chocobozzz/peertube/releases/latest | grep tag_name | cut -d '"' -f 4) && echo "Latest Peertube version is $VERSION"
cd /var/www/peertube/versions
wget -q "https://github.com/Chocobozzz/PeerTube/releases/download/${VERSION}/peertube-${VERSION}.zip"
unzip peertube-${VERSION}.zip && sudo -u peertube rm peertube-${VERSION}.zip
cd /var/www/peertube/ && sudo -u peertube ln -s versions/peertube-${VERSION} ./peertube-latest
cd ./peertube-latest && sudo -H -u peertube yarn install --production --pure-lockfile
```

## Configuration
Copier le fichier d’exemple.

```
cd /var/www/peertube && sudo -u peertube cp peertube-latest/config/production.yaml.example config/production.yaml
```

Éditer la configuration

```
root@tiree:/var/www/peertube# diff /var/www/peertube/versions/peertube-v1.4.1/config/production.yaml.example /var/www/peertube/config/production.yaml
8c8
<   hostname: 'example.com'
---
>   hostname: 'tube.fdn.fr'
41c41
<   password: 'peertube'
---
>   password: "CRYPTED!"
115,119c115,119
< #      -
< #        size: '10GB'
< #        # Minimum time the video must remain in the cache. Only accept values > 10 hours (to not overload remote instances)
< #        min_lifetime: '48 hours'
< #        strategy: 'trending' # Cache trending videos
---
>       -
>         size: '10GB'
>         # Minimum time the video must remain in the cache. Only accept values > 10 hours (to not overload remote instances)
>         min_lifetime: '48 hours'
>         strategy: 'trending' # Cache trending videos
```

## Nginx
Copier puis éditer le vhost

```
sudo cp /var/www/peertube/peertube-latest/support/nginx/peertube /etc/nginx/sites-available/peertube
root@tiree:/var/www/peertube# diff /var/www/peertube/peertube-latest/support/nginx/peertube /etc/nginx/sites-available/peertube 
4c4
<   server_name peertube.example.com;
---
>   server_name tube.fdn.fr;
19c19
<   server_name peertube.example.com;
---
>   server_name tube.fdn.fr;
22,23c22,23
<   ssl_certificate      /etc/letsencrypt/live/peertube.example.com/fullchain.pem;
<   ssl_certificate_key  /etc/letsencrypt/live/peertube.example.com/privkey.pem;
---
>   ssl_certificate      /etc/letsencrypt/live/tube.fdn.fr/fullchain.pem;
>   ssl_certificate_key  /etc/letsencrypt/live/tube.fdn.fr/privkey.pem;
29c29
<   # ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0, not compatible with import-videos script
---
>   ssl_ecdh_curve secp384r1; # Requires nginx >= 1.1.0, not compatible with import-videos script
51c51
<   #add_header Strict-Transport-Security "max-age=63072000; includeSubDomains";
---
>   add_header Strict-Transport-Security "max-age=63072000; includeSubDomains";
```

Puis l’activer:

```
ln -s /etc/nginx/sites-available/peertube /etc/nginx/sites-enabled/peertube
```

## Letsencrypt

Création du certificat

```
systemctl stop nginx
certbot certonly --authenticator nginx --installer nginx --agree-tos -d tube.fdn.fr
systemctl start nginx
```

# TCP/IP Tuning

```
cp /var/www/peertube/peertube-latest/support/sysctl.d/30-peertube-tcp.conf /etc/sysctl.d/
sysctl -p /etc/sysctl.d/30-peertube-tcp.conf
```

# Systemd

```
cp /var/www/peertube/peertube-latest/support/systemd/peertube.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now peertube
```
