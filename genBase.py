#! /usr/local/bin/python
#-*- coding: utf-8 -*-

"""This script generates the base of hash values.
"""

"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010 Cedric Bonhomme

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

pyHIDS Copyright (C) 2010 Cedric Bonhomme
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Cedric Bonhomme"
__date__ = "$Date: 2010/03/06 $"
__copyright__ = "Copyright (c) 2010 Cedric Bonhomme"
__license__ = "GPL v3"

import hashlib
import pickle
import os
import glob
import re

from rsa import rsa
import conf  # variables used by the program

def search_files(motif, root_path):
    """Return a list of files.

    Search fo files containing 'motif' that
    aren't symbolic links.
    """
    result = []
    w = os.walk(root_path)
    for (path, dirs, files) in w:
        for f in files:
            if re.compile(motif).search(f):
                # if not a symbolic link
                if not os.path.islink(os.path.join(path, f)):
                    result.append(os.path.join(path, f))
    return result

def hash_file(target_file):
    """Hash the file given in parameter.
    """
    sha256_hash = hashlib.sha256()
    opened_file = None
    hashed_data = None

    # Handle the errors that may happen
    try:
        opened_file = open(target_file, "r")
        data = opened_file.read()
    except:
        # The specified file does not exist,
        # remove from the list.
        print("File", target_file, "does not exist.")
        globals()['number_of_files_to_scan'] = \
            globals()['number_of_files_to_scan'] - 1
        del list_of_files[list_of_files.index(target_file)]
    finally:
        if opened_file is not None:
            opened_file.close()

    if opened_file is not None:
        sha256_hash.update(data.encode('utf-8'))
        hashed_data = sha256_hash.hexdigest()

    return hashed_data



if __name__ == '__main__':
    # Point of entry in execution mode.
    print("Loading public key")

    # Load the public key to crypt the result.
    with open(conf.pub_key_location, "rb") as key:
        pub_key = pickle.load(key)
        key = rsa.RSA()
        key.b, key.n = pub_key[0], pub_key[1]

    # Open the base of hash values
    try:
        base = open(conf.base_location, "w")
    except Exception as e:
        print("Error :", e)
        exit(0)


    # load the specific files to scan
    list_of_files = conf.specific_files_to_scan

    # adding the folders with rules to scan :
    for rules in conf.folder_rules:
        list_of_files.extend(search_files(rules[0], rules[1]))
    number_of_files_to_scan = len(list_of_files)


    print("Generating data base...")
    # Hash and write each files
    for a_file in list_of_files:
        hash_value = hash_file(a_file)
        if hash_value is not None:
            line = a_file + ":" + hash_value + ":"
            encrypted_line = key.encrypt_text(line)
            encrypted_line = encrypted_line.decode().replace('\n', '')
            base.write(encrypted_line+"\n")
    print(number_of_files_to_scan, "files in the base.")
    base.close()