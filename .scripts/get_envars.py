from __future__ import print_function, unicode_literals
import os
import re
from PyInquirer import prompt, Validator, ValidationError

regex_map = {
    'domain': r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$',
    'email': r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
}


class DomainValidator(Validator):
    def validate(self, document):
        ok = re.match(regex_map['domain'], document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid domain',
                cursor_position=len(document.text))


class EmailValidator(Validator):
    def validate(self, document):
        ok = re.match(regex_map['email'], document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid email',
                cursor_position=len(document.text))


envar_questions = [
    {
        'type': 'input',
        'qmark': ' 🌎 ',
        'name': 'domain',
        'message': 'What\'s the name of the domain you purchased?',
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

envar_answers = prompt(envar_questions)
with open(f"{os.environ['HOME']}/.config/.env", 'w') as out:
    out.write(f'''export DOMAIN={envar_answers['domain']}
export EMAIL={envar_answers['email']}
export TZ=$(cat /etc/timezone)
''')

print('\n✅ SUCCESS: Your .env file is at "~/.config/.env". Don\'t expose (push) this file.\n')
