# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

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
            {'name': 'Collabora: Web based libre office', 'checked': True},
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
services.insert(0, 'traefik')


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
    return None


map = {
    'syncthing': {
        'ports': ['22000:22000', '21027:21027/udp'],
        'port': 8384,
        'volumes':[
            '${HOME}/.config/syncthing/config:/config',

        ]
    }
}


def make_child(service: str, index: int):
    template = {
        service: {
            'container_name': service,
            'depends_on': ['traefik'],
            'image': f'{service}:latest',
            'restart': 'always',
            'networks': {
                'internal': {'ipv4_address': f'172.20.0.{index+3}'},
                'web': 'null'
            },
            'ports': map[service]['ports'],
            'labels': [
                f"traefik.http.services.{service}.loadbalancer.server.port={map[service]['port']}",
                f'traefik.http.routers.{service}.rule=Host(`{service}.$DOMAIN`)',
                f'traefik.http.routers.{service}.entrypoints=https',
                f'traefik.http.routers.{service}.tls.certresolver=http',
                f'traefik.http.routers.{service}.service={service}',
                f'traefik.http.routers.{service}.tls=true',
                'traefik.docker.network=web',
                'traefik.enable=true',
            ],
            'volumes': map[service]['volumes']


        }
    }
    return template


children = [make_child(service, i) for i, service in enumerate(services)]

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
    'services': children

}


def create_docker_compose() -> None:
    with open(f"{os.environ['HOME']}/docker-compose.yml", 'w') as docker_compose:
        yaml.dump(parent, docker_compose, default_flow_style=False)
    return None


if api_ok['status']:
    ip_ok = prompt(ip_confirm, style=custom_style)
    if ip_ok['status']:
        namecheap_as = prompt(namecheap_qs)
        create_a_records(namecheap_as['user'], namecheap_as['key'])
        print('✅  A Records successfully  created!')
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
