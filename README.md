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

Tested with Python 3.2.


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
    Loading public key
    Generating data base...
    552 files in the base

    $ ./pyHIDS.py
    [07/03/10 15:03:06] HIDS starting
    .
    .
    .
    [07/03/10 15:03:08] [notice] /etc/X11/xorg.conf.mdv1229453811 ok
    [07/03/10 15:03:08] [notice] /etc/fonts/conf.d/20-mdv-disable-antialias.conf ok
    [07/03/10 15:03:08] [notice] /etc/makedev.d/cdrom.conf ok
    [07/03/10 15:03:08] [notice] /etc/X11/xorg.conf.mdv1228503577 ok
    [07/03/10 15:03:08] [notice] /etc/X11/xorg.conf.mdv1227813978 ok
    [07/03/10 15:03:08] [notice] /etc/depmod.d/dkms.conf
    .
    .
    .
    [07/03/10 15:03:18] [notice] /etc/fonts/conf.avail/70-yes-bitmaps.conf ok
    [07/03/10 15:03:18] Error(s) : 0
    [07/03/10 15:03:18] Warning(s) : 0
    [07/03/10 15:03:18] HIDS finished


Modify a character in the file  **/etc/httpd/conf/httpd.conf** and relaunch the program:

    $ ./pyHIDS.py
    [07/03/10 15:05:13] HIDS starting.
    [07/03/10 15:05:31] [warning] /etc/httpd/conf/httpd.conf hash has changed :
    573edeed49818cb20ff1efd4f8ce7d6db7e6e28fe831f8d60de40b6298b8d555!=33027d530eeebc9d5355855016b3543a8bf2000c4986bb0eb8aa8e244a827e8a
    [07/03/10 15:05:36] Error(s) : 0
    [07/03/10 15:05:36] Warning(s) : 1
    [07/03/10 15:05:36] HIDS finished.



The program warns that the hash has changed. When this happens, a warning is generated
in the logs **/var/log/syslog** and a mail is sent to the administrator.
If no change is detected only the log file is updated.


Donnation
---------
If you wish and if you like pyHIDS, you can donate via bitcoin. My bitcoin address: 1GVmhR9fbBeEh7rP1qNq76jWArDdDQ3otZ
Thank you!


License
-------
[pyHIDS](https://bitbucket.org/cedricbonhomme/pyhids/) is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt) license.


Contact
-------
[My home page](http://cedricbonhomme.org/).
