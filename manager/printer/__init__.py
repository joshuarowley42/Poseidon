__author__ = 'rowley'

import requests
import json
from config import *
import os

class Printer:
    def __init__(self, name, host, api_key, dock, debug=False):
        self.name = name
        self.host = host
        self.dock_location = dock
        self.online = True
        self.selected = False
        self.api_key = api_key
        self.debug = debug
        self.state = None
        self.temperature = {}
        self.files = []
    
    def get_status(self):
        headers = {"X-Api-Key": self.api_key}
        try:
            r = requests.get("http://{host}/api/connection".format(host=self.host), headers=headers, timeout=TIMEOUT)
        except:
            self.state = 'Connection to Pi Failed'
            self.online = False
            return
        if r.status_code != 200:
            print "Connection {0} - {1}".format(self.name, r.status_code)
            self.online = False
            return
        try:
            response = json.loads(r.content)
        except ValueError:
            self.state = 'Invalid Response'
            self.online = False
            return
        if response['current']['state'] not in ['Printing', 'Operational']:
            self.state = response['current']['state'].strip()
            self.online = False
            return

        try:
            r = requests.get("http://{host}/api/printer".format(host=self.host), headers=headers, timeout=TIMEOUT)
        except:
            self.state = 'Connection to Pi Failed'
            self.online = False
            return
        if r.status_code != 200:
            print "Printer {0} - {1}".format(self.name, r.status_code)
            self.online = False
            return
        else:
            try:
                status = json.loads(r.content)
            except ValueError:
                self.state = 'Invalid Response'
                self.online = False
                return
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
        self.files.sort()
        return self.files

    def upload_file(self, filename):
        if not self.online:
            return
        if os.path.split(filename)[1] in self.files:
            print "File already on {0}".format(self.name)
            return
        headers = {"X-Api-Key": self.api_key}
        file = {'file': open(filename, 'rb')}
        r = requests.post('http://{host}/api/files/local'.format(host=self.host, filename=filename), files=file, headers=headers)
        if r.status_code != 201:
            print "Upload Failed on {host} - HTTP Code {0}".format(r.status_code, filename=filename, host=self.name)
        else:
            print "Upload Successful on {0}".format(self.name)
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

    def kill(self):
        if not self.online:
            return None
        headers = {"X-Api-Key": self.api_key,
                   "Content-Type": "application/json"}
        command = {"command": "cancel"
                   }
        command_json = json.dumps(command)
        r = requests.post("http://{host}/api/job".format(host=self.host),
                          headers=headers,
                          data=command_json)
        print r.status_code


    def dock(self):
        self.send_gcode("G28 X0 Y0")
        self.send_gcode("G1 X{0} F3000".format(self.dock_location[0]))
        self.send_gcode("G1 Y{0} F3000".format(self.dock_location[1]))
