# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from pprint import pprint
import regex
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError




class SwayValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid domain',
                cursor_position=len(document.text))  
      


print('\n 🆂  Sway: A curated selfhosted ecosystem\n\n')

envar_qs = [

  {
    'type': 'input',
    'qmark': ' 🌎 ',
    'name': 'domain',
    'message': 'What\'s the name of the domain purchased at namecheap?:',
    'validate': SwayValidator 
  },
  {
    'type': 'input',
    'qmark': ' 🔐 ',
    'name': 'domain',
    'message': 'What\'s the name of the domain purchased at namecheap?:',
    'validate': SwayValidator, 
  },

]

service_qs = [
  {
    'type': 'checkbox',
    'message': 'Choose Services:',
    'qmark': ' ⚙️  ',
    'name': 'services',
    'choices': [
      Separator('\n= Utilities 🛠'),
      { 'name': 'Bitwarden (3.7k⭐️): Manage passwords, secrets and tokens' },
      { 'name': 'Syncthing (31k⭐️: Dropbox but better' },
      { 
        'name': 'Traefik (29k⭐️: Access services outside of local network.',
        'disabled': 'Required',
      },
      Separator('\n= Media 📺'),
      { 'name': 'Jellyfin (6.5k⭐️): Media Server', 'checked': True },
      Separator('  Sabnzbd, Transmission, Jackett, Radarr, Sonarr recommended. See below.'),
      { 'name': 'Funkwhale (78⭐️): Federated Grooveshark inspired music server' },
      Separator('  Sabnzbd, Transmission, Jackett, Lidarr recommended. See below.'),
      { 'name': 'Booksonic: A subsonic server aimed at audiobooks'  },
      Separator('  Sabnzbd, Transmission, Jackett recommended. See below.'),
      { 'name': 'Calibre Web (3.2k⭐️): Read, download and upload books in calibre db' },
      Separator('  Syncthing required, LazyLibrarian recommended. See below.'),
      Separator('\n= Media Services ☠️ '),
      { 'name': 'Sabnzbd', 'checked': True },
      { 'name': 'Transmission', 'checked': True },
      { 'name': 'Jackett', 'checked': True },
      { 'name': 'Radarr ', 'checked': True },
      { 'name': 'Sonarr', 'checked': True },
      { 'name': 'Bazarr: Subtitle management', 'checked': True },
      { 'name': 'Lidarr', 'checked': True },
      { 'name': 'LazyLibrarian', 'checked': True },
      Separator('\n= Groupware 👪'),
      { 'name': 'Matrix-Synapse (6k⭐️): Federated Messaging and Voip', 'checked': True },
      { 'name': 'Collabora: Web based libre office'},
      Separator('  Syncthing required.'),
      { 'name': 'Radicale (1.8k ⭐️): CalDAV (calendar) and CardDAV (contact) server'},
      Separator('\n= Social Media 💬'),
      { 'name': 'Weechat (1.9k  ⭐️): Manage slack, gitter, discord, irc, matrix chats' },
      { 'name': 'Mastodon: Federated Twitter' },
      { 'name': 'Selfoss: Manage Reddit, hackernews, blogsand anything rss-able' },
      { 'name': 'Ghost: Manage your own blog' },
      Separator('\n= Miscellaneous 🥗'),
      { 'name': 'Lychee (5.6k⭐️): Photo management' },
      Separator('  Syncthing required.'),
      { 'name': 'Hydroxide (360⭐️):  3rd party ProtonMail CardDAV, IMAP SMTP bridge' },
      { 'name': 'Bitcore (3.6k⭐️): Manage crypto. Compatible with bitpay debit card.' },
      { 'name': 'Leon (6.8k⭐️): Personal assistant. Easily add your own module.' },
      { 'name': 'Webdav: Generic webDAV server' },
      { 'name': 'Home Assistant (33k⭐️): Manage smart home devices' },
    ],
    'validate': lambda answer: 'You must choose at least one topping.' \
      if len(answer) == 0 else True
  }

]

custom_style = style_from_dict({
    Token.Separator: '#6C6C6C',
    Token.QuestionMark: '#00E1FD bold',
    #Token.Selected: '',  # default
    Token.Selected: '#5F819D',
    Token.Pointer: '#D65FF2  bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F819D bold',
    Token.Question: '',
})

envars = prompt(envar_qs, style=custom_style)
print('')
services = prompt(service_qs, style=custom_style)

def create_A_records(answers):
  pass

def generate_docker_compose(answers):
  pass  

def link_config_files():
  pass

def get_wallpapers():
  pass


def run_docker_compose():
  pass






