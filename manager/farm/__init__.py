from printer import Printer
from config import *
from time import sleep, strftime, gmtime
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Process
import re


class Farm:
    def __init__(self):
        self.printers = []
        for printer in PRINTER_CREDENTIALS:
            self.printers.append(Printer(printer['name'],
                                         printer['host'],
                                         printer['api-key'],
                                         printer['dock']))
        self.last_update = None
        self.update()

    def map_x(self, f, o):
        if THREADING:
            pool = ThreadPool(20)
            pool.map(f, o)
            pool.close()
            pool.join()
        else:
            for p in o:
                f(p)

    def update_actions(self, p):
        p.get_status()
        p.get_files()

    def update(self):
        self.map_x(self.update_actions, self.printers)
        #self.prune_offline()
        self.last_update = gmtime()

    def prune_offline(self):
        printers = []
        for printer in self.printers:
            if printer.online:
                printers.append(printer)
        self.printers = printers

    def print_status(self):
        print "Last Update: {0}".format(strftime("%H:%M:%S", self.last_update))
        for printer in self.printers:
            if printer.online:
                print "{sel} {0} {padding} {host} - {1}, {2}  \t{3}".format(printer.name,
                                                                            printer.temperature['bed']['actual'],
                                                                            printer.temperature['tool0']['actual'],
                                                                            printer.state,
                                                                            host=printer.host,
                                                                            padding=' '*(10-len(printer.name)),
                                                                            sel='-->' if printer.selected else '   ')
            else:
                print "    {0} {padding} {host} - xx.x, xxx.x  \t{state}".format(printer.name,
                                                                                 state = printer.state,
                                                                                 host=printer.host,
                                                                                 padding=' '*(10-len(printer.name)))

    def printers_by_name(self, name):
        printers = []
        for printer in self.printers:
            if re.match(name.lower(), printer.name.lower()) is not None:
                print printer.name
                printers.append(printer)
        return printers

    def printers_by_status(self, status):
        printers = []
        for printer in self.printers:
            if re.match(status.lower(), printer.state.lower()) is not None:
                print printer.state
                printers.append(printer)
        return printers

    def printers_by_selected(self, selected=True):
        printers = []
        for printer in self.printers:
            if printer.selected == selected:
                printers.append(printer)
        return printers

    def start_print(self, printers, filename):
        for printer in printers:
            printer.select_file(filename, start_print=True)

    def start_print_managed(self, printers, tool_temp, bed_temp, filename):
        for printer in printers:
            printer.set_bed_temp(bed_temp)
            printer.set_tool_temp(tool_temp)

        for printer in printers:
            printer.get_status()
            while True:
                print "{0} - Waiting to reach temp".format(printer.name)
                if abs(printer.temperature['tool0']['actual'] - tool_temp) > 1:
                    sleep(1)
                    continue
                if abs(printer.temperature['bed']['actual'] - bed_temp) > 2:
                    sleep(1)
                    continue
                break

        for printer in printers:
            result = printer.select_file(filename, start_print=False)
            if result:
                print "File selected for {0}".format(printer.name)

    def send_gcode(self, printers, command):
        for printer in printers:
            printer.send_gcode(command)

    def select_all(self, selection=True):
        for printer in self.printers:
            if printer.online:
                printer.selected = selection
            else:
                printer.selected = False

    def select_by_name_or_status(self, name, selection=True):
        printers = self.printers_by_name(name)
        for printer in printers:
            printer.selected = selection
        printers = self.printers_by_status(name)
        for printer in printers:
            printer.selected = selection

    def set_tool_temp(self, printers, setpoint):
        for printer in printers:
            printer.set_tool_temp(setpoint)

    def set_bed_temp(self, printers, setpoint):
        for printer in printers:
            printer.set_bed_temp(setpoint)

    def get_files(self, printers=None):
        if printers is None:
            printers = self.printers
        filenames = {}
        for printer in printers:
            for filename in printer.files:
                if filename not in filenames.keys():
                    filenames[filename] = [printer.name]
                else:
                    filenames[filename].append(printer.name)

        available_files = []
        for filename in filenames.keys():
            if len(filenames[filename]) == len(printers):
                available_files.append(filename)

        return available_files

if __name__ == "__main__":
    farm = Farm()
    farm.print_status()
    #farm.start_print_managed([farm.printer_by_name('lima')], 240, 80, '07_heatedbed_feet_dock_x2.gcode')
    #farm.send_gcode([farm.printer_by_name('foxtrot')], 'G28 Z0')
    #for printer in farm.printers_by_status('Operational'):
    #    if printer.name != 'foxtrot' and printer.name != 'delta':
    #        printer.select_file('08_single_x1.gcode', start_print=False)
    #        print printer.name

    #farm.printer_by_name('beta').set_tool_temp(240)
    #farm.printer_by_name('beta').set_bed_temp(80)
    #farm.printer_by_name('beta').get_files()