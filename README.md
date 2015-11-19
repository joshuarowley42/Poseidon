Poseidon
=========

Poseidon provides a command line interface for multiple OctoPrint servers.

It is Free Software and released under the [GNU Affero General Public License V3](http://www.gnu.org/licenses/agpl.html).

![Screenshot](http://i.imgur.com/Sy96wnH.png)

Functionality
-------------

Currently the following features exist within Poseidon:

    * Show the current status of all printers in the farm
    * Select / deselect printers based on name / status

Perform the following operations on selected printers

    * Set Temp of Extruder O
    * Set Temp of Bed
    * Send arbitrary G-Codes
    * List common .gcode files
    * Batch upload .gcode files
    * Start Print
    * Kill Print
    * Home X/Y then go to pre-defined dock location

Contributing
------------

Please contribute! This is an accidental project spawned from a need to run the BigBox print farm at E3D. I am not a
seasoned python developer and accordingly there may be some things in here that upset people out there. I look forward
to seeing where this goes.


Installation
------------

Quick Instructions
1. Install the python requests module: (e.g. `sudo apt-get install python-requests`).
2. Create and change into the Poseidon directory: `mkdir Poseidon; cd Poseidon`
3. Checkout Poseidon: `git clone https://github.com/joshuarowley42/Poseidon.git`
4. Modify the config accordingly: `vim manager/config/__init__.py`
5. Run the manager: `python run.py`

Proper Instructions
1. Create and change into folder for Poseidon
2. Create a virtualenv: `virtualenv .`
3. Activate virtualenv: `source bin/activate`
4. Checkout Poseidon: `git clone https://github.com/joshuarowley42/Poseidon.git`
5. Install requirements: `pip install -r requirements.txt`
6. Run the manager: `python run.py`


Dependencies
------------

Currently only requests.

Usage
-----

Running Poseidon:

    python run.py

Commands:

    General Commands
    ls      - Lists printers and state. NOTE: DOES NOT UPDATE STATE
    u       - Update state of all printers.

    Printer Selection
    s xxxx  - Select printers by name / status. No args selects all.
    d xxxx  - Deselect printers by name / status. No args deselects all.

    Printer Actions
    t xx    - Set HotEnd 0 Temp
    b xx    - Set Bed Temp
    g xx    - Send arbitrary GCodes
    dock    - Home X & Y. Go to Dock.
    script xx - Run Gcode Script (defined in config/__init__.py)

    File Actions
    f       - List files common to selected printers
    upload  - Upload all files in uplaod folder to selected printers (see config/__init__.py)

    Job Actions
    p x.gcode   - Print named file
    kill        - Kill current job


Special Thanks
--------------

We are standing on the shoulders of giants. Thanks to the [OctoPrint](https://github.com/foosel/OctoPrint) project.
