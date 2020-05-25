# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

from typing import Dict

import requests
import yaml
import json
import os
from random import sample
import string

with open('.services.json', 'r') as f:
    services = json.load(f)

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
    'bitwarden': {
        'port': 80,
        'image': 'bitwardenrs/server',
        'environment': {
            'WEBSOCKET_ENABLED': 'false',
            'SIGNUPS_ALLOWED': 'true',
        },
        'volumes': ['$HOME/.config/bitwarden:/data']
    },
    'sabnzbd': {
        'port': 8080,
        'volumes': [
            '$HOME/.config/sabnzbd:/config',
            '$HOME/Downloads:/downloads',
        ]
    },
    'transmission': {
        'port': 9091,
        'environment': {
            'TRANSMISSION_WEB_HOME': '/combustion-release/',
            'USER': '$USER',
            'PASS': '$TRANSMISSION_PW',
        },
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
        'environment': {
            'FUNKWHALE_PROTOCOL': 'https',
            'FUNKWHALE_HOSTNAME': 'funkwhale.$DOMAIN',
            'NESTED_PROXY': '1',
        },
        'volumes': [
            '$HOME/.config/funkwhale:/data',
            '$HOME/Music:/music',
        ],
    },
    'lazylibrarian': {
        'port': 5299,
        'environment': {'DOCKER_MODS': 'linuxserver/calibre-web:calibre'},
        'volumes': [
            '$HOME/.config/lazylibrarian:/config',
            '$HOME/Downloads:/downloads',
            '$HOME/Downloads/books:/to-process',
            '$HOME/Books:/books',
        ]
    },
    'calibre-web': {
        'port': 8083,
        'environment': {'DOCKER_MODS': 'linuxserver/calibre-web:calibre'},
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
    'matrix': {
        'port': 8008,
        'image': 'matrixdotorg/synapse',
        # TODO: get proper homeserver
        'environment': {'SYNAPSE_CONFIG_PATH': '/data/homeserver.yaml'},
        'volumes': ['$HOME/.config/matrix:/data']
    },
    # TODO: Combine collabora and  wopiserver into a multi-stage container
    'collabora': {
        'port': 9980,
        'image': 'sway-me/collabora',
        'environment': {
            'username': '$USER',
            'password': '$COLLABORA_PW',
            'domain': 'localhost:8080',
        },
        'volumes': ['$HOME/Office:/var/wopi_local_storage'],
    },
    'radicale': {
        'port': 5232,
        'image': 'tomsquest/docker-radicale',
        'volumes': [
            '$HOME/.config/radicale/data:/data',
            '$HOME/.config/radicale/config:/config',
        ]
    },

}

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


def make_child(service: str, index: int) -> Dict:
    # concat if env vars exist for service. see below
    environment = ['PUID=1000', 'PGID=1000', 'TZ=${TZ}']
    if 'environment' in options[service]:
        environment = environment + options[service]['environment']
    return {
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


for i, service in enumerate(services):
    parent['services'][service] = make_child(service, i)

with open(f"{os.environ['HOME']}/docker-compose.yml", 'w') as docker_compose:
    yaml.dump(parent, docker_compose, default_flow_style=False)


def handle_password(service: str) -> str:
    nl = '\n'
    pw = ''.join(sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 10))
    with open(f"{os.environ['HOME']}/.config/.env", 'a') as env:
        env.write(f'{nl}export {service.upper()}_PW={pw}{nl}')

    print(f'''✅ NOTE: Your *{service}* login credentials are u:{os.environ['USER']} p:{pw}.
Use these to log into {service}.{os.environ['DOMAIN']} once its up. Its recommended you note this 
and add it as a login item to the bitwarden service.''')
    return pw

# TODO create subset list of services that require password and envar and just itrate through that list
handle_password('traefik')
with open(f"{os.environ['HOME']}/.config/.env", 'a') as out:
    out.write('export TRAEFIK_BASIC_AUTH=$(htpasswd -nb $USER $TRAEFIK_PW)\n')
if 'transmission' in services:
    handle_password('transmission')
if 'collabora' in services:
    handle_password('collabora')
if 'radicale' in services:
    password = handle_password('radicale')
