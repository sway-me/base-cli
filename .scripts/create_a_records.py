# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import regex, requests, os
from PyInquirer import prompt, Validator, ValidationError
from namecheap import Api
from tqdm import tqdm
import json

with open('.services.json', 'r') as f:
    services = json.load(f)


def create_a_records(user, key) -> None:
    ip = requests.get('http://ifconfig.me')
    for i in tqdm(range(len(services))):
        record = {
            "Type": "A",
            "Name": services[i],
            "Address": ip,
            "TTL": "1799",
        }
        api = Api(user, key, user, ip.text, sandbox=False, attempts_count=3, attempts_delay=0.1)
        import sys
        sys.stdout = None
        api.domains_dns_addHost(os.environ['DOMAIN'], record)
        sys.stdout = sys.__stdout__

    print(f'✅ SUCCESS: {len(services)} A Record(s) successfully created!')


api_question = [
    {
        'type': 'confirm',
        'message': 'Do you have a Namecheap API key?',
        'name': 'is_ok',
        'default': True,
    },
]

ip_question = [
    {
        'type': 'confirm',
        'message': 'Did you whitelist your IP to your Namecheap account settings?',
        'name': 'is_ok',
        'default': True,
    },
]


class KeyValidator(Validator):
    def validate(self, document) -> None:
        ok = regex.match('[0-9a-z]{32}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid API key',
                cursor_position=len(document.text))


namecheap_questions = [
    {
        'type': 'input',
        'name': 'user',
        'qmark': ' 👤',
        'message': 'What\'s your Namecheap username?',
    },
    {
        'type': 'input',
        'name': 'key',
        'qmark': ' 🔑',
        'message': 'What\'s your Namecheap API key?',
        'validate': KeyValidator
    }
]

api_answer = prompt(api_question)
if api_answer['is_ok']:
    ip_answer = prompt(ip_question)
    if ip_answer['is_ok']:
        namecheap_answers = prompt(namecheap_questions)
        create_a_records(namecheap_answers['user'], namecheap_answers['key'])
    else:
        print('To whitelist an IP, visit https://sway-me.xyz/wiki#namecheap#whitelist_ip')
else:
    nlh = "\n - "
    nl = "\n"
    print(f'''You have selected the following services:
    {nl} - traefik{nlh}{nlh.join(services)}{nl}{nl}Please create an "A" Record for each service. You can do this later, 
but it is required.  Otherwise your services will be unreachable. If you are using namecheap, 
visit https://sway-me.xyz/wiki/namecheap#add_a_record.''')

