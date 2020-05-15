from __future__ import print_function, unicode_literals

import os
import regex
import string
from random import sample

from PyInquirer import style_from_dict, Token, prompt, Validator, ValidationError

regex_map = {
    'domain': '^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$',
    'email': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
}


class DomainValidator(Validator):
    def validate(self, document):
        ok = regex.match(regex_map['domain'], document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid domain',
                cursor_position=len(document.text))


class EmailValidator(Validator):
    def validate(self, document):
        ok = regex.match(regex_map['email'], document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid email',
                cursor_position=len(document.text))


envar_qs = [
    {
        'type': 'input',
        'qmark': ' 🌎 ',
        'name': 'domain',
        'message': 'What\'s the name of the domain purchased at namecheap?',
        'validate': DomainValidator
    },
    {
        'type': 'input',
        'qmark': ' ✉️ ',
        'name': 'email',
        'message': 'What\'s the root recovery email for all your data (protonmail recommended)?',
        'validate': EmailValidator,
    },
]

custom_style = style_from_dict({
    Token.Answer: '#00E1FD bold',
})

envars = prompt(envar_qs, style=custom_style)

traefik_pw = ''.join(sample(string.ascii_uppercase + string.ascii_lowercase + string.digits, 10))

with open(f"{os.environ['HOME']}/.config/.env", 'w') as out:
    out.write(f'''
export DOMAIN={envars['domain']}
export EMAIL={envars['email']}
export TRAEFIK_PW={traefik_pw}
export TRAEFIK_BASIC_AUTH=$(htpasswd -nb $USER $TRAEFIK_PW)
export TZ=$(cat /etc/timezone)
''')

print('\n✅ SUCCESS: Your .env file is at "~/.config/.env". Don\'t expose (push) this file.\n')

print(
    f"\n✅ NOTE: Your *traefik* password is {traefik_pw}.\n\nUse this to log  into traefik.{envars['domain']} once its up. Its recommended you keep this and add it as a login item to the bitwarden service once its up.\n")
