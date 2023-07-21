#! /usr/bin/env python

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

import configparser
import os

# load the configuration
config = configparser.SafeConfigParser()
try:
    config.read(os.environ.get("PYHIDS_CONFIG", "./conf.cfg"))
except Exception:
    raise Exception("No configuration file provided.")

PATH = os.path.abspath(".")

IRC_ENABLED = bool(config.getint("irc", "enabled"))
IRC_CHANNEL = config.get("irc", "channel")
IRKER_HOST = config.get("irc", "host")
IRKER_PORT = int(config.get("irc", "port"))

MAIL_ENABLED = bool(config.getint("email", "enabled"))
MAIL_FROM = config.get("email", "mail_from")
MAIL_TO = [config.get("email", "mail_to")]
SMTP_SERVER = config.get("email", "smtp")
USERNAME = config.get("email", "username")
PASSWORD = config.get("email", "password")

# address of the log file :
LOGS = os.path.join(PATH, "log")
# address of the database of hash values :
DATABASE = os.path.join(PATH, "database")
# address of the signature of the database:
DATABASE_SIG = os.path.join(PATH, "database.sig")

# path of the private key (to sign the database of hash values) :
PRIVATE_KEY = os.path.join(PATH, "pyhids_rsa")
# path of the public key (to check the integrity of the database) :
PUBLIC_KEY = os.path.join(PATH, "pyhids_rsa.pub")


# specific files to scan :
SPECIFIC_FILES_TO_SCAN = []
for _, current_file in config.items("files"):
    SPECIFIC_FILES_TO_SCAN.append(current_file)

# rules to scan folders :
FOLDER_RULES = []
for _, rule in config.items("rules"):
    pattern, folfer = rule.split(" ")
    FOLDER_RULES.append((pattern, folfer))

# Output of commands :
COMMANDS = []
for _, command in config.items("commands"):
    COMMANDS.append(tuple(command.split(" ")))
