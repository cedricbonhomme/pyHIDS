#! /usr/bin/env python

import hashlib
import os
import pickle
import re
import subprocess
from typing import BinaryIO, Dict

import rsa

import conf


def search_files(motif, root_path):
    """
    Return a list of files.

    Search for file names containing 'motif' that
    aren't symbolic links.
    """
    result = []
    w = os.walk(root_path)
    for path, _dirs, files in w:
        for f in files:
            if re.compile(motif).search(f):
                # if not a symbolic link
                if not os.path.islink(os.path.join(path, f)):
                    result.append(os.path.join(path, f))
    return result


def hash_file(target_file):
    """
    Hash the file given in parameter.
    """
    sha1_hash = hashlib.sha1()
    hashed_data = None
    data = None

    # Handle the errors that may happen
    try:
        opened_file: BinaryIO = open(target_file, "rb")
        data = opened_file.read()
        opened_file.close()
    except Exception as e:
        # The specified file does not exist,
        # remove from the list.
        print(target_file, ":", e)

    if data is not None:
        sha1_hash.update(data)
        hashed_data = sha1_hash.hexdigest()

    return hashed_data


def main(sign_database=False):
    database: Dict[str, Dict[str, str]] = {}
    database["files"] = {}
    database["commands"] = {}

    # load the specific files to scan
    list_of_files = conf.SPECIFIC_FILES_TO_SCAN

    # adding the folders with rules to scan :
    for rules in conf.FOLDER_RULES:
        list_of_files.extend(search_files(rules[0], rules[1]))
    number_of_files_to_scan = len(list_of_files)

    print("Generating database...")
    # Compute the hash values of each files
    for a_file in list_of_files:
        hash_value = hash_file(a_file)
        if hash_value is not None:
            database["files"][a_file] = hash_value

    # Compute the hash values of each commands
    for command in conf.COMMANDS:
        try:
            proc = subprocess.Popen(
                (command), stderr=subprocess.STDOUT, stdout=subprocess.PIPE
            )
        except FileNotFoundError:
            continue
        command_output = proc.stdout.read()
        sha1_hash = hashlib.sha1()
        sha1_hash.update(command_output)
        hashed_data = sha1_hash.hexdigest()
        database["commands"][command] = hashed_data

    serialized_database = open(conf.DATABASE, "wb")
    pickle.dump(database, serialized_database)
    serialized_database.close()

    print(number_of_files_to_scan, "files in the database.")

    if sign_database:
        print(f"Signing the database in {conf.DATABASE_SIG}")
        # Loads the private key
        with open(conf.PRIVATE_KEY, "rb") as private_key_dump:
            private_key = pickle.load(private_key_dump)

        # Sign the database of hash
        with open(conf.DATABASE, "rb") as msgfile:
            signature = rsa.sign(msgfile, private_key, "SHA-256")

        # Writes the signature in a file.
        with open(conf.DATABASE_SIG, "wb") as signature_file:
            signature_file.write(signature)


if __name__ == "__main__":
    main()
