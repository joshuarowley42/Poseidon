from comms import Printer
from config import *
from time import sleep
from multiprocessing.dummy import Pool as ThreadPool


class Farm:
    def __init__(self):
        self.printers = []
        for printer in PRINTER_CREDENTIALS:
            self.printers.append(Printer(printer['name'],
                                         printer['host'],
                                         printer['api-key']))
        self.update()

    def x(self, p):
        p.get_status()
        p.get_files()

    def update(self):
        if THREADING:
            pool = ThreadPool(8)
            pool.map(self.x, self.printers)
            pool.close()
            pool.join()
        else:
            for p in self.printers:
                self.x(p)

        #self.prune_offline()

    def prune_offline(self):
        printers = []
        for printer in self.printers:
            if printer.online:
                printers.append(printer)
        self.printers = printers

    def print_status(self):
        for printer in self.printers:
            if printer.online:
                print "{0} {padding} {host} - {1}, {2}  \t{3}".format(printer.name,
                                                                      printer.temperature['bed']['actual'],
                                                                      printer.temperature['tool0']['actual'],
                                                                      printer.state,
                                                                      host=printer.host,
                                                                      padding=' '*(10-len(printer.name)))
            else:
                print "{0} {padding} {host} - xx.x, xxx.x  \t{state}".format(printer.name,
                                                                            state = printer.state,
                                                                            host=printer.host,
                                                                            padding=' '*(20-len(printer.name)))

    def printer_by_name(self, name):
        for printer in self.printers:
            if printer.name == name:
                return printer

    def printers_by_status(self, status):
        printers = []
        for printer in self.printers:
            if printer.state == status:
                printers.append(printer)
        return printers

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