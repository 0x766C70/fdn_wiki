# Administration du service

## Caractéristiques

* Emplacement: TC14
* vcpu: 4
* RAM: 4GB
* IP: 80.67.169.122 - 2001:910:800::122
* Points de montage:
  * /: 5GB
  * /var/lib/postgresql: 50GB
  * /var/lib/matrix-synapse: 15 GB

## Administration

### Modifier la config du bridge

    vim /etc/matrix-appservice-irc/config.yaml
	node /usr/lib/node_modules/matrix-appservice-irc/app.js -r -f /etc/matrix-appservice-irc/my_registration_file.yaml -u "http://matrix.fdn.fr:9999" -c /etc/matrix-appservice-irc/config.yaml -l neo
	systemctl reload matrix-synapse
	systemctl reload matrix-appservice-irc

### Bridger une nouvelle room

Créer/choisir la room IRC: #fdn-name

	/join -geeknode #fdn-name

Créer/choisir la room matrix (choisir le même nom)

Nommer la room avec le même nom que le nom IRC dans :
	
	Settings>General>Main address : #fdn-name:matrix.fdn.fr

Récupérer 'l'Internal room ID' de la room dans :

	Settings>Advanced: !chaineAlphaNum:matrix.fdn.fr

Changer le paramètre de la room dans Security & Privacy:

	Who can access this room ? anyone who know the room's links inluding guest

Changer le paramètre de la room dans Security & Privacy :

	Who can read history -> Members only (since they joined)

Éditer le fichier: /etc/matrix-appservice-irc/config.yaml y ajouter dans la section "mappings:" du serveur irc voulu:

	"#fdn-name":
	roomIds: ["!chaineAlphaNum:matrix.fdn.fr"]

Reprendre les étapes de la section d'avant "Modifier la config du bridge"

### Config chan IRC privé

#### fdn-adminsys-internal (Register + Invite Only)

creation (irssi)

    /join -geeknode #fdn-adminsys-internal

Register le salon:

    chan REGISTER #fdn-adminsys-internal

Passer au Register & Invite Only en parlant a C (/msg C)

    chan SET #fdn-adminsys-internal MLOCK +Ri

admin only : inviter un pseudo ou pseudo[m]

    /invite pseudo #fdn-adminsys-internal
    /invite pseudo[m] #fdn-adminsys-internal

#### fdn-adminsys (Register Only)

Register le salon

    chan REGISTER #fdn-adminsys

Passer au Register Only en parlant a C (/msg C)

    	chan SET #fdn-adminsys MLOCK +R
	
### Réinitialisation du mot de passe

Pour effectuer un _reset_ de mot de passe d'un utilisateur manuellement :

- se connecter à neo.fdn.fr
- calculer le hash du mot de passe

    bash
    hash_password
    Password:
    Confirm password:
    $2a$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    
- mettre à jour la base de données

    su - postgres
    psql
      \c synapse
      UPDATE users SET password_hash='$2a$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' WHERE name='@nick:matrix.fdn.fr';
      \q

- ou avec une méthode directe de requête sur la table :
 
    su -c "psql -c \"UPDATE users SET password_hash='$2a$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' WHERE name='@nick:matrix.fdn.fr'\" -d synapse" -l postgres

- ou avec une requête API

    export user_admin_url="@admin_user:matrix.fdn.fr"
    export user_url="@user_to_modify:matrix.fdn.fr"
    export token="your_token"    (voir section d'après)
    curl -k -XPOST -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d '{"new_password":"xxxxxxxx"}' "https://localhost:8448/_matrix/client/r0/admin/reset_password/$user_url"
    curl -k -XGET -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d '{}' "https://localhost:8448/_synapse/admin/v2/users/$user_url"

### Nettoyer la VM afin de récupérer de l'espace disk 

#### Générer son Token pour accéder à l'API (depuis un compte admin)

    curl -X POST -d '{"type":"m.login.password", "user":"vlp", "password":"XXXXXXX"}' "http://127.0.0.1:8008/_matrix/client/r0/login"
    export token="your_token"

#### Purge local data:

    curl --header "Authorization: Bearer $token" -X POST -d '{}' "http://127.0.0.1:8008/_synapse/admin/v1/media/matrix.fdn.fr/delete?before_ts=1625097600000"

#### Purge remote data:

    curl --header "Authorization: Bearer $token" -X POST -d '{}' "http://127.0.0.1:8008/_synapse/admin/v1/purge_media_cache?before_ts=1625097600000"

#### Purge event

    curl --header "Authorization: Bearer $token" -X POST -H "Content-Type: application/json" -d '{ "delete_local_events": true, "purge_up_to_ts": 1625097600000 }' 'http://127.0.0.1:8008/_synapse/admin/v1/purge_history/!coderoom:matrix.org/'
    curl --header "Authorization: Bearer $token" -X POST -H "Content-Type: application/json" -d '{}' 'http://127.0.0.1:8008/_synapse/admin/v1/purge_history_status/PURGE_ID_FROM_COMMAND_ABOVE/'

#### Purge room

    curl --header "Authorization: Bearer $token" -X POST -H "Content-Type: application/json" -d "{ \"room_id\": \"!coderoom:matrix.org\" }" 'http://127.0.0.1:8008/_synapse/admin/v1/purge_room/'

#### Delete room

    curl --header "Authorization: Bearer $token" -X DELETE -H "Content-Type: application/json" -d "{ \"purge\": true }" 'http://127.0.0.1:8008/_synapse/admin/v1/rooms/!code_room:matrix.org'

#### Get version

    curl --header "Authorization: Bearer $token" -X GET -H "Content-Type: application/json" -d '{}' 'http://127.0.0.1:8008/_synapse/admin/v1/server_version'

#### Check event number by room

    SELECT room_id, count(*) AS count FROM state_groups_state GROUP BY room_id ORDER BY count DESC;

#### Check DB size in Postgres

    select schemaname as table_schema, relname as table_name, pg_size_pretty(pg_relation_size(relid)) as data_size from pg_catalog.pg_statio_user_tables order by pg_relation_size(relid) desc;

### Logs

#### synapse log

    /var/log/matrix-synapse

#### bridge log

    /var/log/matrix-appservice-irc

### Base de données

Dump hebdo sur jabba

### Sauvegarde

Snapshot/Backup hebdo de la VM

### En cas de pépins

#### Relancer matrix:

	systemctl restart matrix-synapse.service

#### Relancer le bridge

	systemctl restart matrix-appservice-irc

### Question

Contacter l'équipe adminsys en charge de matrix: blt, afriqs, vlp
