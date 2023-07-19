#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""pyHIDS. Python HIDS implementation.

pyHIDS verify the integrity of your system.
pyHIDS can send alerts by email, log file and syslog.
"""

"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010-2023 Cedric Bonhomme

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

pyHIDS Copyright (C) 2010-2023 Cedric Bonhomme
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.6 $"
__date__ = "$Date: 2010/03/06 $"
__revision__ = "$Date: 2023/07/19 $"
__copyright__ = "Copyright (c) 2010-2023 Cedric Bonhomme"
__license__ = "GPL v3"

import os
import sys
import socket
import json
import time
import pickle
import hashlib
import threading, queue
import subprocess
import rsa
from contextlib import contextmanager

import smtplib
from email.mime.text import MIMEText

import conf

# lock object to protect the log file during the writing
lock = threading.Lock()
# lock object used when sending alerts via irc
irker_lock = threading.Lock()

Q = queue.Queue()


def load_base():
    """
    Load the base file.

    Return a dictionnary wich contains filenames
    and theirs hash value.
    """
    # try to open the saved base of hash values
    database = None
    with open(conf.DATABASE, "rb") as serialized_database:
        database = pickle.load(serialized_database)
    # try:
    # base_file = open(conf.DATABASE, "r")
    # except:
    # globals()['warning'] = globals()['warning'] + 1
    # log("Base file " + conf.DATABASE + " does no exist.")
    return database


def compare_hash(target_file, expected_hash):
    """
    Compare 2 hash values.

    Compare the hash value of the target file
    with the expected hash value.
    """
    sha256_hash = hashlib.sha256()
    opened_file = None

    # each log's line contain the local time. it makes research easier.
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

    # test for safety. Normally expected_hash != "" thanks to genBase.py
    if expected_hash == "":
        globals()["warning"] = globals()["warning"] + 1
        log(local_time + " No hash value for " + target_file)

    # opening the file to test
    try:
        opened_file = open(target_file, "rb")
        data = opened_file.read()
    except:
        globals()["error"] = globals()["error"] + 1
        log(
            local_time
            + " [error] "
            + target_file
            + " does not exist. "
            + "Or not enough privilege to read it."
        )
    finally:
        if opened_file is not None:
            opened_file.close()

    # now we're ready to compare the hash values
    if opened_file is not None:
        sha256_hash.update(data)
        hashed_data = sha256_hash.hexdigest()

        if hashed_data == expected_hash:
            # no changes, just write a notice in the log file
            log(local_time + " [notice] " + target_file + " ok")
        else:
            # hash has changed, warning

            # reporting aler in the log file
            globals()["warning"] = globals().get("warning", 0) + 1
            message = local_time + " [warning] " + target_file + " changed."

            # pyHIDS log
            log(message, True)

            # reporting alert in syslog
            log_syslog(message)

            if conf.IRC_CHANNEL != "":
                # reporting alert via IRC
                log_irker(conf.IRC_CHANNEL, message)

            if conf.MAIL_ENABLED:
                Q.put(message + "\n")


def compare_command_hash(command, expected_hash):
    # each log's line contain the local time. it makes research easier.
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

    proc = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    command_output = proc.stdout.read()
    sha256_hash = hashlib.sha256()
    sha256_hash.update(command_output)
    hashed_data = sha256_hash.hexdigest()

    if hashed_data == expected_hash:
        # no changes, just write a notice in the log file
        log(local_time + " [notice] " + " ".join(command) + " ok")
    else:
        # hash has changed, warning

        # reporting aler in the log file
        globals()["warning"] = globals()["warning"] + 1
        message = (
            local_time
            + " [warning] "
            + " ".join(command)
            + " command output has changed."
        )

        # pyHIDS log
        log(message, True)

        # reporting alert in syslog
        log_syslog(message)

        if conf.IRC_CHANNEL != "":
            # reporting alert via IRC
            log_irker(conf.IRC_CHANNEL, message)

        if conf.MAIL_ENABLED:
            Q.put(message + "\n")


@contextmanager
def opened_w_error(filename, mode="r"):
    try:
        f = open(filename, mode)
    except IOError as err:
        yield None, err
    else:
        try:
            yield f, None
        finally:
            f.close()


def log(message, display=False):
    """
    Print and save the log in the log file.
    """
    lock.acquire()
    if display:
        print(message)
    try:
        log_file = open(conf.LOGS, "a")
    except Exception as e:
        log_syslog("Something wrong happens when opening the logs: " + str(e))
        print("Something wrong happens when opening the logs: " + str(e))
        exit(0)
    try:
        log_file.write(message + "\n")
    except Exception as e:
        print(e)
        # log_syslog(e)
    lock.release()


def log_syslog(message):
    """
    Write a message in syslog.
    """
    import syslog

    syslog.syslog("pyHIDS - " + message)


def log_mail(mfrom, mto, message):
    """
    Send the warning via mail
    """
    email = MIMEText(message, "plain", "utf-8")
    email["From"] = mfrom
    email["To"] = mto
    email["Subject"] = "pyHIDS : Alert"
    # email['Text'] = message

    server = smtplib.SMTP(conf.SMTP_SERVER)
    server.login(conf.USERNAME, conf.PASSWORD)
    server.send_message(email)
    server.quit()


def log_irker(target, message):
    irker_lock.acquire()
    data = {"to": target, "privmsg": message}
    try:
        s = socket.create_connection((conf.IRKER_HOST, conf.IRKER_PORT))
        s.sendall(json.dumps(data).encode("utf-8"))
    except socket.error as e:
        sys.stderr.write("irkerd: write to server failed: %r\n" % e)
    finally:
        irker_lock.release()


def main(check_signature=False):
    if check_signature:
        print("Verifying the integrity of the base of hashes...")
        with opened_w_error(conf.PUBLIC_KEY, "rb") as (public_key_dump, err):
            if err:
                print(str(err))
                exit(0)
            else:
                public_key = pickle.load(public_key_dump)

        with opened_w_error(conf.DATABASE_SIG, "rb") as (signature_file, err):
            if err:
                print(str(err))
                exit(0)
            else:
                signature = signature_file.read()

        with opened_w_error(conf.DATABASE, "rb") as (msgfile, err):
            if err:
                print(str(err))
                exit(0)
            else:
                try:
                    rsa.verify(msgfile, signature, public_key)
                    print("Database integrity verified.")
                except rsa.pkcs1.VerificationError as e:
                    log_syslog("Integrity check of the base of hashes failed.")
                    print("Integrity check of the base of hashes failed.")
                    exit(0)

    print("Verifying the integrity of the files...")
    # open the log file
    log_file = None
    try:
        log_file = open(conf.LOGS, "a")
    except Exception as e:
        log_syslog("Something wrong happens when opening the logs: " + str(e))
        print("Something wrong happens when opening the logs: " + str(e))
        exit(0)
    log(time.strftime("[%d/%m/%y %H:%M:%S] HIDS starting.", time.localtime()))

    warning, error = 0, 0

    # dictionnary containing filenames and their hash value.
    base = load_base()
    if base is None:
        print("Base of hash values can not be loaded.")
        exit(0)

    report = ""

    # Check the integrity of monitored files
    list_of_threads = []
    for file in list(base["files"].keys()):
        if os.path.exists(file):
            thread = threading.Thread(
                None,
                compare_hash,
                None,
                (
                    file,
                    base["files"][file],
                ),
            )
            thread.start()
            list_of_threads.append(thread)

        else:
            error = error + 1
            log(file + " does not exist. " + "Or not enought privilege to read it.")

    # Check the integrity of commands output
    for command in list(base["commands"].keys()):
        thread = threading.Thread(
            None,
            compare_command_hash,
            None,
            (
                command,
                base["commands"][command],
            ),
        )
        thread.start()
        list_of_threads.append(thread)

    # blocks the calling thread until the thread
    # whose join() method is called is terminated.
    for th in list_of_threads:
        th.join()

    while not Q.empty():
        report += Q.get(True, 0.5)

    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())
    log(local_time + " Error(s) : " + str(error))
    log(local_time + " Warning(s) : " + str(warning))
    log(local_time + " HIDS finished.")

    if log_file is not None:
        log_file.close()

    if conf.MAIL_ENABLED:
        if report != "":
            # reporting alert via mail
            # this list contains the admins to prevent
            for admin in conf.MAIL_TO:
                log_mail(
                    conf.MAIL_FROM,
                    admin,
                    report
                    + "\n\nHave a nice day !\n\n"
                    + "\nThis mail was sent to :\n"
                    + "\n".join(conf.MAIL_TO),
                )
        message = "A system check successfully terminated at " + local_time + "."
        for admin in conf.MAIL_TO:
            log_mail(
                conf.MAIL_FROM,
                admin,
                message
                + "\n\nHave a nice day !\n\n"
                + "\nThis mail was sent to :\n"
                + "\n".join(conf.MAIL_TO),
            )


if __name__ == "__main__":
    # Point of entry in execution mode
    main()
