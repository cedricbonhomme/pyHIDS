## pyHIDS

### Presentation

[pyHIDS](https://github.com/cedricbonhomme/pyHIDS) is a
[HIDS](http://en.wikipedia.org/wiki/Host-based_intrusion_detection_system)
(host-based intrusion detection system) for verifying the integrity of a system.

It is possible to use an RSA signature to check the integrity of its database.

Alerts are written in the logs of the system and can be sent via email
to a list of users. You can define rules to specify files to be checked.

It is recommended to use Python >= 3.11.

### Features

* checks the integrity of system's files with a list of rules;
* checks the output of commands (*iptables*, ...);
* uses an RSA signature to check the integrity of its database;
* alerts are written in the logs of the system;
* alerts can be sent via email to a list of users;
* alerts can be sent on IRC channels through the
  [irker](https://gitlab.com/esr/irker) IRC client (which should be running as
  a daemon).


### Installation

#### Installation as a command line tool

You can simply use [pipx](https://pypa.github.io/pipx/).

```bash
$ pipx install pyHIDS
$ export PYHIDS_CONFIG=~/.pyHIDS/conf.cfg

$ pyhids gen-keys --size 2048
Generating 2048 bits RSA keys ...
Dumping Keys
Done.

$ pyhids gen-base --sign
Generating database...
2427 files in the database.

$ pyhids run --check-signature
Verifying the integrity of the base of hashes...
Database integrity verified.
Verifying the integrity of the files...
```

As you can see you can skip the first step (generation of the keys)
if you do not want to sign the database with the solution provided
with pyHIDS (RSA) or if you simply do not want to sign the database.

As an example you can modify a character in a monitored file and
relaunch the program:

```bash
$ pyhids run
Verifying the integrity of the files...
[07/19/23 15:05:31] [warning] /etc/httpd/conf/httpd.conf changed.
```

The program warns that the file has changed. When this happens, a warning is
generated in the logs **/var/log/syslog** and a mail is sent to the
administrator.
If no change is detected only the log file is updated.


Log file generated:

```bash
$ tail log
[18/07/23 22:34:25] [notice] /bin/tload ok
[18/07/23 22:34:25] [notice] /bin/mbim-network ok
[18/07/23 22:34:25] [notice] /bin/preparetips5 ok
[18/07/23 22:34:25] [notice] /bin/grub-file ok
[18/07/23 22:34:25] [notice] /bin/xclip ok
[18/07/23 22:34:25] [notice] /bin/pamperspective ok
[18/07/23 22:34:25] [notice] /bin/pod2usage ok
[18/07/23 22:34:25] Error(s) : 0
[18/07/23 22:34:25] Warning(s) : 0
[18/07/23 22:34:25] HIDS finished.
```


#### From the repository

Get pyHIDS source code and copy the
sample configuration file:

```bash
$ git clone https://github.com/cedricbonhomme/pyHIDS.git
$ cd pyHIDS/
$ cp ./conf.cfg-sample ./conf.cfg
$ poetry install
```

The same as explained above applies.


### Configuration

The configuration file of pyHIDS looks like the following:

```ini
[irc]
channel = irc://irc.libera.chat/#testpyHIDS
host = localhost
port = 6697
[email]
enabled = 0
mail_from = pyHIDS@no-reply.com
mail_to = you_address
smtp = SMTP_server
username = your_username
password = your_password
[files]
file1 = /etc/crontab
file2 = /boot/grub/grub.cfg
file3 = /etc/shadow
file4 = /etc/networks
[rules]
rule1 = conf$ /etc
rule2 = list /etc/apt
rule3 = .* /bin
[commands]
iptables = /sbin/iptables -L
```

Description of the sections:

* *irc*: configure notifications sent via IRC;
* *email*: configure the email notifications. Set the value of "enabled" to 1
  to activate notifications;
* *files*: list of files to scan;
* *rules*: regular expression to specify files in a folder;
* *commands*: command's output to check.



### Automatic execution

Use the time-based job scheduler, Cron, in order to schedule system scans.
In your shell enter the command:

```bash
$ crontab -e
```

And add the following line to check the integrity of the system every fifty
minutes:

```bash
*/50 * * * * pyhids run
```

After each system check, pyHIDS sends a report to the administrators.
In the case of an attacker who has deleted the cron line, for example.


### License

[pyHIDS](https://github.com/cedricbonhomme/pyHIDS) is under
[GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt) license.

Copyright (C) 2010-2023 [Cédric Bonhomme](https://www.cedricbonhomme.org)
