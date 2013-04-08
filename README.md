pyHIDS
======

Presentation
------------
[pyHIDS](https://bitbucket.org/cedricbonhomme/pyhids) is a simple
[HIDS](http://en.wikipedia.org/wiki/Host-based_intrusion_detection_system)
(host-based intrusion detection system) for verifying the integrity of a system.
It uses an RSA signature to check the integrity of its database.
Alerts are written in the logs of the system and can be sent via email
to a list of users. You can define rules to specify files to be checked periodically.

Tested with Python 3.2 and Python 3.3.1.

Features
--------
* checks the integrity of system's files with a list of rules;
* checks the output of commands (*iptables*, ...);
* uses an RSA signature to check the integrity of its database;
* alerts are written in the logs of the system;
* alerts can be sent via email to a list of users.

Requirement
-----------

pyHIDS only requires the [Pure-Python RSA implementation](http://pypi.python.org/pypi/rsa).

    $ sudo pip install rsa

Configuration
-------------
The configuration is really easy. First get pyHIDS source code and copy the sample configuration file:

    $ hg clone https://bitbucket.org/cedricbonhomme/pyhids
    $ cd pyhids/
    $ cp ./conf.cfg-sample ./conf.cfg

Then edit the file **conf.cfg**:

    [globals]
    nb_bits = 752
    [email]
    enabled = 0
    mail_from = pyHIDS@no-reply.com
    mail_to = you_address
    smtp = SMTP_server
    username = your_username
    password = your_password

Set the value of "enabled" to 1 to activate email notification.

You can configure the number of bits of the RSA keys.


Example of use
--------------

    $ ./genKeys.py
    Generating 752 bits RSA keys ...
    Dumping Keys
    Done.

    $ ./genBase.py
    Generating database...
    543 files in the database.

    $ ./pyHIDS.py

Modify a character in the file  **/etc/httpd/conf/httpd.conf** and relaunch the program:

    $ ./pyHIDS.py
    [01/03/13 15:05:31] [warning] /etc/httpd/conf/httpd.conf has changed.

The program warns that the file has changed. When this happens, a warning is generated
in the logs **/var/log/syslog** and a mail is sent to the administrator.
If no change is detected only the log file is updated.

Automatic execution
-------------------
Use the time-based job scheduler, Cron, in order to schedule system scans. In your shell enter the command:

    $ crontab -e

And add the following line to check the integrity of the system every fifty minutes:

    */50 * * * * python /home/username/pyhids/pyHIDS.py

After each system check pyHIDS sends an email to the administrators.
In the case of an attacker who has deleted the cron line, for example.

Donation
--------
If you wish and if you like pyHIDS, you can donate via bitcoin. My bitcoin address: 1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ
Thank you!


License
-------
[pyHIDS](https://bitbucket.org/cedricbonhomme/pyhids/) is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt) license.


Contact
-------
[My home page](http://cedricbonhomme.org/).
