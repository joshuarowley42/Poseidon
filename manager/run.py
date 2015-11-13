__author__ = 'rowley'

from cli import Interface
from farm import Farm
from monitor import Monitor

print_farm = Farm()
farm_monitor = Monitor()

if __name__ == '__main__':
    interface = Interface()
    interface.set_farm(print_farm)
    interface.cmdloop()
    print 'Bye!'