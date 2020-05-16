# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import string
from random import sample
from typing import List, Dict, Any, Union

import regex, requests, os
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
import yaml
# from namecheap import Api
from tqdm import tqdm

service_qs = [
    {
        'type': 'checkbox',
        'message': 'Choose Services:',
        'qmark': ' ⚙️  ',
        'name': 'services',
        'choices': [
            Separator('\n= Utilities 🛠'),
            {'name': 'Bitwarden (3.7k⭐️): Manage passwords, secrets and tokens', 'checked': True},
            {'name': 'Syncthing (31k⭐️: Dropbox but better', 'checked': True},
            {
                'name': 'Traefik (29k⭐️: Access services outside of local network.',
                'disabled': 'Required',
                'checked': True,
            },
            Separator('\n= Media 📺'),
            {'name': 'Jellyfin (6.5k⭐️): Media Server', 'checked': True},
            Separator('  Sabnzbd, Transmission, Jackett, Radarr, Sonarr recommended. See below.'),
            {'name': 'Funkwhale (78⭐️): Federated Grooveshark inspired music server', 'checked': True},
            Separator('  Sabnzbd, Transmission, Jackett, Lidarr recommended. See below.'),
            {'name': 'Booksonic: A subsonic server aimed at audiobooks', 'checked': True},
            Separator('  Sabnzbd, Transmission, Jackett recommended. See below.'),
            {'name': 'Calibre Web (3.2k⭐️): Read, download and upload books in calibre db', 'checked': True},
            Separator('  Syncthing required, LazyLibrarian recommended. See below.'),
            Separator('\n= Media Services ☠️ '),
            {'name': 'Sabnzbd', 'checked': True},
            {'name': 'Transmission', 'checked': True},
            {'name': 'Jackett', 'checked': True},
            {'name': 'Radarr ', 'checked': True},
            {'name': 'Sonarr', 'checked': True},
            {'name': 'Bazarr: Subtitle management', 'checked': True},
            {'name': 'Lidarr', 'checked': True},
            {'name': 'LazyLibrarian', 'checked': True},
            Separator('\n= Groupware 👪'),
            {'name': 'Matrix Synapse (6k⭐️): Federated Messaging and Voip', 'checked': True},
            {'name': 'Collabora: Web based LibreOffice', 'checked': True},
            Separator('  Syncthing required.'),
            {'name': 'Radicale (1.8k ⭐️): CalDAV (calendar) and CardDAV (contact) server', 'checked': True},
            Separator('\n= Social Media 💬'),
            {'name': 'Weechat (1.9k  ⭐️): Manage slack, gitter, discord, irc, matrix chats', 'checked': True},
            {'name': 'Mastodon: Federated Twitter', 'checked': True},
            {'name': 'Selfoss: Manage Reddit, hackernews, blogs and anything rss-able', 'checked': True},
            {'name': 'Ghost: Manage your own blog', 'checked': True},
            Separator('\n= Miscellaneous 🥗'),
            {'name': 'Lychee (5.6k⭐️): Photo management', 'checked': True},
            Separator('  Syncthing required.'),
            {'name': 'Hydroxide (360⭐️):  3rd party ProtonMail CardDAV, IMAP SMTP bridge', 'checked': True},
            {'name': 'Bitcore (3.6k⭐️): Manage crypto. Compatible with bitpay debit card.', 'checked': True},
            {'name': 'Leon (6.8k⭐️): Personal assistant. Easily add your own module.', 'checked': True},
            {'name': 'Webdav: Generic webDAV server', 'checked': True},
            {'name': 'Home-Assistant (33k⭐️): Manage smart home devices', 'checked': True},
        ],
    }

]

api_confirm = [
    {
        'type': 'confirm',
        'message': 'Do you have a Namecheap API key?',
        'name': 'status',
        'default': True,
    },
]

ip_confirm = [
    {
        'type': 'confirm',
        'message': 'Did you whitelist your IP to your Namecheap account settings?',
        'name': 'status',
        'default': True,
    },
]


class KeyValidator(Validator):
    def validate(self, document):
        ok = regex.match('[0-9a-z]{32}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid API key',
                cursor_position=len(document.text))


namecheap_qs = [
    {
        'type': 'input',
        'name': 'user',
        'qmark': ' 👤',
        'message': 'What\'s your Namecheap user name?',
    },
    {
        'type': 'input',
        'name': 'key',
        'qmark': ' 🔑',
        'message': 'What\'s your Namecheap API key?',
        'validate': KeyValidator
    }
]

custom_style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#00E1FD bold',
    # Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#D65FF2  bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

service_r = prompt(service_qs, style=custom_style)
api_ok = prompt(api_confirm, style=custom_style)

services = [service.split()[0].lower().rstrip(':') for service in service_r['services']]


def create_a_records(user, key) -> None:
    ip = requests.get('http://ifconfig.me')
    for i in tqdm(range(len(services))):
        record = {
            "Type": "A",
            "Name": services[i],
            "Address": ip,
            "TTL": "1799",
        }
    # import sys as sys1
    # sys1.stdout = None
    # api = Api(user, key, user, ip.text, sandbox=False, attempts_count=3, attempts_delay=0.1)
    # api.domains_dns_addHost(os.environ['DOMAIN'], record)
    print(f'✅ SUCCESS! {len(services)} A Records successfully created!')
    return None


options = {
    'syncthing': {
        'ports': ['22000:22000', '21027:21027/udp'],
        'port': 8384,
        'volumes': [
            '$HOME/.config/syncthing:/config',
            '$HOME/Books:/Books',
            '$HOME/Documents:/Documents/',
            '$HOME/Downloads:/Downloads',
            '$HOME/Feeds:/Feeds',
            '$HOME/Images:/Images',
            '$HOME/Office:/Office',
            '$HOME/Public:/Public',
        ]
    },
    'sabnzbd': {
        'port': 8080,
        'volumes': [
            '$HOME/.config/sabnzbd:/config',
            '$HOME/Downloads:/downloads'
        ]
    },
    'transmission': {
        'port': 9091,
        'environment': [
            'TRANSMISSION_WEB_HOME=/combustion-release/',
            'USER=$USER',
            'PASS=$TRANSMISSION_PW',
        ],
        'volumes': [
            '$HOME/.config/transmission:/config'
            '$HOME/Downloads:/downloads'
        ]
    },
    'jackett': {
        'port': 9117,
        'volumes': ['$HOME/.config/jackett:/config'],
    },
    'radarr': {
        'port': 7878,
        'volumes': [
            '$HOME/.config/radarr:/config'
            '$HOME/Downloads:/downloads',
            '$HOME/Film:/movies'
        ]
    },
    'sonarr': {
        'port': 8989,
        'volumes': [
            '$HOME/.config/sonarr:/config'
            '$HOME/Downloads:/downloads',
            '$HOME/Series:/tv',
        ]
    },
    'bazarr': {
        'port': 6767,
        'volumes': [
            '$HOME/.config/bazarr:/config'
            '$HOME/Series:/tv',
            '$HOME/Film:/movies',
        ]
    },
    'lidarr': {
        'port': 8686,
        'volumes': [
            '$HOME/.config/lidarr:/config'
            '$HOME/Downloads:/downloads',
            '$HOME/Music:/music',
        ]
    },
    'jellyfin': {
        'port': 8096,
        'volumes': [
            '$HOME/.config/jellyfin:/config'
            '$HOME/Film:/data/movies',
            '$HOME/Series:/data/tvshows',
            '$HOME/Music:/data/music',
        ]
    },
    'funkwhale': {
        'port': 80,
        'image': 'funkwhale/all-in-one:latest',
        'environment': [
            'FUNKWHALE_PROTOCOL=https',
            'FUNKWHALE_HOSTNAME=funkwhale.$DOMAIN',
            'NESTED_PROXY=1',
        ],
        'volumes': [
            '$HOME/.config/funkwhale:/data',
            '$HOME/Music:/music',
        ],
    },
    'lazylibrarian': {
        'port': 5299,
        'environment': ['DOCKER_MODS=linuxserver/calibre-web:calibre'],
        'volumes': [
            '$HOME/.config/lazylibrarian:/config',
            '$HOME/Downloads:/downloads',
            '$HOME/Downloads/books:/to-process',
            '$HOME/Books:/books',
        ]
    },
    'calibre-web': {
        'port': 8083,
        'environment': ['DOCKER_MODS=linuxserver/calibre-web:calibre'],
        'volumes': [
            '$HOME/.config/calibre-web:/config',
            '$HOME/Books:/books',
        ]
    },
    'booksonic': {
        'port': 4040,
        'volumes': [
            '$HOME/.config/booksonic:/config',
            '$HOME/Books:/audiobooks',
        ]
    },
}


def make_child(service: str, index: int):
    # concat if env vars exist for service. see below
    environment = ['PUID=1000', 'PGID=1000', 'TZ=${TZ}']
    if 'environment' in options[service]:
        environment = environment + options[service]['environment']

    template = {
        'container_name': service,
        'depends_on': ['traefik'],
        'restart': 'unless-stopped',
        'image': options[service]['image'] if 'image' in options[service] else f'linuxserver/{service}:latest',
        'networks': {
            'internal': {'ipv4_address': f'172.20.0.{index + 3}'},
            'web': None
        },
        'ports': options[service]['ports'] if 'ports' in options[service] else None,
        'environment': environment,
        'labels': [
            'traefik.docker.network=web',
            'traefik.enable=true',
            f'traefik.http.routers.{service}.service={service}',
            f"traefik.http.services.{service}.loadbalancer.server.port={options[service]['port']}",
            f'traefik.http.routers.{service}.rule=Host(`{service}.$DOMAIN`)',
            f'traefik.http.routers.{service}.entrypoints=http',
            f'traefik.http.middlewares.{service}-https-redirect.redirectscheme.scheme=https',
            f'traefik.http.routers.{service}.middlewares={service}-https-redirect',
            f'traefik.http.routers.{service}-secure.rule=Host(`{service}.$DOMAIN`)',
            f'traefik.http.routers.{service}-secure.entrypoints=https',
            f'traefik.http.routers.{service}-secure.tls.certresolver=http',
            f'traefik.http.routers.{service}-secure.tls=true',
        ],
        'volumes': options[service]['volumes'],
    }
    return template


parent = {
    'version': '3',
    'networks': {
        'web': {'external': True},
        'internal': {
            'external': False,
            'ipam': {
                'config': [{'subnet': '172.20.0.0/24'}]
            }
        }
    },
    'services': {
        'traefik': {
            'image': 'traefik:latest',
            'container_name': 'traefik',
            'restart': 'unless-stopped',
            'ports': ['80:80', '443:443'],
            'networks': 'web',
            'labels': [
                'traefik.http.middlewares.traefik-auth.basicauth.users=$TRAEFIK_BASIC_AUTH',
                'traefik.http.routers.traefik.middlewares=traefik-auth',
                'traefik.http.routers.traefik.rule=Host(`traefik.$DOMAIN`)',
                'traefik.http.services.traefik.loadbalancer.server.port=8080',
                'traefik.http.routers.traefik.tls.certresolver=http',
                'traefik.http.routers.traefik.entrypoints=https',
                'traefik.http.routers.traefik.service=api@internal',
                'traefik.http.routers.traefik.tls=true',
                'traefik.enable=true',
            ],
            'volumes': [
                '/etc/localtime:/etc/localtime',
                '/var/run/docker.sock:/var/run/docker.sock',
                '$HOME/.config/traefik/traefik.yml:/traefik.yml',
                '$HOME/.config/traefik/acme.json:/acme.json'
            ]
        }
    }
}

for i, service in enumerate(services):
    parent['services'][service] = make_child(service, i)


def create_docker_compose() -> None:
    with open(f"{os.environ['HOME']}/docker-compose.yml", 'w') as docker_compose:
        yaml.dump(parent, docker_compose, default_flow_style=False)


if api_ok['status']:
    ip_ok = prompt(ip_confirm, style=custom_style)
    if ip_ok['status']:
        namecheap_as = prompt(namecheap_qs)
        create_a_records(namecheap_as['user'], namecheap_as['key'])
        create_docker_compose()
    else:
        print('To whitelist an IP, visit https://sway-me.xyz/wiki#namecheap#whitelist_ip')
else:
    nlh = "\n - "
    nl = "\n"
    print(f'''You have selected the following services:
    {nlh}{nlh.join(services)}{nl}  
    Please create an A Record for each service. This is required.
    If you are using namecheap, visit https://sway-me.xyz/wiki/namecheap#add_a_record.''')

if 'transmission' in services:
    transmission_pw = ''.join(sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 10))
    with open(f"{os.environ['HOME']}/.config/.env", 'a') as out:
        out.write(f'{nl}export TRANSMISSION_PW={transmission_pw}{nl}')
    print(f'''✅ NOTE: Your *transmission* password is {transmission_pw}.
            Use this to log into transmission.{os.environ['DOMAIN']} once its up. Its recommended you keep this. 
            Then add it as a login item to the bitwarden service.''')
