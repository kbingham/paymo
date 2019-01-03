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

    def projects(self):
        self._projects = self.api_call('projects')['projects']
        return self._projects

    def project(self, id):
        return [p for p in self.projects() if p['id'] == id][0]

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


import re

class TimeWarriorExporter(object):

    def __init__(self, paymo, project):
        self._paymo = paymo

        self._project = paymo.project(project)

        self._project_name = self._project['code']
        self._tasks = paymo.tasks(project)
        self._entries = paymo.entries(project)

    def print_entries(self):
        def task_name(id):
            return [t for t in self._tasks if t['id'] == id][0]['name']

        def conv_date(d):
            return re.sub("[:-]", "", d)

        def remove_newlines(d):
            return re.sub("\r?\n", " ", d)

        for e in self._entries:
            start = conv_date(e['start_time'])
            end = conv_date(e['end_time'])
            desc = remove_newlines(e['description'])

            print("inc {} - {} # {} {} \" {} \"".format(start, end, self._project_name, task_name(e['task_id']), desc))
