#! /usr/local/bin/python
#-*- coding: utf-8 -*-

"""pyHIDS. Python HIDS implementation.

pyHIDS verify the integrity of your system.
pyHIDS can prevent the admin by mail, log file and syslog.
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

import os
import time
import pickle
import smtplib
import hashlib
import threading

from email import *

from rsa import rsa
import conf # variables used by the program

def load_base():
    """Load the base file.

    Return a dictionnary wich contains filenames
    and theirs hash value.
    """
    # load the private key (to decrypt the base)
    priv_key = None
    with open(conf.priv_key_location, "rb") as rsa_key:
        priv_key = pickle.load(rsa_key)
        key = rsa.RSA()
        key.a, key.n = priv_key[0], priv_key[1]

    # try to open the saved base of hash values
    base_file = None
    try:
        base_file = open(conf.base_location, "rb")
    except:
        globals()['warning'] = globals()['warning'] + 1
        log("Base file " + conf.base_location + " does no exist.")

    if base_file is not None and priv_key is not None:
        # dictionnary containing the files and hash values
        result = {}
        for line in base_file:
            clearLine = key.decrypt_text(line)
            (address, sha256, _) = clearLine.split(":")
            result[address] = sha256
        base_file.close()
        return result
    return None

def compare_hash(target_file, expected_hash):
    """Compare 2 hash values.

    Compare the hash value of the target file
    with the expected hash value.
    """
    sha256_hash = hashlib.sha256()
    opened_file = None

    # each log's line contain the local time. it makes research easier.
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

    # test for safety. Normally expected_hash != "" thanks to genBase.py
    if expected_hash == "":
        globals()['warning'] = globals()['warning'] + 1
        log(local_time + " No hash value for " + target_file)

    # opening the file to test
    try:
        opened_file = open(target_file, "r")
        data = opened_file.read()
    except:
        globals()['error'] = globals()['error'] + 1
        log(local_time + " [error] " + \
                   target_file + " does not exist. " + \
                  "Or not enough privilege to read it.")
    finally:
        if opened_file is not None:
            opened_file.close()

    # now we're ready to compare the hash values
    if opened_file is not None:
        sha256_hash.update(data.encode())
        hashed_data = sha256_hash.hexdigest()

        if hashed_data == expected_hash:
            # no changes, just write a notice in the log file
            log(local_time + " [notice] "  + target_file + " ok")
        else:
            # hash has change, warning

            # reporting aler in the log file
            globals()['warning'] = globals()['warning'] + 1
            log(local_time + " [warning] " + target_file + \
                      " hash has changed : " + \
                      hashed_data + " != " + expected_hash)

            # reporting alert in syslog
            message = target_file + " hash has changed : " + \
                       hashed_data + " != " + expected_hash
            log_syslog(message)

            # reporting alert via mail
            # this list contains the admins to prevent
            for admin in conf.admin_mail:
                log_mail(conf.sender, \
                        admin, \
                        local_time+"\n"+message+"\n\nHave a nice day !\n\n" + \
                        "\nThis mail was sent to :\n"+"\n".join(conf.admin_mail))


def log(message):
    """Print and save the log in the log file.
    """
    lock.acquire()
    print(message)
    try:
        log_file.write(message+"\n")
    except Exception as e:
        log_syslog(e)
    lock.release()

def log_syslog(message):
    """Write a message in syslog.
    """
    import syslog
    syslog.syslog(message)

def log_mail(mfrom, mto, message):
    """Send the warning via mail
    """
    email = MIMEText(message)
    email['From'] = mfrom
    email['To'] = mto
    email['Subject'] = 'pyHIDS : Alerte'
    #email['Text'] = message

    server = smtplib.SMTP('smtp.orange.fr')
    server.sendmail(mfrom, \
                    mto, \
                    email.as_string())
    server.quit()




if __name__ == "__main__":
    # Point of entry in execution mode

    # lock object to protect the log file during the writing
    lock = threading.Lock()

    # open the log file
    log_file = None
    try:
        log_file = open(conf.log_location, "a")
    except Exception as e:
        print(("Something wrong happens when opening the logs :-(", e))

    log(time.strftime("[%d/%m/%y %H:%M:%S] HIDS starting.", \
                           time.localtime()))

    warning, error = 0, 0

    # dictionnary containing filenames and their hash value.
    base = load_base()
    if base is None:
        print("Base of hash values can not be loaded.")
        exit(0)

    list_of_threads = []
    for file in list(base.keys()):
        if os.path.exists(file):
            thread = threading.Thread(None, compare_hash, \
                                        None, (file, base[file],))
            thread.start()
            list_of_threads.append(thread)
        else:
            error = error + 1
            log(file + "does not exist. " + \
                  "Or not enought privilege to read it.")

    # blocks the calling thread until the thread
    # whose join() method is called is terminated.
    for th in list_of_threads:
        th.join()

    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())
    log(local_time + " Error(s) : " + str(error))
    log(local_time + " Warning(s) : " + str(warning))
    log(local_time + " HIDS finished.")

    if log_file is not None:
        log_file.close()