**fail2ban**
*  apt-get install fail2ban

/etc/fail2ban/jail.local

```
[proxmox]
enabled = true
port = https,http,8006
filter = proxmox
logpath = /var/log/daemon.log
maxretry = 3
# 1 hour
bantime = 3600
```

/etc/fail2ban/filter.d/proxmox.conf 

```
[Definition]
failregex = pvedaemon\[.*authentication failure; rhost=<HOST> user=.* msg=.*
ignoreregex =
```

systemctl restart fail2ban

Proof:
iptables -L -n -v
```
Chain INPUT (policy ACCEPT 73 packets, 5132 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    54  8141 f2b-proxmox  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            multiport dports 443,80,8006
       79  5044 f2b-sshd   tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            multiport dports 22

       Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
        pkts bytes target     prot opt in     out     source               destination         

        Chain OUTPUT (policy ACCEPT 54 packets, 4674 bytes)
         pkts bytes target     prot opt in     out     source               destination         

         Chain f2b-proxmox (1 references)
          pkts bytes target     prot opt in     out     source               destination         
              4   240 REJECT     all  --  *      *       80.67.177.123        0.0.0.0/0            reject-with icmp-port-unreachable
                 50  7901 RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0           

                 Chain f2b-sshd (1 references)
                  pkts bytes target     prot opt in     out     source               destination         
                      0     0 REJECT     all  --  *      *       34.90.27.142         0.0.0.0/0            reject-with icmp-port-unreachable
                         79  5044 RETURN     all  --  *      *       0.0.0.0/0            0.0.0.0/0  
                         ```         