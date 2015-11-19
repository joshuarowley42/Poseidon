import cmd
import os
from config import *

class Interface(cmd.Cmd):
    """Simple command processor for print farm."""

    def set_farm(self, farm):
        self.farm = farm

    def do_ls(self, line):
        """Show printers and their current status.
            --> indicates they are selected for commands
        Usage:
            (cmd) ls

        Output:
            Last Update: 11:50:09
                IP  Name          Bed   SetPoint    HE     SetPoint Status   %     Time Remaining
            --> 220 alpha         80.0  80.0        229.1  240.0    Printing 57.1% 02:13:39
            --> 221 beta          80.1  80.0        240.2  240.0    Printing 57.0% 02:13:42
            --> 222 charlie       80.0  80.0        239.3  240.0    Printing 57.0% 02:13:42
            --> 223 delta         120.0  120.0      238.6  240.0    Printing 31.2% 07:32:54
            --> 224 echo          80.1  80.0        240.2  240.0    Printing 57.0% 02:13:42
                225 foxtrot       80.1  80.0        240.2  240.0    Printing 57.1% 02:13:37
            --> 226 golf          80.0  80.0        239.9  240.0    Printing 57.0% 02:13:38
            --> 227 hotel         80.0  80.0        240.2  240.0    Printing 57.0% 02:13:37
            --> 228 india         80.0  80.0        226.8  240.0    Printing 57.0% 02:13:37
            --> 229 juliet        80.0  80.0        240.2  240.0    Printing 57.0% 02:13:39
            --> 230 kilo          80.0  80.0        240.0  240.0    Printing 56.0% 02:20:11
                231 lima          79.9  80.0        240.1  240.0    Operational
            --> 232 mike          80.0  80.0        239.7  240.0    Printing 57.0% 02:14:02
            --> 234 oscar         80.0  80.0        239.9  240.0    Printing 57.0% 02:13:33

            """
        self.farm.update()
        self.farm.print_status(show_details=True)

    def do_f(self, line):
        """Show files available on all of the selected printers.
        Usage:
            (cmd) f

        Output:
            Available Files:
               01_z_axis_cover_brackets_x2.gcode
               02_y_axis_small_x4.gcode
               03_y_axis_large_x2.gcode
               04_x_axis_x2.gcode
               05_spools_x4.gcode
               06_spine_x2.gcode
               07_heatedbed_feet_dock_x2.gcode
               08_single_x1.gcode
               09_dual_x1.gcode
               10_octopi_x4.gcode
               11_hi_temp_x5.gcode
        """
        if line == "":
            filenames = self.farm.get_files(self.farm.printers_by_selected())
            print "Available Files:"
            for filename in filenames:
                print "   {0}".format(filename)

    def do_s(self, line):
        """Select printers by name / status. Case sensitive. Leave blank to select all. Tab completion should work
        for printer names.

        Example:
            (cmd) s op
            -- Will select all printers with status/names beginning with 'op'.
            (cmd s
            -- Will select all printers
        """
        if line == "":
            self.farm.select_all()
        else:
            self.farm.select_by_name_or_status(line)
        self.farm.print_status()

    def do_d(self, line):
        """Deselect printers by name / status. Case sensitive. Leave blank to deselect all. Tab completion should work
        for printer names.
        Example:
            (cmd) d op
            -- Will de-select all printers with status/names beginning with 'op'
            (cmd s
            -- Will de-select all printers
        """
        if line == "":
            self.farm.select_all(False)
        else:
            self.farm.select_by_name_or_status(line, selection=False)
        self.farm.print_status()

    def complete_s(self, text, line, begidx, endidx):
        if text == "":
            completions = [p.name for p in self.farm.printers]
        else:
            completions = [p.name for p in self.farm.printers if p.name.startswith(text)]
        return completions

    def complete_d(self, text, line, begidx, endidx):
        if text == "":
            completions = [p.name for p in self.farm.printers]
        else:
            completions = [p.name for p in self.farm.printers if p.name.startswith(text)]
        return completions

    def do_t(self, temp):
        """Set hotend temp on selected printers

        Example:
            (cmd) t 240
            -- Will set the HotEnd to 240.

        """
        temp = int(temp)
        self.farm.set_tool_temp(self.farm.printers_by_selected(), temp)

    def do_b(self, temp):
        """Set bed temp on selected printers

        Example:
            (cmd) b 80
            -- Will set the Bed to 80.

        """
        temp = int(temp)
        self.farm.set_bed_temp(self.farm.printers_by_selected(), temp)

    def do_p(self, filename):
        """Print filename on selected printers. Tab completion should work for available files.

        Examples:
            (Cmd) f
            Available Files:
               07_heatedbed_feet_dock_x2.gcode

            (Cmd) p 07_heatedbed_feet_dock_x2.gcode

        """
        if filename in self.farm.get_files(self.farm.printers_by_selected()):
            self.farm.start_print(self.farm.printers_by_selected(), filename)
        else:
            print 'File not available'

    def complete_p(self, text, line, begidx, endidx):
        filenames = self.farm.get_files(self.farm.printers_by_selected())
        if text == "":
            return filenames
        else:
            return [f for f in filenames if f.startswith(text)]


    def do_g(self, line):
        """Send G-Code to selected printers.
        Usage:
            (cmd) g G1 X150 Y100 F3000

        """
        self.farm.send_gcode(self.farm.printers_by_selected(), line)

    def do_u(self, line):
        print "Depreciated - use `ls`"

    def do_dock(self, line):
        print "Depreciated - use `script dock`"

    def do_kill(self, line):
        """Kill prints on selected printers.
        Usage:
            (cmd) kill

        """
        for printer in self.farm.printers_by_selected():
            printer.kill()

    def do_script(self, line):
        """ Run a script as defined in config/__init__.py. Tab complete should work.
        Usage:
            (Cmd) script
            Available Scripts:
               purge
               dock
               clean

            (Cmd) script purge

        """
        if line == "":
            scripts = SCRIPTS.keys()
            print "Available Scripts:"
            for script in scripts:
                print "   {0}".format(script)
        else:
            self.farm.run_script(line, self.farm.printers_by_selected())

    def complete_script(self, text, line, begidx, endidx):
        if text == "":
            return SCRIPTS.keys()
        else:
            return [s for s in SCRIPTS.keys() if s.startswith(text)]


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
