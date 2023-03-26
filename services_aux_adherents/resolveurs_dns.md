# Service aux adhérents

FDN fourni des resolveurs dns ouverts dont les adresses sont : 80.67.169.12 et 80.67.169.40.

DoT et DoH sont aussi disponibles:

- DoT: ns0.fdn.fr et ns1.fdn.fr
- DoH: https://ns0.fdn.fr/dns-query et https://ns1.fdn.fr/dns-query

Le domaine 'resolver.fdn.fr' existe aussi est il est prévu d'en faire un round-robin sur les deux serveurs, mais la génération du certificat n'est pas en place donc le domaine ne sert que ns0 actuellement.

# Opérations de maintenance

Les resolvers sont architecturés avec un resolver recursif (unbound) en local sur le port 10053, et dnsdist qui utlise unbound et répond aux requêtes utilisateurs.

## Vider le cache d'un domaine

Il faut vider le cache d'unbound et de dnsdist pour que ce soit utile (dans cet ordre).

Attention, le cache de dnsdist est un cache "de requêtes" : si on intérroge un domaine d'une manière légèrement différente, on risque fort de ne pas tomber dans le cache et de penser (à tord) que le domaine n'est pas caché. Il faut bien vider les deux caches pour que ce soit efficace.

Exemple pour le domaine 'www.fdn.fr' :

```
unbound-control flush www.fdn.fr
dnsdist -C /etc/dnsdist/dnsdist.conf -e 'getPool(""):getCache():expungeByName(newDNSName("www.fdn.fr"))'
```

On peut vérifier en regardant le TTL donné par la commande `dig www.fdn.fr @ns0.fdn.fr` (ou ns1) *avant* et *après* l'opération.

## Stats diverses

dnsdist permet d'obtenir un certain nombres de statistiques, soit dans une interface web, soit en console.

### Interface web

L'interface web écoute sur localhost, il faut monter un tunnel ssh:

```
ssh -L 8082:127.0.0.1:8082 ns0.fdn.fr
```

Puis se connecter à localhost:8082 sur sa machine, avec n'importe quel user et le mot de passe défini dans la commande `webserver()` de /etc/dnsdist/dnsdist.conf

### Interface console

On peut se connecter à la console avec la commande suivante (oui, il faut spécifier le chemin vers la conf...):

```
dnsdist -C /etc/dnsdist/dnsdist.conf -c
```

De là on peut interroger pas mal de choses, on a accès à tout ce qui est visible de l'interpreteur lua de dnsdist. Par exemple:

```
> dumpStats()
acl-drops                                         0    noncompliant-responses                             0
cache-hits                                 77361434    outgoing-doh-query-pipe-full                       0
cache-misses                               40505519    proxy-protocol-invalid                             0
cpu-iowait                                    72640    queries                                    246186067
cpu-steal                                   1975489    rdqueries                                  246118556
cpu-sys-msec                                8153735    real-memory-usage                          910274560
cpu-user-msec                               7678834    responses                                   38104265
doh-query-pipe-full                               0    rule-drop                                     680021
doh-response-pipe-full                            0    rule-nxdomain                                      0
downstream-send-errors                            0    rule-refused                                       0
downstream-timeouts                         2264034    rule-servfail                                      0
dyn-block-nmg-size                                6    rule-truncated                              39801241
dyn-blocked                                87825921    security-status                                    0
empty-queries                                  2495    self-answered                               39801241
fd-usage                                       1444    servfail-responses                           3347584
frontend-noerror                          128682132    special-memory-usage                       900517888
frontend-nxdomain                          21020203    tcp-cross-protocol-query-pipe-full                 0
frontend-servfail                           5473462    tcp-cross-protocol-response-pipe-full              0
latency-avg100                                20127.4  tcp-listen-overflows                          176252
latency-avg1000                               21479.1  tcp-query-pipe-full                                0
latency-avg10000                              20668.2  trunc-failures                                     0
latency-avg1000000                            24056.4  udp-in-csum-errors                            686661
latency-count                             151162037    udp-in-errors                               91446375
latency-slow                                 408365    udp-noport-errors                           31264387
latency-sum                              2600959605    udp-recvbuf-errors                                 0
latency0-1                                127951388    udp-sndbuf-errors                                224
latency1-10                                 4465608    udp6-in-csum-errors                            14386
latency10-50                               10736319    udp6-in-errors                                 19132
latency100-1000                             5379485    udp6-noport-errors                          10388020
latency50-100                               2220872    udp6-recvbuf-errors                             4746
no-policy                                         0    udp6-sndbuf-errors                                71
noncompliant-queries                           6517    uptime                                         28412
> getPool(""):getCache():printStats()
Entries: 1985622/2000000
Hits: 77424498
Misses: 40454235
Deferred inserts: 78046
Deferred lookups: 78484
Lookup Collisions: 31096
Insert Collisions: 24323
TTL Too Shorts: 0
> showServers()
#   Name                 Address                       State     Qps    Qlim Ord Wt    Queries   Drops Drate   Lat Outstanding Pools
0   Local-bind1          [::1]:10053                      up   292.4       0   1  1   10144152  412693   7.9  88.6          71
1   Local-bind2          [::1]:10053                      up   280.5       0   1  1   10141700  401043  10.9 107.2          60
2   Local-bind3          [::1]:10053                      up   308.2       0   1  1   10136345  723757  93.2 110.3         495
3   Local-bind4          [::1]:10053                      up   295.1       0   1  1   10142837  742254 111.3 102.9         518
All                                                           1175.0                  40565034 2279747
> showDynBlocks()
> topSlow()
> topQueries()
> topClients()
> topBandwidth()
```

En cas de doute, la commande 'help' ou bien la doc en ligne https://dnsdist.org/reference/ peuvent toujours servir.
