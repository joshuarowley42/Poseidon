import cmd
import os

class Interface(cmd.Cmd):
    """Simple command processor for print farm."""

    def set_farm(self, farm):
        self.farm = farm

    def do_ls(self, line):
        """Show printers and their current status. --> indicates they are selected for commands"""
        self.farm.print_status()

    def do_f(self, line):
        """Show files available on selected printers"""
        if line == "":
            filenames = self.farm.get_files(self.farm.printers_by_selected())
            print "Available Files:"
            for filename in filenames:
                print "   {0}".format(filename)

    def do_s(self, line):
        """Select printers by name / status. Case sensitive. Leave blank to select all"""
        if line == "":
            self.farm.select_all()
        else:
            self.farm.select_by_name_or_status(line)
        self.farm.print_status()

    def do_d(self, line):
        """De-select printers by name / status. Case sensitive. Leave blank to de-select all"""
        if line == "":
            self.farm.select_all(False)
        else:
            self.farm.select_by_name_or_status(line, selection=False)
        self.farm.print_status()

    def complete_s(self, text, line, begidx, endidx):
        if not text:
            completions = [p.name for p in self.farm.printers]
        return completions

    def do_t(self, temp):
        """Set hotend temp on selected printers"""
        temp = int(temp)
        self.farm.set_tool_temp(self.farm.printers_by_selected(), temp)

    def do_b(self, temp):
        """Set bed temp on selected printers"""
        temp = int(temp)
        self.farm.set_bed_temp(self.farm.printers_by_selected(), temp)

    def do_p(self, filename):
        """Print filename on selected printers.
        e.g.
        (Cmd) f
        Available Files:
           07_heatedbed_feet_dock_x2.gcode

        (Cmd) p 07_heatedbed_feet_dock_x2.gcode

        """
        if filename in self.farm.get_files(self.farm.printers_by_selected()):
            self.farm.start_print(self.farm.printers_by_selected(), filename)
        else:
            print 'File not available'

    def do_g(self, line):
        """Send G-Code to selected printers"""
        self.farm.send_gcode(self.farm.printers_by_selected(), line)

    def do_u(self, line):
        """Update status of print farm"""
        self.farm.update()
        self.farm.print_status()

    def do_dock(self, line):
        """Dock selected printers"""
        for printer in self.farm.printers_by_selected():
            printer.dock()

    def do_kill(self, line):
        """Kill prints on selected printers"""
        for printer in self.farm.printers_by_selected():
            printer.kill()

    def do_upload(self, path):
        if path == '':
            path = "/media/PrintFarm/GCode"
        filenames = os.listdir(path)
        for filename in filenames:
            if filename[-6:] == '.gcode':
                full_path = os.path.join(path, filename)
                print full_path
                self.farm.upload_file(full_path, self.farm.printers_by_selected())
            else:
                print 'Not Uploaded{0}'.format(filename)
    def do_q(self, line):
        """Quit"""
        return True
