#!/usr/bin/python3

import json
import requests
from requests.auth import HTTPBasicAuth

### https://github.com/paymoapp/api/blob/master/sections/includes.md

def sort_entry_key(elem):
    return elem['start_time']

class Paymo(object):
    """A helper class to interact with the paymoapp.com API"""

    paymo_api = 'https://app.paymoapp.com/api/'
    auth_key=''

    def __init__(self, api_key):
        self.apikey = api_key
        self.paymo_auth = HTTPBasicAuth(api_key, 'pass')

    def __repr__(self):
        return 'Paymo: API'

    def api_call(self, l):
        url = self.paymo_api + l
        r = requests.get(url, auth=self.paymo_auth)
        j = json.loads(r.text)
        return j

    def me(self):
        return self.api_call('me')

    def tasks(self, project):
        r = self.api_call('tasks?where=project_id=' + str(project))
        return r['tasks']

    def task(self, project, id):
        return [t for t in self.tasks(project) if t['id'] == id][0]

    def entries(self, project):
        r = self.api_call('entries?where=project_id=' + str(project))
        e = r['entries']
        e.sort(key=sort_entry_key)
        return e

    def print_tasks(self, project):
        for t in self.tasks(project):
            print(t['id'], ":", t['name'])
