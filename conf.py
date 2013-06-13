#! /usr/bin/env python
#-*- coding: utf-8 -*-

""" Program variables.

This file contain the variables used by pyHIDS.
"""

"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010-2013 Cedric Bonhomme

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

pyHIDS Copyright (C) 2010-2013 Cedric Bonhomme
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2013/02/16 $"
__revesion__ = "$Date: 2013/02/16 $"
__copyright__ = "Copyright (c) 2010-2013 Cedric Bonhomme"
__license__ = "GPL v3"

import os
import configparser
# load the configuration
config = configparser.SafeConfigParser()
try:
    config.read("./conf.cfg")
except:
    config.read("./conf.cfg-sample")

PATH = os.path.abspath(".")

NB_BITS = int(config.get('globals','nb_bits'))

MAIL_ENABLED = bool(int(config.get('email','enabled')))
MAIL_FROM = config.get('email','mail_from')
MAIL_TO = [config.get('email','mail_to')]
SMTP_SERVER = config.get('email','smtp')
USERNAME =  config.get('email','username')
PASSWORD =  config.get('email','password')

# address of the log file :
LOGS = os.path.join(PATH, "log")
# address of the database of hash values :
DATABASE = os.path.join(PATH, "base")
# address of the signature of the database:
DATABASE_SIG = os.path.join(PATH, "database.sig")

# path of the private key (to sign the database of hash values) :
PRIVATE_KEY = os.path.join(PATH, "pyhids_rsa")
# path of the public key (to check the integrity of the database) :
PUBLIC_KEY = os.path.join(PATH, "pyhids_rsa.pub")


# specific files to scan :
SPECIFIC_FILES_TO_SCAN = [ \
        os.path.join(PATH, "pyHIDS.py"),
        os.path.join(PATH, "conf.py"),
        os.path.join(PATH, "conf.cfg"),
        #"/etc/cron.hourly/pyHIDS", \
        "/etc/crontab", \
        "/boot/grub/grub.cfg", \
        "/etc/shadow", \
        "/etc/networks"]

# rules to scan folders :
FOLDER_RULES = [ \
                ("conf", "/etc"), \
                ("list", "/etc/apt") \
                ]

# Output of commands :
COMMANDS = []
for name, command in config.items("commands"):
    COMMANDS.append(tuple(command.split(' ')))