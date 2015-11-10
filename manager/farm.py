from multiprocessing.dummy import Pool as ThreadPool
from comms import Printer
from config import *


class Farm:
    def __init__(self):
        self.printers = []
        for printer in PRINTER_CREDENTIALS:
            self.printers.append(Printer(printer['name'],
                                         printer['host'],
                                         printer['api-key']))
        self.update()

    def x(self, c):
        c.get_status()

    def update(self):
        pool = ThreadPool(8)
        pool.map(self.x, self.printers)
        pool.close()
        pool.join()

    def print_status(self):
        for printer in self.printers:
            if printer.online:
                print "{0} {padding} - {1}, {2}  \t{3}".format(printer.name,
                                                               printer.status['temperature']['bed']['actual'],
                                                               printer.status['temperature']['tool0']['actual'],
                                                               printer.status['state']['text'],
                                                               padding=' '*(20-len(printer.name)))

    def printer_by_name(self, name):
        for printer in self.printers:
            if printer.name == name:
                return printer

if __name__ == "__main__":
    farm = Farm()
    farm.print_status()
    #farm.printer_by_name('beta').set_tool_temp(240)
    #farm.printer_by_name('beta').set_bed_temp(80)
    farm.printer_by_name('beta').get_files()