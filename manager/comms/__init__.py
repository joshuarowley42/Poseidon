__author__ = 'rowley'

import requests
import json


class Printer:
    def __init__(self, name, host, api_key, debug=False):
        self.name = name
        self.host = host
        self.online = True
        self.api_key = api_key
        self.debug = debug
        self.status = None
        self.files = None
    
    def get_status(self):
        headers = {"X-Api-Key": self.api_key}
        try:
            r = requests.get("http://{host}/api/printer".format(host=self.host), headers=headers, timeout=0.5)
        except requests.exceptions.ConnectTimeout:
            self.online = False
            return
        if r.status_code != 200:
            self.online = False
            return
        else:
            self.status = json.loads(r.content)

    def get_files(self):
        if not self.online:
            return
        headers = {"X-Api-Key": self.api_key}
        r = requests.get("http://{host}/api/files".format(host=self.host), headers=headers, timeout=0.5)
        if r.status_code != 200:
            return None
        else:
            self.files = json.loads(r.content)['files']
            for file in self.files:
                print "{0} - {1}".format(self.name,
                                         file['name'])

    def set_tool_temp(self, target):
        if not self.online:
            return
        headers = {"X-Api-Key": self.api_key,
                   "Content-Type": "application/json"}
        command = {"command": "target",
                   "targets":{
                       "tool0": target
                   }}
        command_json = json.dumps(command)
        r = requests.post("http://{host}/api/printer/tool".format(host=self.host),
                          headers=headers,
                          data=command_json)

    def set_bed_temp(self, target):
        if not self.online:
            return
        headers = {"X-Api-Key": self.api_key,
                   "Content-Type": "application/json"}
        command = {"command": "target",
                   "target": target
                   }
        command_json = json.dumps(command)
        r = requests.post("http://{host}/api/printer/bed".format(host=self.host),
                          headers=headers,
                          data=command_json)
