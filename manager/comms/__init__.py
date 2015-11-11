__author__ = 'rowley'

import requests
import json
from manager.config import *


class Printer:
    def __init__(self, name, host, api_key, debug=False):
        self.name = name
        self.host = host
        self.online = True
        self.api_key = api_key
        self.debug = debug
        self.state = None
        self.temperature = {}
        self.files = None
    
    def get_status(self):
        headers = {"X-Api-Key": self.api_key}
        try:
            r = requests.get("http://{host}/api/connection".format(host=self.host), headers=headers, timeout=TIMEOUT)
        except:
            self.online = False
            return
        if r.status_code != 200:
            print r.status_code
            self.online = False
            return
        response = json.loads(r.content)
        if response['current']['state'] == 'Closed':
            self.state = response['current']['state']
            self.online = False
            return


        try:
            r = requests.get("http://{host}/api/printer".format(host=self.host), headers=headers, timeout=TIMEOUT)
        except:
            self.online = False
            return
        if r.status_code != 200:
            print r.status_code
            self.online = False
            return
        else:
            status = json.loads(r.content)
            self.state = status['state']['text']
            self.temperature = status['temperature']

    def send_gcode(self, message):
        if not self.online:
            return
        headers = {"X-Api-Key": self.api_key,
                   "Content-Type": "application/json"}
        command = {"command": message}
        command_json = json.dumps(command)

        r = requests.post("http://{host}/api/printer/command".format(host=self.host),
                          headers=headers,
                          data=command_json,
                          timeout=0.5)
        if r.status_code != 204:
            print 'Error - {0}'.format(r.status_code)

    def get_files(self):
        if not self.online:
            return
        headers = {"X-Api-Key": self.api_key}
        r = requests.get("http://{host}/api/files".format(host=self.host), headers=headers, timeout=TIMEOUT)
        if r.status_code != 200:
            self.files = None
            return None
        else:
            files = json.loads(r.content)['files']
            self.files = []
            for file in files:
                self.files.append(file['name'])
        return self.files

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

    def select_file(self, filename, start_print=False):
        if not self.online:
            return None
        if self.files is None or filename not in self.files:
            print "Can't load file on: {0}".format(self.name)
            return None
        headers = {"X-Api-Key": self.api_key,
                   "Content-Type": "application/json"}
        command = {"command": "select",
                   "print": start_print
                   }
        command_json = json.dumps(command)
        r = requests.post("http://{host}/api/files/local/{filename}".format(host=self.host, filename=filename),
                          headers=headers,
                          data=command_json)
        if r.status_code != 204:
            print "{status_code} http://{host}/api/files/local/{filename}".format(status_code=r.status_code,
                                                                                  host=self.host, filename=filename)
            return None

        return True