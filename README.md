## pyHIDS

### Presentation

[pyHIDS](https://github.com/cedricbonhomme/pyHIDS) is a
[HIDS](https://en.wikipedia.org/wiki/Host-based_intrusion_detection_system)
(host-based intrusion detection system) for verifying the integrity of a system.

It is recommended to use Python >= 3.11.


### Features

* checks the integrity of system's files with a list of rules;
* checks the output of commands (*iptables*, ...);
* possibity to use RSA to sign to check the integrity of its database;
* alerts are written in the logs of the system;
* alerts can be sent via email to a list of users;
* alerts can be sent on IRC channels through the
  [irker](https://gitlab.com/esr/irker) IRC client (which should be running as
  a daemon);
* verify files with [Hashlookup](https://github.com/hashlookup),
  [Pandora](https://github.com/pandora-analysis),
  [MISP](https://github.com/MISP) and
  [YARA](https://github.com/virustotal/yara);
* possibility to export the database in a Bloom or a Cuckoo filter.

You can define rules to specify files to be checked.


### Installation

You can use [pipx](https://pypa.github.io/pipx/).

```bash
$ pipx install pyHIDS
$ export PYHIDS_CONFIG=~/.pyHIDS/conf.cfg
```

[An example](./conf.cfg-sample) of configuration file is available.
With this file you can configure:

- the integration with Hashlookup, Pandora, MISP and YARA;
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
[12/10/23 21:35:26] Error(s) : 0
[12/10/23 21:35:26] Warning(s) : 0
[12/10/23 21:35:26] HIDS finished.
```

You can skip the first step (generation of the keys) if you do not want to
sign the database with the solution provided with pyHIDS (RSA) or if you
do not want to sign the database.

Change a monitored file and relaunch the program:

```bash
$ pyhids run
Verifying the integrity of the files...
[12/10/23 14:41:51] [warning] /bin/cifsdd changed.
```

The program warns that the file has changed. When this happens, a warning is
generated in the logs of the system and an email is sent to the
administrator. If no change is detected, only the log file is updated.

Log file generated:

```bash
$ tail var/log
[09/10/23 14:41:51] [notice] /bin/cifscreds ok
[09/10/23 14:41:51] [notice] /bin/mbim-network ok
[09/10/23 14:41:51] [notice] /bin/xclip ok
[09/10/23 14:41:51] [notice] /bin/preparetips5 ok
[09/10/23 14:41:51] [notice] /bin/pamperspective ok
[12/10/23 14:41:51] [warning] /bin/cifsdd changed.
[09/10/23 14:41:51] [notice] /bin/pod2usage ok
[09/10/23 14:41:51] [notice] /bin/mkzftree ok
[09/10/23 14:41:51] Error(s) : 0
[09/10/23 14:41:51] Warning(s) : 1
[09/10/23 14:41:51] HIDS finished.
```

If you want to see the logs in ``syslog`` you have different options
depending on your system:

```bash
$ journalctl --follow
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /etc/resolv.conf changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/mdsearch changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/smbcacls changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/smbspool changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/smbclient changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/smbcquotas changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/smbget changed.
Oct 12 22:58:47 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/nmblookup changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:47] [warning] /bin/rpcclient changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/smbpasswd changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/dbwrap_tool changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/cifsdd changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/net changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/samba-regedit changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/testparm changed.
Oct 12 22:58:48 debian pyhids[98135]: pyHIDS - [12/10/23 22:58:48] [warning] /bin/smbtree changed.
```

```bash
$ journalctl --since="1 minute ago"
```

```bash
$ tail -f /var/log/syslog
```


### Other features

#### Checks with external tools

Check for known malicious files with Hashlookup, Pandora, MISP or YARA.

```bash
$ pyhids hashlookup
$ pyhids pandora
$ pyhids misp
$ pyhids yara
```

#### Export functions

```bash
$ pyhids export --bloom-filter
Bloom filter generated and stored: var/bloom/bloomfilter.bf
```

```bash
$ pyhids export --cuckoo-filter
Cuckoo filter generated and stored: var/cuckoo/cuckoofilter.cf
```


### Automatic execution

Use the time-based job scheduler, Cron, in order to schedule system scans.
In your shell enter the command:

```bash
$ crontab -e
```

Add the following line to check the integrity of the system every fifty
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
