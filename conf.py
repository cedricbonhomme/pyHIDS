#! /usr/local/bin/python
#-*- coding: utf-8 -*-

""" Program variables.

This file contain the variables used by pyHIDS.
"""

"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010-2013-2013 Cedric Bonhomme

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
__date__ = "$Date: 2013/02/14 $"
__copyright__ = "Copyright (c) 2010-2013-2013 Cedric Bonhomme"
__license__ = "GPL v3"

import os

pyhids_location = os.path.abspath(".")

# address of the log file :
log_location = os.path.join(pyhids_location, "log")
# address of the saved base of hash values :
base_location = os.path.join(pyhids_location, "base")


# address of the private key
# (used only genBase.py by to crypt the base of hash values) :
priv_key_location = os.path.join(pyhids_location, "cle_priv")
# address of the public key (used to decrypt the base of hash values) :
pub_key_location = os.path.join(pyhids_location, "cle_pub")

# mail of admins
admin_mail = ["yourmail@mail.com"]
# mail of the sender
sender = "sendermail@mail.com"


# specific files to scan :
specific_files_to_scan = [ \
        os.path.join(pyhids_location, "pyHIDS.py"),
        os.path.join(pyhids_location, "conf.py"),
        #"/home/cedric/pyHIDS/genBase.py", (genBase.py should not stay on the computer)
        "/etc/cron.hourly/pyHIDS", \
        "/boot/grub/menu.lst", \
        "/etc/shadow", \
        "/etc/crontab", \
        "/etc/networks"]

# rules to scan folders :
folder_rules = [ \
    ("conf", "/etc")]
# used by search_files() in genBase.py
