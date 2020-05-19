# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import os
import string
from random import sample

from PyInquirer import prompt, Separator

initial_question = [
    {
        'type': 'confirm',
        'name': 'is_ok',
        'message': 'You are going to to go through 5 prompts to select services in 5 categories: Utilities, Media, '
                   'Groupware, Social, and Miscellaneous. They are all selected by default. This creates a list of '
                   'services to install. Feel free to cancel and research the service before installation. Do you '
                   'understand? '
    },
]

services_questions = [
    {
        'type': 'checkbox',
        'qmark': '🛠',
        'message': 'Utilities (all strongly recommended)',
        'name': 'utilities',
        'choices': [
            {'name': 'Syncthing (31k⭐️: Dropbox but better', 'checked': True},
            Separator('  Several services rely on syncthing. Uncheck only if you know what you are doing.'),
            {'name': 'Bitwarden (3.7k⭐️): Manage passwords, secrets and tokens', 'checked': True},
            {
                'name': 'Traefik (29k⭐️: Access services outside of local network.',
                'disabled': 'Required',
                'checked': True,
            },

        ]
    },
    {
        'type': 'checkbox',
        'qmark': '📺',
        'message': 'Media',
        'name': 'media',
        'choices': [
            {'name': 'Jellyfin (6.5k⭐️): Media Server', 'checked': True},
            Separator('  Sabnzbd, Transmission, Jackett, Radarr, Sonarr recommended. See below.'),
            {'name': 'Funkwhale (78⭐️): Federated Grooveshark inspired music server', 'checked': True},
            Separator('  Sabnzbd, Transmission, Jackett, Lidarr recommended. See below.'),
            {'name': 'Booksonic: A subsonic server aimed at audiobooks', 'checked': True},
            Separator('  Sabnzbd, Transmission, Jackett recommended. See below.'),
            {'name': 'Calibre Web (3.2k⭐️): Read, download and upload books in calibre db', 'checked': True},
            Separator('  Syncthing required, LazyLibrarian recommended. See below.'),
            Separator(),
            {'name': 'Sabnzbd', 'checked': True},
            {'name': 'Transmission', 'checked': True},
            {'name': 'Jackett', 'checked': True},
            {'name': 'Radarr ', 'checked': True},
            {'name': 'Sonarr', 'checked': True},
            {'name': 'Bazarr: Subtitle management', 'checked': True},
            {'name': 'Lidarr', 'checked': True},
            {'name': 'LazyLibrarian', 'checked': True},
        ]
    },
    {
        'type': 'checkbox',
        'qmark': '👪',
        'message': 'Groupware',
        'name': 'groupware',
        'choices': [
            {'name': 'Matrix Synapse (6k⭐️): Federated Messaging and Voip', 'checked': True},
            {'name': 'Collabora: Web based LibreOffice', 'checked': True},
            Separator('  Syncthing required.'),
            {'name': 'Radicale (1.8k ⭐️): CalDAV (calendar) and CardDAV (contact) server', 'checked': True},
        ]
    },
    {
        'type': 'checkbox',
        'qmark': '💬',
        'message': 'Social',
        'name': 'social',
        'choices': [
            {'name': 'Weechat (1.9k  ⭐️): Manage slack, gitter, discord, irc, matrix chats', 'checked': True},
            {'name': 'Mastodon: Federated Twitter', 'checked': True},
            {'name': 'Selfoss: Manage Reddit, hackernews, blogs and anything rss-able', 'checked': True},
            {'name': 'Ghost: Manage your own blog', 'checked': True},
        ]
    },
    {
        'type': 'checkbox',
        'qmark': '🥗',
        'message': 'Miscellaneous',
        'name': 'miscellaneous',
        'choices': [
            {'name': 'Lychee (5.6k⭐️): Photo management', 'checked': True},
            Separator('  Syncthing required.'),
            {'name': 'Hydroxide (360⭐️):  3rd party ProtonMail CardDAV, IMAP SMTP bridge', 'checked': True},
            {'name': 'Bitcore (3.6k⭐️): Manage crypto. Compatible with bitpay debit card.', 'checked': True},
            {'name': 'Leon (6.8k⭐️): Personal assistant. Easily add your own module.', 'checked': True},
            {'name': 'Webdav: Generic webDAV server', 'checked': True},
            {'name': 'Home-Assistant (33k⭐️): Manage smart home devices', 'checked': True},
        ],
        'validate': lambda answer: 'You must choose at least one service.'
        if len(answer) == 0 else True
    },
]

initial_answer = prompt(initial_question)
if initial_answer['is_ok']:
    services_answers = prompt(services_questions)
    services = [service.split()[0].lower().rstrip(':')
                for _, category in services_answers.items()
                for service in category]
    with open('.services.json', 'w') as out:
        out.write(json.dumps(services))
