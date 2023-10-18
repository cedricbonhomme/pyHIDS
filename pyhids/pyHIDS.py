#!/usr/bin/env python

import hashlib
import json
import os
import pickle
import smtplib
import socket
import subprocess
import sys
import syslog
import threading
import time
from email.mime.text import MIMEText
from queue import Queue

import rsa

import conf
from pyhids import utils

# lock object to protect the log file during the writing
lock = threading.Lock()
# lock object used when sending alerts via irc
irker_lock = threading.Lock()

Q: Queue[str] = Queue()


def compare_file_hash(target_file: str, expected_hash: str, verbose: bool = False):
    """
    Compare 2 hash values.

    Compare the hash value of the target file
    with the expected hash value.
    """
    sha1_hash = hashlib.sha1()
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
    except Exception:
        globals()["error"] = globals().get("error", 0) + 1
        log(
            local_time
            + " [error] "
            + target_file
            + " does not exist"
            + " or not enough rights to read it.",
            True,
        )
    finally:
        if opened_file is not None:
            opened_file.close()

    # now we're ready to compare the hash values
    if opened_file is not None:
        sha1_hash.update(data)
        hashed_data = sha1_hash.hexdigest()

        if hashed_data == expected_hash:
            # no changes, just write a notice in the log file
            log(local_time + " [notice] " + target_file + " ok", verbose)
        else:
            # hash has changed, warning

            # reporting alert in the log file
            globals()["warning"] = globals().get("warning", 0) + 1
            message = local_time + " [warning] " + target_file + " changed."

            # pyHIDS log
            log(message, True)

            # reporting alert in syslog
            log_syslog(message)

            if conf.IRC_ENABLED:
                # reporting alert via IRC
                log_irker(conf.IRC_CHANNEL, message)

            if conf.MAIL_ENABLED:
                Q.put(message + "\n")


def compare_command_hash(command: str, expected_hash: str, verbose: bool = True):
    # each log's line contain the local time. it makes research easier.
    local_time = time.strftime("[%d/%m/%y %H:%M:%S]", time.localtime())

    proc = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    command_output = proc.stdout.read()
    sha1_hash = hashlib.sha1()
    sha1_hash.update(command_output)
    hashed_data = sha1_hash.hexdigest()

    if hashed_data == expected_hash:
        # no changes, just write a notice in the log file
        log(local_time + " [notice] " + " ".join(command) + " ok", verbose)
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

        if conf.IRC_ENABLED:
            # reporting alert via IRC
            log_irker(conf.IRC_CHANNEL, message)

        if conf.MAIL_ENABLED:
            Q.put(message + "\n")


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
        log_syslog("There was a problem opening the logs: " + str(e))
        print("There was a problem opening the logs: " + str(e))
        exit(1)
    try:
        log_file.write(message + "\n")
    except Exception as e:
        log_syslog(e)
    lock.release()


def log_syslog(message):
    """
    Write a message in syslog.
    """
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
    except OSError as e:
        sys.stderr.write("irkerd: write to server failed: %r\n" % e)
    finally:
        irker_lock.release()


def main(check_signature: bool = False, verbose: bool = False):
    globals()["warning"] = globals().get("warning", 0)
    globals()["error"] = globals().get("error", 0)
    if check_signature:
        print("Verifying the integrity of the base of hashes...")
        with utils.opened_w_error(conf.PUBLIC_KEY, "rb") as (public_key_dump, err):
            if err:
                print(str(err))
                exit(1)
            else:
                public_key = pickle.load(public_key_dump)

        with utils.opened_w_error(conf.DATABASE_SIG, "rb") as (signature_file, err):
            if err:
                print(str(err))
                exit(1)
            else:
                signature = signature_file.read()

        with utils.opened_w_error(conf.DATABASE, "rb") as (msgfile, err):
            if err:
                print(str(err))
                exit(1)
            else:
                try:
                    rsa.verify(msgfile, signature, public_key)
                    print("Database integrity verified.")
                except rsa.pkcs1.VerificationError:  # type: ignore
                    log_syslog("Integrity check of the base of hashes failed.")
                    print("Integrity check of the base of hashes failed.")
                    exit(1)

    print("Verifying the integrity of the files...")
    # open the log file
    log_file = None
    try:
        log_file = open(conf.LOGS, "a")
    except Exception as e:
        log_syslog("There was a problem opening the logs: " + str(e))
        print("There was a problem opening the logs: " + str(e))
        exit(1)
    log(time.strftime("[%d/%m/%y %H:%M:%S] HIDS starting.", time.localtime()))

    # dictionnary containing filenames and their hash value.
    base = utils.load_base()

    report = ""

    # Check the integrity of monitored files
    list_of_threads = []
    for file in list(base["files"].keys()):
        if os.path.exists(file):
            thread = threading.Thread(
                None,
                compare_file_hash,
                None,
                (
                    file,
                    base["files"][file],
                    verbose,
                ),
            )
            thread.start()
            list_of_threads.append(thread)

        else:
            globals()["error"] = globals().get("error", 0) + 1
            log(
                file + " does not exist or not enought rights to read it.",
                True,
            )

    # Check the integrity of commands output
    for command in list(base["commands"].keys()):
        thread = threading.Thread(
            None,
            compare_command_hash,
            None,
            (
                command,
                base["commands"][command],
                verbose,
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
    log(local_time + " Error(s) : " + str(globals()["error"]), True)
    log(local_time + " Warning(s) : " + str(globals()["warning"]), True)
    log(local_time + " HIDS finished.", True)

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
