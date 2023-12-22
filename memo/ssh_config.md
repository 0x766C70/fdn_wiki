Voici un exemple de fichier de configuration renforcée de client à placer dans `~/.ssh/config`:

```
#Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512,diffie-hellman-group18-sha512,diffie-hellman-group-exchange-sha256
MACs hmac-sha2-256-etm@openssh.com,hmac-sha2-512-etm@openssh.com,umac-128-etm@openssh.com
HostKeyAlgorithms ssh-ed25519,ssh-ed25519-cert-v01@openssh.com,sk-ssh-ed25519@openssh.com,sk-ssh-ed25519-cert-v01@openssh.com,rsa-sha2-256,rsa-sha2-256-cert-v01@openssh.com,rsa-sha2-512,rsa-sha2-512-cert-v01@openssh.com

# Utile si l'empreinte des clés se trouvent dans le DNS
#VerifyHostKeyDNS yes

# Permet l'utilisation de Kerberos
#GSSAPIAuthentication yes
#GSSAPIDelegateCredentials yes

# Permet de réutiliser une connexion préexistante
Host *
  ControlMaster auto
  ControlPath ~/.ssh/%h-%p-%r
  ControlPersist 10
```

:warning: Cette configuration renforcé peut empêcher la connexion sur d'ancienne machine ne supportant pas les ciphers renforcés. Il est possible de modifier la configuration pour un host sécifique.