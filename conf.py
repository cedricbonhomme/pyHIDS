#! /usr/bin/env python

"""This module is responsible for loading the configuration variables.
"""

import configparser
import os
from typing import List, Tuple

# load the configuration
config = configparser.ConfigParser()
try:
    configs = config.read(os.environ.get("PYHIDS_CONFIG", "./conf.cfg"))
except Exception as exc:
    raise Exception("No configuration file provided.") from exc

BASE_PATH = os.path.abspath(".")
PATH = config.get("main", "path")
if not PATH:
    PATH = os.path.join(BASE_PATH, "var")
if not os.path.exists(PATH):
    os.makedirs(PATH)

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

HASHLOOKUP_URL = config.get("hashlookup", "root_url")

PANDORA_URL = config.get("pandora", "root_url")
PANDORA_USERNAME = config.get("pandora", "username")
PANDORA_PASSWORD = config.get("pandora", "password")

MISP_URL = config.get("misp", "root_url")
MISP_KEY = config.get("misp", "key")

YARA_RULES = config.get("yara", "rules")
if not os.path.exists(YARA_RULES):
    os.makedirs(YARA_RULES)

BLOOM_LOCATION = config.get("bloom", "location")
BLOOM_CAPACITY = config.getint("bloom", "capacity")
BLOOM_FALSE_POSITIVE_PROBABILITY = config.getfloat(
    "bloom", "false_positive_probability"
)
if not os.path.exists(BLOOM_LOCATION):
    os.makedirs(BLOOM_LOCATION)

CUCKOO_LOCATION = config.get("cuckoo", "location")
CUCKOO_CAPACITY = config.getint("cuckoo", "capacity")
CUCKOO_ERROR_RATE = config.getfloat("cuckoo", "error_rate")
if not os.path.exists(CUCKOO_LOCATION):
    os.makedirs(CUCKOO_LOCATION)

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
SPECIFIC_FILES_TO_SCAN: List[str] = []
for _, current_file in config.items("files"):
    SPECIFIC_FILES_TO_SCAN.append(current_file)

# rules to scan folders :
FOLDER_RULES: List[Tuple] = []
for _, rule in config.items("rules"):
    pattern, folfer = rule.split(" ")
    FOLDER_RULES.append((pattern, folfer))

# Output of commands :
COMMANDS: List[Tuple] = []
for _, command in config.items("commands"):
    COMMANDS.append(tuple(command.split(" ")))
