# Les tests à faire

## Arrêter (puis redémarrer) un noeud

### Arrêter l'esclave proprement

    root@r2d2:~# gnt-cluster getmaster
    r2d2.fdn.fr
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83521, 83522
    Waiting for job 83521 ...
    Sat May 25 00:07:27 2013 * Verifying cluster config
    Sat May 25 00:07:27 2013 * Verifying cluster certificate files
    Sat May 25 00:07:27 2013 * Verifying hypervisor parameters
    Sat May 25 00:07:27 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83522 ...
    Sat May 25 00:07:28 2013 * Verifying group 'default'
    Sat May 25 00:07:28 2013 * Gathering data (2 nodes)
    Sat May 25 00:07:28 2013 * Gathering disk information (2 nodes)
    Sat May 25 00:07:28 2013 * Verifying configuration file consistency
    Sat May 25 00:07:28 2013 * Verifying node status
    Sat May 25 00:07:28 2013 * Verifying instance status
    Sat May 25 00:07:28 2013 * Verifying orphan volumes
    Sat May 25 00:07:28 2013 * Verifying N+1 Memory redundancy
    Sat May 25 00:07:29 2013 * Other Notes
    Sat May 25 00:07:29 2013 * Hooks Results
    root@r2d2:~# ssh c3po poweroff
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83524, 83525
    Waiting for job 83524 ...
    Sat May 25 00:08:45 2013 * Verifying cluster config
    Sat May 25 00:08:45 2013 * Verifying cluster certificate files
    Sat May 25 00:08:45 2013 * Verifying hypervisor parameters
    Sat May 25 00:08:45 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83525 ...
    Sat May 25 00:08:51 2013 * Verifying group 'default'
    Sat May 25 00:08:51 2013 * Gathering data (2 nodes)
    Sat May 25 00:08:57 2013 * Gathering disk information (2 nodes)
    Sat May 25 00:09:00 2013   - ERROR: node c3po.fdn.fr: while getting disk information: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Sat May 25 00:09:00 2013 * Verifying configuration file consistency
    Sat May 25 00:09:00 2013   - ERROR: node c3po.fdn.fr: Node did not return file checksum data
    Sat May 25 00:09:00 2013 * Verifying node status
    Sat May 25 00:09:00 2013   - ERROR: node c3po.fdn.fr: while contacting node: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Sat May 25 00:09:00 2013   - ERROR: node r2d2.fdn.fr: ssh communication with node 'c3po.fdn.fr': ssh problem: ssh: connect to host c3po.fdn.fr port 22: No route to host\'r\n
    Sat May 25 00:09:00 2013   - ERROR: node r2d2.fdn.fr: tcp communication with node 'c3po.fdn.fr': failure using the primary interface(s)
    Sat May 25 00:09:00 2013 * Verifying instance status
    Sat May 25 00:09:00 2013   - ERROR: instance paploo.fdn.fr: instance not running on its primary node c3po.fdn.fr
    Sat May 25 00:09:00 2013   - ERROR: instance paploo.fdn.fr: couldn't retrieve status for disk/0 on c3po.fdn.fr: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Sat May 25 00:09:00 2013   - ERROR: node c3po.fdn.fr: instance paploo.fdn.fr, connection to primary node failed
    Sat May 25 00:09:00 2013 * Verifying orphan volumes
    Sat May 25 00:09:00 2013 * Verifying N+1 Memory redundancy
    Sat May 25 00:09:00 2013 * Other Notes
    Sat May 25 00:09:03 2013  - WARNING: Communication failure to node c3po.fdn.fr: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Sat May 25 00:09:03 2013 * Hooks Results
    Sat May 25 00:09:03 2013   - ERROR: node c3po.fdn.fr: Communication failure in hooks execution: Error 7: Failed connect to 80.67.169.48:1811; No route to host

Puis, une fois l'esclave redémarré :

    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83529, 83530
    Waiting for job 83529 ...
    Sat May 25 00:10:43 2013 * Verifying cluster config
    Sat May 25 00:10:43 2013 * Verifying cluster certificate files
    Sat May 25 00:10:43 2013 * Verifying hypervisor parameters
    Sat May 25 00:10:43 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83530 ...
    Sat May 25 00:10:43 2013 * Verifying group 'default'
    Sat May 25 00:10:43 2013 * Gathering data (2 nodes)
    Sat May 25 00:10:44 2013 * Gathering disk information (2 nodes)
    Sat May 25 00:10:45 2013 * Verifying configuration file consistency
    Sat May 25 00:10:45 2013 * Verifying node status
    Sat May 25 00:10:45 2013   - ERROR: node c3po.fdn.fr: drbd minor 0 of instance paploo.fdn.fr is not active
    Sat May 25 00:10:45 2013 * Verifying instance status
    Sat May 25 00:10:45 2013   - ERROR: instance paploo.fdn.fr: instance not running on its primary node c3po.fdn.fr
    Sat May 25 00:10:45 2013   - ERROR: instance paploo.fdn.fr: couldn't retrieve status for disk/0 on c3po.fdn.fr: Can't find device <DRBD8(hosts=r2d2.fdn.fr/0-c3po.fdn.fr/0, port=11009, configured as 80.67.169.48:11009 80.67.169.49:11009, backend=<LogicalVolume(/dev/vg1/d868ee5b-0887-4d4e-9289-f209f9243d45.disk0_data, not visible, size=2048m)>, metadev=<LogicalVolume(/dev/vg1/d868ee5b-0887-4d4e-9289-f209f9243d45.disk0_meta, not visible, size=128m)>, visible as /dev/disk/0, size=2048m)>
    Sat May 25 00:10:45 2013 * Verifying orphan volumes
    Sat May 25 00:10:45 2013 * Verifying N+1 Memory redundancy
    Sat May 25 00:10:45 2013 * Other Notes
    Sat May 25 00:10:45 2013 * Hooks Results

Et quelques minutes plus tard après le passage de *ganeti-watcher* :

    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83535, 83536
    Waiting for job 83535 ...
    Sat May 25 00:17:53 2013 * Verifying cluster config
    Sat May 25 00:17:53 2013 * Verifying cluster certificate files
    Sat May 25 00:17:53 2013 * Verifying hypervisor parameters
    Sat May 25 00:17:53 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83536 ...
    Sat May 25 00:17:53 2013 * Verifying group 'default'
    Sat May 25 00:17:53 2013 * Gathering data (2 nodes)
    Sat May 25 00:17:54 2013 * Gathering disk information (2 nodes)
    Sat May 25 00:17:54 2013 * Verifying configuration file consistency
    Sat May 25 00:17:54 2013 * Verifying node status
    Sat May 25 00:17:54 2013 * Verifying instance status
    Sat May 25 00:17:54 2013 * Verifying orphan volumes
    Sat May 25 00:17:54 2013 * Verifying N+1 Memory redundancy
    Sat May 25 00:17:54 2013 * Other Notes
    Sat May 25 00:17:54 2013 * Hooks Results

### Arrêter le maître proprement

#### Redémarrage sans failover

RAS, voir le paragraphe sur *ganeti-watcher*.

#### Redémarrage après failover

Scénario : on arrête le maître (*r2d2*) avec une VM active. On force *c3po* à devenir maître :

    gnt-cluster master-failover --no-voting

Après ça, *ganeti-watcher* essaie de remettre la VM en face des trous mais ça chouine parce qu'il ne peut pas parler à *r2d2*. On peut quand même remonter la VM (dans l'exemple, *paploo*) sur *c3po* :

    gnt-instance failover --ignore-consistency paploo.fdn.fr

Après ça, la VM remonte sur le secondaire *c3po*.

Une fois *r2d2* rallumé, il ne se rattache pas au cluster, du coup on ne risque pas de blague avec une VM qui remonte toute seule et qui met son DRBD en vrac. Pour remettre *r2d2* en face des trous, sur *c3po* (le «nouveau» maître, celui qui a la VM qui tourne) :

    gnt-cluster redist-conf

On peut s'assurer que tout est bien revenu :

    gnt-cluster verify

### Arrêter le maître ou l'esclave à la hache

**Pas (encore) testé** mais a priori ça marche pareil qu'en cas d'arrêt propre.

# Les tests déjà faits

## gnt-cluster verify

### Sur un cluster vierge

    root@r2d2:~# gnt-cluster verify
    Submitted jobs 69461, 69462
    Waiting for job 69461 ...
    Tue Apr 30 19:21:52 2013 * Verifying cluster config
    Tue Apr 30 19:21:52 2013 * Verifying cluster certificate files
    Tue Apr 30 19:21:52 2013 * Verifying hypervisor parameters
    Tue Apr 30 19:21:52 2013 * Verifying all nodes belong to an existing group
    Waiting for job 69462 ...
    Tue Apr 30 19:21:53 2013 * Verifying group 'default'
    Tue Apr 30 19:21:53 2013 * Gathering data (2 nodes)
    Tue Apr 30 19:21:53 2013 * Gathering disk information (2 nodes)
    Tue Apr 30 19:21:53 2013 * Verifying configuration file consistency
    Tue Apr 30 19:21:53 2013 * Verifying node status
    Tue Apr 30 19:21:53 2013 * Verifying instance status
    Tue Apr 30 19:21:53 2013 * Verifying orphan volumes
    Tue Apr 30 19:21:53 2013 * Verifying N+1 Memory redundancy
    Tue Apr 30 19:21:53 2013 * Other Notes
    Tue Apr 30 19:21:53 2013 * Hooks Results

## burnin

On part d'un cluster vierge.

    root@r2d2:~# /usr/lib/ganeti/tools/burnin -o debootstrap+wheezy64 --disk-size 1G -p \
    > teebo.fdn.fr paploo.fdn.fr chirpa.fdn.fr
  - Testing global parameters
  - Creating instances
    * instance teebo.fdn.fr
      on c3po.fdn.fr, r2d2.fdn.fr
    * instance paploo.fdn.fr
      on r2d2.fdn.fr, c3po.fdn.fr
    * instance chirpa.fdn.fr
      on c3po.fdn.fr, r2d2.fdn.fr
    Submitted jobs 69465, 69466, 69467
    Waiting for job 69465 for teebo.fdn.fr ...
    Waiting for job 69466 for paploo.fdn.fr ...
    Waiting for job 69467 for chirpa.fdn.fr ...
  - Replacing disks on the same nodes
    * instance teebo.fdn.fr
      run replace_on_secondary
      run replace_on_primary
    * instance paploo.fdn.fr
      run replace_on_secondary
      run replace_on_primary
    * instance chirpa.fdn.fr
      run replace_on_secondary
      run replace_on_primary
    Submitted jobs 69469, 69470, 69471
    Waiting for job 69469 for teebo.fdn.fr ...
    Waiting for job 69470 for paploo.fdn.fr ...
    Waiting for job 69471 for chirpa.fdn.fr ...
  - Growing disks
    * instance teebo.fdn.fr
      increase disk/0 by 128 MB
    * instance paploo.fdn.fr
      increase disk/0 by 128 MB
    * instance chirpa.fdn.fr
      increase disk/0 by 128 MB
    Submitted jobs 69473, 69474, 69475
    Waiting for job 69473 for teebo.fdn.fr ...
    Waiting for job 69474 for paploo.fdn.fr ...
    Waiting for job 69475 for chirpa.fdn.fr ...
  - Failing over instances
    * instance teebo.fdn.fr
    * instance paploo.fdn.fr
    * instance chirpa.fdn.fr
    Submitted jobs 69476, 69477, 69478
    Waiting for job 69476 for teebo.fdn.fr ...
    Waiting for job 69478 for chirpa.fdn.fr ...
    Waiting for job 69477 for paploo.fdn.fr ...
  - Migrating instances
    * instance teebo.fdn.fr
      migration and migration cleanup
    * instance paploo.fdn.fr
      migration and migration cleanup
    * instance chirpa.fdn.fr
      migration and migration cleanup
    Submitted jobs 69479, 69480, 69481
    Waiting for job 69479 for teebo.fdn.fr ...
    Waiting for job 69480 for paploo.fdn.fr ...
    Waiting for job 69481 for chirpa.fdn.fr ...
  - Exporting and re-importing instances
    * instance teebo.fdn.fr
      export to node c3po.fdn.fr
      remove instance
      import from c3po.fdn.fr to c3po.fdn.fr, r2d2.fdn.fr
      remove export
    * instance paploo.fdn.fr
      export to node r2d2.fdn.fr
      remove instance
      import from r2d2.fdn.fr to r2d2.fdn.fr, c3po.fdn.fr
      remove export
    * instance chirpa.fdn.fr
      export to node c3po.fdn.fr
      remove instance
      import from c3po.fdn.fr to c3po.fdn.fr, r2d2.fdn.fr
      remove export
    Submitted jobs 69485, 69486, 69487
    Waiting for job 69485 for teebo.fdn.fr ...
    Waiting for job 69486 for paploo.fdn.fr ...
    Waiting for job 69487 for chirpa.fdn.fr ...
  - Reinstalling instances
    * instance teebo.fdn.fr
      reinstall without passing the OS
      reinstall specifying the OS
    * instance paploo.fdn.fr
      reinstall without passing the OS
      reinstall specifying the OS
    * instance chirpa.fdn.fr
      reinstall without passing the OS
      reinstall specifying the OS
    Submitted jobs 69490, 69491, 69492
    Waiting for job 69490 for teebo.fdn.fr ...
    Waiting for job 69491 for paploo.fdn.fr ...
    Waiting for job 69492 for chirpa.fdn.fr ...
  - Rebooting instances
    * instance teebo.fdn.fr
      reboot with type 'hard'
      reboot with type 'soft'
      reboot with type 'full'
    * instance paploo.fdn.fr
      reboot with type 'hard'
      reboot with type 'soft'
      reboot with type 'full'
    * instance chirpa.fdn.fr
      reboot with type 'hard'
      reboot with type 'soft'
      reboot with type 'full'
    Submitted jobs 69495, 69496, 69497
    Waiting for job 69495 for teebo.fdn.fr ...
    Waiting for job 69496 for paploo.fdn.fr ...
    Waiting for job 69497 for chirpa.fdn.fr ...
  - Adding and removing disks
    * instance teebo.fdn.fr
      adding a disk
      removing last disk
    * instance paploo.fdn.fr
      adding a disk
      removing last disk
    * instance chirpa.fdn.fr
      adding a disk
      removing last disk
    Submitted jobs 69498, 69499, 69500
    Waiting for job 69498 for teebo.fdn.fr ...
    Waiting for job 69499 for paploo.fdn.fr ...
    Waiting for job 69500 for chirpa.fdn.fr ...
  - Adding and removing NICs
    * instance teebo.fdn.fr
      adding a NIC
      removing last NIC
    * instance paploo.fdn.fr
      adding a NIC
      removing last NIC
    * instance chirpa.fdn.fr
      adding a NIC
      removing last NIC
    Submitted jobs 69503, 69504, 69505
    Waiting for job 69503 for teebo.fdn.fr ...
    Waiting for job 69504 for paploo.fdn.fr ...
    Waiting for job 69505 for chirpa.fdn.fr ...
  - Activating/deactivating disks
    * instance teebo.fdn.fr
      activate disks when online
      activate disks when offline
      deactivate disks (when offline)
    * instance paploo.fdn.fr
      activate disks when online
      activate disks when offline
      deactivate disks (when offline)
    * instance chirpa.fdn.fr
      activate disks when online
      activate disks when offline
      deactivate disks (when offline)
    Submitted jobs 69506, 69507, 69508
    Waiting for job 69506 for teebo.fdn.fr ...
    Waiting for job 69507 for paploo.fdn.fr ...
    Waiting for job 69508 for chirpa.fdn.fr ...
  - Checking confd results
    * Ping: OK
    * Master: OK
    * Node role for master: OK
  - Stopping and starting instances
    * instance teebo.fdn.fr
    * instance paploo.fdn.fr
    * instance chirpa.fdn.fr
    Submitted jobs 69509, 69510, 69511
    Waiting for job 69509 for teebo.fdn.fr ...
    Waiting for job 69510 for paploo.fdn.fr ...
    Waiting for job 69511 for chirpa.fdn.fr ...
  - Removing instances
    * instance teebo.fdn.fr
    * instance paploo.fdn.fr
    * instance chirpa.fdn.fr
    Submitted jobs 69512, 69513, 69514
    Waiting for job 69512 for teebo.fdn.fr ...
    Waiting for job 69513 for paploo.fdn.fr ...
    Waiting for job 69514 for chirpa.fdn.fr ...

## Créer une VM

  * Départ avec un cluster vierge.
  * Monter une VM.
  * Vérifier qu'on peut s'y connecter sur la console.
  * Vérifier que son réseau est up.
  * Vérifier qu'on peut s'y connecter en SSH.

    root@r2d2:~# gnt-instance list
    Instance Hypervisor OS Primary_node Status Memory
    root@r2d2:~# gnt-instance add -I hail -s 2G -t drbd -o debootstrap+wheezy32 teebo.fdn.fr
    Thu May  2 14:15:17 2013  - INFO: Selected nodes for instance teebo.fdn.fr via iallocator hail: c3po.fdn.fr, r2d2.fdn.fr
    Thu May  2 14:15:18 2013 * creating instance disks...
    Thu May  2 14:15:24 2013 adding instance teebo.fdn.fr to cluster config
    Thu May  2 14:15:27 2013 * wiping instance disks...
    Thu May  2 14:15:28 2013  - INFO: * Wiping disk 0
    Thu May  2 14:15:33 2013  - INFO:  - done: 10.0% ETA: 45s
    Thu May  2 14:16:19 2013  - INFO: Waiting for instance teebo.fdn.fr to sync disks.
    Thu May  2 14:16:19 2013  - INFO: Instance teebo.fdn.fr's disks are in sync.
    Thu May  2 14:16:19 2013 * running the instance OS create scripts...
    Thu May  2 14:20:04 2013 * starting instance...
    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 c3po.fdn.fr  running   512M
    root@r2d2:~# gnt-instance console teebo.fdn.fr
  
    Debian GNU/Linux 7.0 teebo.fdn.fr ttyS0
  
    teebo login: root
    Linux teebo.fdn.fr 3.2.0-4-686-pae #1 SMP Debian 3.2.41-2 i686
  
    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.
  
    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    root@teebo:~# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 16436 qdisc noqueue state UNKNOWN 
      link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
      inet 127.0.0.1/8 scope host lo
      inet6 ::1/128 scope host 
         valid_lft forever preferred_lft forever
    2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
      link/ether aa:00:00:94:19:2a brd ff:ff:ff:ff:ff:ff
      inet 80.67.169.52/25 brd 80.67.169.127 scope global eth0
      inet6 2001:910:800::52/64 scope global 
         valid_lft forever preferred_lft forever
      inet6 fe80::a800:ff:fe94:192a/64 scope link 
         valid_lft forever preferred_lft forever
    root@teebo:~# ping -c3 www.glou.org
    PING www.glou.org (80.67.176.33) 56(84) bytes of data.
    64 bytes from pousse.glou.org (80.67.176.33): icmp_req=1 ttl=63 time=50.1 ms
    64 bytes from pousse.glou.org (80.67.176.33): icmp_req=2 ttl=63 time=42.2 ms
    64 bytes from pousse.glou.org (80.67.176.33): icmp_req=3 ttl=63 time=43.5 ms
  
  --- www.glou.org ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2002ms
    rtt min/avg/max/mdev = 42.211/45.302/50.126/3.464 ms
    root@teebo:~# ping6 -c3 www.glou.org
    PING www.glou.org(pousse.glou.org) 56 data bytes
    64 bytes from pousse.glou.org: icmp_seq=1 ttl=63 time=51.4 ms
    64 bytes from pousse.glou.org: icmp_seq=2 ttl=63 time=42.2 ms
    64 bytes from pousse.glou.org: icmp_seq=3 ttl=63 time=41.9 ms
  
  --- www.glou.org ping statistics ---
    3 packets transmitted, 3 received, 0% packet loss, time 2002ms
    rtt min/avg/max/mdev = 41.996/45.213/51.442/4.405 ms
    root@teebo:~# Connection to c3po.fdn.fr closed.
    root@r2d2:~# ssh -o stricthostkeychecking=no -o UserKnownHostsFile=/dev/null root@teebo
    Warning: Permanently added 'teebo,80.67.169.52' (ECDSA) to the list of known hosts.
    Linux teebo.fdn.fr 3.2.0-4-686-pae #1 SMP Debian 3.2.41-2 i686
  
    The programs included with the Debian GNU/Linux system are free software;
    the exact distribution terms for each program are described in the
    individual files in /usr/share/doc/*/copyright.
  
    Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
    permitted by applicable law.
    Last login: Thu May  2 12:20:24 2013
    root@teebo:~# logout
    Connection to teebo closed.

Note au 2 mai 2013 : ça marche bien avec Wheezy (les OS *debootstrap+wheezy32* et *debootstrap+wheezy64*, et *debootstrap+default* qui est un alias de ce dernier), par contre Sid ne s'installe pas. À voir quand on aura le temps si quelqu'un juge ça important.

## gnt-cluster verify avec des VM

    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 c3po.fdn.fr  running   512M
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 70539, 70540
    Waiting for job 70539 ...
    Thu May  2 14:26:08 2013 * Verifying cluster config
    Thu May  2 14:26:08 2013 * Verifying cluster certificate files
    Thu May  2 14:26:08 2013 * Verifying hypervisor parameters
    Thu May  2 14:26:08 2013 * Verifying all nodes belong to an existing group
    Waiting for job 70540 ...
    Thu May  2 14:26:08 2013 * Verifying group 'default'
    Thu May  2 14:26:08 2013 * Gathering data (2 nodes)
    Thu May  2 14:26:08 2013 * Gathering disk information (2 nodes)
    Thu May  2 14:26:09 2013 * Verifying configuration file consistency
    Thu May  2 14:26:09 2013 * Verifying node status
    Thu May  2 14:26:09 2013 * Verifying instance status
    Thu May  2 14:26:09 2013 * Verifying orphan volumes
    Thu May  2 14:26:09 2013 * Verifying N+1 Memory redundancy
    Thu May  2 14:26:09 2013 * Other Notes
    Thu May  2 14:26:09 2013 * Hooks Results

## Migrer une VM d'un socle à l'autre

### Du maître à l'esclave

    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 r2d2.fdn.fr  running   512M
    root@r2d2:~# gnt-instance migrate teebo.fdn.fr
    Instance teebo.fdn.fr will be migrated. Note that migration might
    impact the instance if anything goes wrong (e.g. due to bugs in the
    hypervisor). Continue?
    y/[n]/?: y
    Thu May  2 14:29:17 2013 Migrating instance teebo.fdn.fr
    Thu May  2 14:29:17 2013 * checking disk consistency between source and target
    Thu May  2 14:29:17 2013 * switching node c3po.fdn.fr to secondary mode
    Thu May  2 14:29:17 2013 * changing into standalone mode
    Thu May  2 14:29:17 2013 * changing disks into dual-master mode
    Thu May  2 14:29:19 2013 * wait until resync is done
    Thu May  2 14:29:19 2013 * preparing c3po.fdn.fr to accept the instance
    Thu May  2 14:29:19 2013 * migrating instance to c3po.fdn.fr
    Thu May  2 14:29:24 2013 * switching node r2d2.fdn.fr to secondary mode
    Thu May  2 14:29:24 2013 * wait until resync is done
    Thu May  2 14:29:25 2013 * changing into standalone mode
    Thu May  2 14:29:25 2013 * changing disks into single-master mode
    Thu May  2 14:29:26 2013 * wait until resync is done
    Thu May  2 14:29:26 2013 * done
    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 c3po.fdn.fr  running   512M

### De l'esclave au maître

    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 c3po.fdn.fr  running   512M
    root@r2d2:~# gnt-instance migrate teebo.fdn.fr
    Instance teebo.fdn.fr will be migrated. Note that migration might
    impact the instance if anything goes wrong (e.g. due to bugs in the
    hypervisor). Continue?
    y/[n]/?: y
    Thu May  2 14:28:29 2013 Migrating instance teebo.fdn.fr
    Thu May  2 14:28:29 2013 * checking disk consistency between source and target
    Thu May  2 14:28:29 2013 * switching node r2d2.fdn.fr to secondary mode
    Thu May  2 14:28:29 2013 * changing into standalone mode
    Thu May  2 14:28:30 2013 * changing disks into dual-master mode
    Thu May  2 14:28:31 2013 * wait until resync is done
    Thu May  2 14:28:31 2013 * preparing r2d2.fdn.fr to accept the instance
    Thu May  2 14:28:31 2013 * migrating instance to r2d2.fdn.fr
    Thu May  2 14:28:37 2013 * switching node c3po.fdn.fr to secondary mode
    Thu May  2 14:28:37 2013 * wait until resync is done
    Thu May  2 14:28:37 2013 * changing into standalone mode
    Thu May  2 14:28:37 2013 * changing disks into single-master mode
    Thu May  2 14:28:38 2013 * wait until resync is done
    Thu May  2 14:28:39 2013 * done
    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 r2d2.fdn.fr  running   512M

## Détruire une VM

  * Départ avec une VM qui tourne.
  * gnt-instance remove la.vm
  * Vérifier qu'elle a bien disparu.

    root@r2d2:~# gnt-instance list
    Instance     Hypervisor OS                   Primary_node Status  Memory
    teebo.fdn.fr kvm        debootstrap+wheezy32 c3po.fdn.fr  running   512M
    root@r2d2:~# gnt-instance remove teebo.fdn.fr
    This will remove the volumes of the instance teebo.fdn.fr (including
    mirrors), thus removing all the data of the instance. Continue?
    y/[n]/?: y
    root@r2d2:~# gnt-instance list
    Instance Hypervisor OS Primary_node Status Memory

## Changer de noeud d'admin

  * Départ avec *r2d2* master.
  * Lancer un *ping droides.fdn.fr*
  * *gnt-cluster master-failover*
  * Vérifier que la VIP a bien disparu sur *r2d2* et qu'elle est remotée sur *c3po*.
  * Regarder si le ping a perdu des paquets.

### Avec les deux noeuds en fonctionnement nominal

#### Sur le maître

    root@r2d2:~# gnt-cluster getmaster
    r2d2.fdn.fr
    root@r2d2:~# gnt-cluster master-failover
    Failure: prerequisites not met for this operation:
    error type: wrong_input, error details:
    This commands must be run on the node where you want the new master to be. r2d2.fdn.fr is already the master

Il faut lancer la commande depuis l'esclave.

#### Sur l'esclave

    root@c3po:~# gnt-cluster getmaster 
    r2d2.fdn.fr
    root@c3po:~# gnt-cluster master-failover
    root@c3po:~# gnt-cluster getmaster 
    c3po.fdn.fr
    root@c3po:~# ip a sh dev br0
    4: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
      link/ether 00:25:90:78:90:33 brd ff:ff:ff:ff:ff:ff
      inet 80.67.169.48/25 brd 80.67.169.127 scope global br0
      inet 80.67.169.50/32 scope global br0:0
      inet6 2001:910:800::48/64 scope global 
         valid_lft forever preferred_lft forever
      inet6 fe80::225:90ff:fe78:9033/64 scope link 
         valid_lft forever preferred_lft forever

Les résultats du ping :

   droides.fdn.fr ping statistics ---
    24 packets transmitted, 18 received, 25% packet loss, time 23065ms
    rtt min/avg/max/mdev = 41.530/42.624/44.721/0.736 ms

Et sur l'ancien maître :

    root@r2d2:~# ip a sh dev br0
    4: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
      link/ether 00:25:90:78:7a:34 brd ff:ff:ff:ff:ff:ff
      inet 80.67.169.49/25 brd 80.67.169.127 scope global br0
      inet6 2001:910:800::49/64 scope global 
         valid_lft forever preferred_lft forever
      inet6 fe80::225:90ff:fe78:7a34/64 scope link 
         valid_lft forever preferred_lft forever


### Sans ganeti-noded sur le maître

Sur le maître :

    root@c3po:~# ps aufx|grep [g]aneti
    root@c3po:~# 

Sur l'esclave :

    root@r2d2:~# gnt-cluster getmaster
    c3po.fdn.fr
    root@r2d2:~# gnt-cluster master-failover
    Failure: prerequisites not met for this operation:
    error type: environment_error, error details:
    Cluster is inconsistent, most nodes did not respond.

### Sans ganeti-noded sur l'esclave

    root@r2d2:~# /etc/init.d/ganeti stop
    [ ok ] Stopping Ganeti cluster:[....] ganeti-confd...done.
    [ ok ] ganeti-rapi...done.
    [ ok ] ganeti-masterd...done.
    [ ok ] ganeti-noded...done.
    root@r2d2:~# gnt-cluster getmaster
    c3po.fdn.fr
    root@r2d2:~# gnt-cluster master-failover 
    root@r2d2:~# gnt-cluster getmaster
    c3po.fdn.fr
    root@r2d2:~# ps aufx|grep [g]aneti
    root@r2d2:~# 

**Attention**, ça casse tout ! Après cette manip, la VIP a disparu et chacun des noeuds croit que l'autre est maître.
    root@r2d2:~# gnt-cluster master-failover
    Failure: prerequisites not met for this operation:
    error type: wrong_state, error details:
    I have a wrong configuration, I believe the master is c3po.fdn.fr but the other nodes voted r2d2.fdn.fr. Please resync the configuration of this node.

Pour s'en tirer :

    root@r2d2:~# gnt-cluster master-failover --no-voting
    This will perform the failover even if most other nodes are down, or
    if this node is outdated. This is dangerous as it can lead to a non-
    consistent cluster. Check the gnt-cluster(8) man page before
    proceeding. Continue?
    y/[n]/?: y
    root@r2d2:~# gnt-cluster getmaster
    r2d2.fdn.fr
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 70583, 70584
    Waiting for job 70583 ...
    Thu May  2 16:03:42 2013 * Verifying cluster config
    Thu May  2 16:03:42 2013 * Verifying cluster certificate files
    Thu May  2 16:03:43 2013 * Verifying hypervisor parameters
    Thu May  2 16:03:43 2013 * Verifying all nodes belong to an existing group
    Waiting for job 70584 ...
    Thu May  2 16:03:43 2013 * Verifying group 'default'
    Thu May  2 16:03:43 2013 * Gathering data (2 nodes)
    Thu May  2 16:03:43 2013 * Gathering disk information (2 nodes)
    Thu May  2 16:03:44 2013 * Verifying configuration file consistency
    Thu May  2 16:03:44 2013 * Verifying node status
    Thu May  2 16:03:44 2013 * Verifying instance status
    Thu May  2 16:03:44 2013 * Verifying orphan volumes
    Thu May  2 16:03:44 2013 * Verifying N+1 Memory redundancy
    Thu May  2 16:03:44 2013 * Other Notes
    Thu May  2 16:03:44 2013 * Hooks Results

### Avec l'esclave arrêté

Pas possible, puisque c'est l'esclave qui lance la migration.

### Avec le maître arrêté

    root@r2d2:~# gnt-cluster getmaster
    c3po.fdn.fr
    root@r2d2:~# gnt-cluster master-failover --no-voting
    This will perform the failover even if most other nodes are down, or
    if this node is outdated. This is dangerous as it can lead to a non-
    consistent cluster. Check the gnt-cluster(8) man page before
    proceeding. Continue?
    y/[n]/?: y
    root@r2d2:~# gnt-cluster getmaster
    r2d2.fdn.fr
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83499, 83500
    Waiting for job 83499 ...
    Fri May 24 23:49:35 2013 * Verifying cluster config
    Fri May 24 23:49:35 2013 * Verifying cluster certificate files
    Fri May 24 23:49:35 2013 * Verifying hypervisor parameters
    Fri May 24 23:49:35 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83500 ...
    Fri May 24 23:49:41 2013 * Verifying group 'default'
    Fri May 24 23:49:41 2013 * Gathering data (2 nodes)
    Fri May 24 23:49:47 2013 * Gathering disk information (2 nodes)
    Fri May 24 23:49:50 2013   - ERROR: node c3po.fdn.fr: while getting disk information: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Fri May 24 23:49:50 2013 * Verifying configuration file consistency
    Fri May 24 23:49:50 2013   - ERROR: node c3po.fdn.fr: Node did not return file checksum data
    Fri May 24 23:49:50 2013 * Verifying node status
    Fri May 24 23:49:50 2013   - ERROR: node c3po.fdn.fr: while contacting node: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Fri May 24 23:49:50 2013   - ERROR: node r2d2.fdn.fr: ssh communication with node 'c3po.fdn.fr': ssh problem: ssh: connect to host c3po.fdn.fr port 22: No route to host\'r\n
    Fri May 24 23:49:50 2013   - ERROR: node r2d2.fdn.fr: tcp communication with node 'c3po.fdn.fr': failure using the primary interface(s)
    Fri May 24 23:49:51 2013 * Verifying instance status
    Fri May 24 23:49:51 2013   - ERROR: instance paploo.fdn.fr: instance not running on its primary node c3po.fdn.fr
    Fri May 24 23:49:51 2013   - ERROR: instance paploo.fdn.fr: couldn't retrieve status for disk/0 on c3po.fdn.fr: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Fri May 24 23:49:51 2013   - ERROR: node c3po.fdn.fr: instance paploo.fdn.fr, connection to primary node failed
    Fri May 24 23:49:51 2013 * Verifying orphan volumes
    Fri May 24 23:49:51 2013 * Verifying N+1 Memory redundancy
    Fri May 24 23:49:51 2013 * Other Notes
    Fri May 24 23:49:53 2013  - WARNING: Communication failure to node c3po.fdn.fr: Error 7: Failed connect to 80.67.169.48:1811; No route to host
    Fri May 24 23:49:53 2013 * Hooks Results
    Fri May 24 23:49:53 2013   - ERROR: node c3po.fdn.fr: Communication failure in hooks execution: Error 7: Failed connect to 80.67.169.48:1811; No route to host

À ce stade, on a un cluster boiteux mais fonctionnel. Problème : quand on rallume l'ancien maître (ici *c3po*), le cluster est dans un état incohérent.

    root@c3po:~# gnt-cluster getmaster
    c3po.fdn.fr
    root@c3po:~# gnt-cluster verify
    Cannot communicate with the master daemon.
    Is it running and listening for connections?

    root@r2d2:~# gnt-cluster getmaster
    r2d2.fdn.fr
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83507, 83508
    Waiting for job 83507 ...
    Fri May 24 23:54:28 2013 * Verifying cluster config
    Fri May 24 23:54:28 2013 * Verifying cluster certificate files
    Fri May 24 23:54:28 2013 * Verifying hypervisor parameters
    Fri May 24 23:54:28 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83508 ...
    Fri May 24 23:54:28 2013 * Verifying group 'default'
    Fri May 24 23:54:28 2013 * Gathering data (2 nodes)
    Fri May 24 23:54:29 2013 * Gathering disk information (2 nodes)
    Fri May 24 23:54:29 2013 * Verifying configuration file consistency
    Fri May 24 23:54:29 2013   - ERROR: cluster: File /var/lib/ganeti/config.data found with 2 different checksums (variant 1 on r2d2.fdn.fr; variant 2 on c3po.fdn.fr)
    Fri May 24 23:54:29 2013   - ERROR: cluster: File /var/lib/ganeti/ssconf_master_node found with 2 different checksums (variant 1 on c3po.fdn.fr; variant 2 on r2d2.fdn.fr)
    Fri May 24 23:54:29 2013 * Verifying node status
    Fri May 24 23:54:29 2013   - ERROR: node c3po.fdn.fr: drbd minor 0 of instance paploo.fdn.fr is not active
    Fri May 24 23:54:29 2013 * Verifying instance status
    Fri May 24 23:54:29 2013   - ERROR: instance paploo.fdn.fr: instance not running on its primary node c3po.fdn.fr
    Fri May 24 23:54:29 2013   - ERROR: instance paploo.fdn.fr: couldn't retrieve status for disk/0 on c3po.fdn.fr: Can't find device <DRBD8(hosts=r2d2.fdn.fr/0-c3po.fdn.fr/0, port=11009, configured as 80.67.169.48:11009 80.67.169.49:11009, backend=<LogicalVolume(/dev/vg1/d868ee5b-0887-4d4e-9289-f209f9243d45.disk0_data, not visible, size=2048m)>, metadev=<LogicalVolume(/dev/vg1/d868ee5b-0887-4d4e-9289-f209f9243d45.disk0_meta, not visible, size=128m)>, visible as /dev/disk/0, size=2048m)>
    Fri May 24 23:54:29 2013 * Verifying orphan volumes
    Fri May 24 23:54:29 2013 * Verifying N+1 Memory redundancy
    Fri May 24 23:54:29 2013 * Other Notes
    Fri May 24 23:54:29 2013 * Hooks Results

(Les erreurs concernant *paploo* ne sont pas très graves, ça veut juste dire «j'ai une VM qui n'est plus là» -- VM qui était sur la machine arrêtée.)

Une fois qu'on en est là, la VIP d'admin doit être présente sur un seul noeud ; dans mon exemple, c'est *r2d2*. Je synchronise donc l'état de *c3po* sur celui de *r2d2* (depuis la machine qui a raison vers le reste du cluster, donc celle qui a tort) :

    root@r2d2:~# gnt-cluster redist-conf
    root@r2d2:~# gnt-cluster verify
    Submitted jobs 83514, 83515
    Waiting for job 83514 ...
    Fri May 24 23:58:16 2013 * Verifying cluster config
    Fri May 24 23:58:16 2013 * Verifying cluster certificate files
    Fri May 24 23:58:16 2013 * Verifying hypervisor parameters
    Fri May 24 23:58:16 2013 * Verifying all nodes belong to an existing group
    Waiting for job 83515 ...
    Fri May 24 23:58:17 2013 * Verifying group 'default'
    Fri May 24 23:58:17 2013 * Gathering data (2 nodes)
    Fri May 24 23:58:17 2013 * Gathering disk information (2 nodes)
    Fri May 24 23:58:17 2013 * Verifying configuration file consistency
    Fri May 24 23:58:17 2013 * Verifying node status
    Fri May 24 23:58:17 2013 * Verifying instance status
    Fri May 24 23:58:18 2013 * Verifying orphan volumes
    Fri May 24 23:58:18 2013 * Verifying N+1 Memory redundancy
    Fri May 24 23:58:18 2013 * Other Notes
    Fri May 24 23:58:18 2013 * Hooks Results

Ça marche :

    root@c3po:~# gnt-cluster getmaster
    r2d2.fdn.fr

On a même récupéré notre VM dans la bagarre :

    root@r2d2:~# gnt-instance list
    Instance      Hypervisor OS                  Primary_node Status  Memory
    paploo.fdn.fr kvm        debootstrap+default c3po.fdn.fr  running   512M

(Ça n'a pas grand chose à voir avec le *redist-conf* de quelques instants avant, c'est juste *ganeti-watcher* qui est passé.)

## *ganeti-watcher* : redémarrage automatique des VM

### Sur le maître

Situation de départ : une VM sur l'esclave. Arrêter l'esclave, voir si la VM monte automatiquement sur le maître. Que se passe-t-il quand l'esclave redémarre ?

#### Arrêt propre

*ganeti-watcher* ne redémarre pas les VM.

    root@r2d2:~# gnt-cluster getmaster
    r2d2.fdn.fr
    root@r2d2:~# gnt-instance list
    Instance      Hypervisor OS                  Primary_node Status  Memory
    paploo.fdn.fr kvm        debootstrap+default c3po.fdn.fr  running   512M
    root@r2d2:~# ssh c3po poweroff
    root@r2d2:~# gnt-instance list
    Instance      Hypervisor OS                  Primary_node Status         Memory
    paploo.fdn.fr kvm        debootstrap+default c3po.fdn.fr  ERROR_nodedown      ?
    root@r2d2:~# ganeti-watcher 
    root@r2d2:~# gnt-instance list
    Instance      Hypervisor OS                  Primary_node Status         Memory
    paploo.fdn.fr kvm        debootstrap+default c3po.fdn.fr  ERROR_nodedown      ?

Les VM ne redémarrent pas au reboot de l'esclave, mais uniquement au lancement de *ganeti-watcher* par le maître (à la main, ou lancé par *cron* toutes les 5 minutes)  :

    root@r2d2:~# gnt-instance list
    Instance      Hypervisor OS                  Primary_node Status     Memory
    paploo.fdn.fr kvm        debootstrap+default c3po.fdn.fr  ERROR_down      -
    root@r2d2:~# ganeti-watcher -d
    2013-06-08 11:13:52,572: ganeti-watcher pid=13966 process:197 DEBUG RunCmd /usr/lib/ganeti/daemon-util check-and-start ganeti-noded
    2013-06-08 11:13:52,577: ganeti-watcher pid=13966 process:197 DEBUG RunCmd /usr/lib/ganeti/daemon-util check-and-start ganeti-confd
    2013-06-08 11:13:52,582: ganeti-watcher pid=13966 process:197 DEBUG RunCmd /usr/lib/ganeti/daemon-util check-and-start ganeti-rapi
    2013-06-08 11:13:52,588: ganeti-watcher pid=13966 __init__:613 DEBUG Attempting to talk to remote API on 127.0.0.1
    2013-06-08 11:13:52,588: ganeti-watcher pid=13966 client:209 DEBUG Using cURL version libcurl/7.26.0 GnuTLS/2.12.20 zlib/1.2.7 libidn/1.25 libssh2/1.4.2 librtmp/2.3
    2013-06-08 11:13:52,589: ganeti-watcher pid=13966 client:419 DEBUG Sending request GET https://127.0.0.1:5080/version (content='')
    2013-06-08 11:13:52,679: ganeti-watcher pid=13966 __init__:344 DEBUG Reported RAPI version 2
    2013-06-08 11:13:52,679: ganeti-watcher pid=13966 __init__:621 DEBUG Successfully talked to remote API
    2013-06-08 11:13:52,683: ganeti-watcher pid=13966 __init__:575 DEBUG Archived 0 jobs, left 0
    2013-06-08 11:13:52,685: ganeti-watcher pid=13966 __init__:547 DEBUG Spawning child for group 'default' (276f96a7-3244-4b4b-b657-72cd0c0e6d6a), arguments ['/usr/sbin/ganeti-watcher', '-d', '--node-group', '276f96a7-3244-4b4b-b657-72cd0c0e6d6a']
    2013-06-08 11:13:52,686: ganeti-watcher pid=13966 __init__:556 DEBUG Started with PID 13977
    2013-06-08 11:13:52,687: ganeti-watcher pid=13966 __init__:561 DEBUG Waiting for child PID 13977
    2013-06-08 11:13:52,772: ganeti-watcher pid=13977 __init__:716 INFO Watcher for node group '276f96a7-3244-4b4b-b657-72cd0c0e6d6a'
    2013-06-08 11:13:52,773: ganeti-watcher pid=13977 __init__:729 DEBUG Using state file /var/lib/ganeti/watcher.276f96a7-3244-4b4b-b657-72cd0c0e6d6a.data
    2013-06-08 11:13:55,177: ganeti-watcher pid=13977 __init__:393 DEBUG Updating instance status file '/var/lib/ganeti/watcher.276f96a7-3244-4b4b-b657-72cd0c0e6d6a.instance-status' with 1 instances
    2013-06-08 11:13:55,237: ganeti-watcher pid=13977 __init__:480 DEBUG Acquired exclusive lock on '/var/run/ganeti/instance-status'
    2013-06-08 11:13:55,237: ganeti-watcher pid=13977 __init__:440 DEBUG Reading per-group instance status from '/var/lib/ganeti/watcher.276f96a7-3244-4b4b-b657-72cd0c0e6d6a.instance-status'
    2013-06-08 11:13:55,238: ganeti-watcher pid=13977 __init__:393 DEBUG Updating instance status file '/var/run/ganeti/instance-status' with 1 instances
    2013-06-08 11:13:55,238: ganeti-watcher pid=13977 __init__:194 INFO Restarting instance 'paploo.fdn.fr' (attempt #2)
    2013-06-08 11:13:59,493: ganeti-watcher pid=13977 __init__:288 DEBUG Verify-disks reported no offline disks, nothing to do
    2013-06-08 11:13:59,551: ganeti-watcher pid=13966 __init__:567 DEBUG Child PID 13977 exited with status (13977, 0)
    root@r2d2:~# gnt-instance list
    Instance      Hypervisor OS                  Primary_node Status  Memory
    paploo.fdn.fr kvm        debootstrap+default c3po.fdn.fr  running   512M

Il faut que *ganeti-watcher* tourne sur le maître pour avoir ce genre d'effet, sur l'esclave il ne touche pas aux VM, même locales :

    root@c3po:~# ganeti-watcher -d
    2013-06-08 11:12:16,590: ganeti-watcher pid=3593 process:197 DEBUG RunCmd /usr/lib/ganeti/daemon-util check-and-start ganeti-noded
    2013-06-08 11:12:16,609: ganeti-watcher pid=3593 process:197 DEBUG RunCmd /usr/lib/ganeti/daemon-util check-and-start ganeti-confd
    root@c3po:~#


#### Arrêt brutal

Pas de différence avec l'arrêt propre.

### Sur l'esclave

Situation de départ : une VM sur le maître. Arrêter le maître. A priori, la VM ne devrait pas remonter. Elle devrait repartir quand le maître redémarre.

Tant que le maître est arrêté, on peut lancer *ganeti-watcher* sur l'esclave tant qu'on veut sans aucun effet. Quand le maître redémarre, il redémarra la VM au premier lancement de *ganeti-watcher*.

