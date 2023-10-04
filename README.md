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
* possibity to use RSA to sign to check the integrity of its database;
* verify files with [Hashlookup](https://github.com/hashlookup);
* verify files with [Pandora](https://github.com/pandora-analysis);
* verify files with [MISP](https://github.com/MISP);
* alerts are written in the logs of the system;
* alerts can be sent via email to a list of users;
* alerts can be sent on IRC channels through the
  [irker](https://gitlab.com/esr/irker) IRC client (which should be running as
  a daemon).


### Installation

You can simply use [pipx](https://pypa.github.io/pipx/)
or [poetry](https://python-poetry.org/).

```bash
$ pipx install pyHIDS
$ export PYHIDS_CONFIG=~/.pyHIDS/conf.cfg
```

[An example](./conf.cfg-sample) of configuration file is available.
With this file you can configure:

- the connection to Hashlookup;
- the connection to Pandora;
- the IRC connection for the notifications;
- the SMTP connection for the email notifications;
- the list of files to scan;
- the regular expressions to specify files to scan in a folder;
- the command's output to check.


### Usage

```bash
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

You can skip the first step (generation of the keys) if you do not want to
sign the database with the solution provided with pyHIDS (RSA) or if you
do not want to sign the database.

Change a monitored file and relaunch the program:

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


### Other features

Check for known malicious files with
[Hashlookup](https://github.com/hashlookup):

```bash
$ pyhids hashlookup
```

Check for known malicious files with
[Pandora](https://github.com/pandora-analysis):

```bash
$ pyhids pandora
```

Check for known malicious files with
[MISP](https://github.com/MISP):

```bash
$ pyhids misp
```


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
