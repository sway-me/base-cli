#!/bin/bash
set -e

sh -c "$(https://sway-me.xyz/base.sh)"
sh -c "$(https://sway-me.xyz/server.sh)"

sudo apt install python3-pip
sudo -H pip3 install PyInquirer PyNamecheap ruamel.yaml requests tqdm

python3 .scripts/get_envars.py
source $HOME/.config/.env
python3 .scripts/get_services.py
python3 .scripts/create_a_records.py
python3 .scripts/create_docker_compose.py

mkdir -p Backups Books Code Docs Downloads/books Feeds Film Music Office Public Series
docker-compose up -d

stow --target=$HOME traefik
echo -e "\nLinked traefik config files.\n"

# commands when services first starting
check(){
  cat .services.json | jq 'contains(["'$1'"])'
}

## radicale
if [[  $(check 'radicale') = true ]]; then
  stow --target=$HOME radicale
  sudo htpasswd -db -c -B .config/radicale/users $USER $RADICALE_PW
  # the calendar name matches the calendar name created by hydroxide
  curl -u $USER:RADICALE_PW -X MKCOL 'https://radicale.$DOMAIN/user/radicale.$DOMAIN' --data \
'<?xml version="1.0" encoding="UTF-8" ?>
<create xmlns="DAV:" xmlns:C="urn:ietf:params:xml:ns:caldav" xmlns:I="http://apple.com/ns/ical/">
  <set>
    <prop>
      <resourcetype>
        <collection />
        <C:calendar />
      </resourcetype>
      <C:supported-calendar-component-set>
        <C:comp name="VEVENT" />
      </C:supported-calendar-component-set>
      <displayname>Calendar</displayname>
    </prop>
  </set>'

  curl -u  $USER:RADICALE_PW -X MKCOL 'http://localhost:5232/user/contacts' --data \
'<?xml version="1.0" encoding="UTF-8" ?>
<create xmlns="DAV:" xmlns:CR="urn:ietf:params:xml:ns:carddav">
  <set>
    <prop>
      <resourcetype>
        <collection />
        <CR:addressbook />
      </resourcetype>
      <displayname>Contacts</displayname>
    </prop>
  </set>
</create>'
echo -e "\nLinked radicale config files.\n"
fi





