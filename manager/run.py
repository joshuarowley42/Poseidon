__author__ = 'rowley'

import cmd
from farm import Farm

farm = Farm()

class Interface(cmd.Cmd):
    """Simple command processor for print farm."""

    def do_ls(self, line):
        """Show printers and their current status. --> indicates they are selected for commands"""
        farm.print_status()

    def do_f(self, line):
        """Show files available on selected printers"""
        if line == "":
            filenames = farm.get_files(farm.printers_by_selected())
            print "Available Files:"
            for filename in filenames:
                print "   {0}".format(filename)

    def do_s(self, line):
        """Select printers by name / status. Case sensitive. Leave blank to select all"""
        if line == "":
            farm.select_all()
        else:
            farm.select_by_name_or_status(line)
        farm.print_status()

    def do_d(self, line):
        """De-select printers by name / status. Case sensitive. Leave blank to de-select all"""
        if line == "":
            farm.select_all(False)
        else:
            farm.select_by_name_or_status(line, selection=False)
        farm.print_status()

    def complete_s(self, text, line, begidx, endidx):
        if not text:
            completions = [p.name for p in farm.printers]
        return completions

    def do_t(self, temp):
        """Set hotend temp on selected printers"""
        temp = int(temp)
        farm.set_tool_temp(farm.printers_by_selected(), temp)

    def do_b(self, temp):
        """Set bed temp on selected printers"""
        temp = int(temp)
        farm.set_bed_temp(farm.printers_by_selected(), temp)

    def do_p(self, filename):
        """Print filename on selected printers.
        e.g.
        (Cmd) f
        Available Files:
           07_heatedbed_feet_dock_x2.gcode

        (Cmd) p 07_heatedbed_feet_dock_x2.gcode

        """
        if filename in farm.get_files(farm.printers_by_selected()):
            farm.start_print(farm.printers_by_selected(), filename)
        else:
            print 'File not available'

    def do_g(self, line):
        """Send G-Code to selected printers"""
        farm.send_gcode(farm.printers_by_selected(), line)

    def do_u(self, line):
        """Update status of print farm"""
        farm.update()
        farm.print_status()

    def do_dock(self, line):
        """Dock selected printers"""
        for printer in farm.printers_by_selected():
            printer.dock()

    def do_kill(self, line):
        """Kill prints on selected printers"""
        for printer in farm.printers_by_selected():
            printer.kill()

    def do_q(self, line):
        """Quit"""
        return True

if __name__ == '__main__':
    Interface().cmdloop()