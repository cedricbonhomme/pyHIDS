pyHIDS
======

Presentation
------------
pyHIDS is a little [HIDS](http://en.wikipedia.org/wiki/Host-based_intrusion_detection_system)
(written for my personal needs) for verifying the integrity of a system.

Tested with Python 3.2.


Configuration
-------------
The configuration is very easy. First copy the sample configuration file:

    $ cp ./conf.cfg-sample ./conf.cfg

And edit the file **conf.cfg**:

    [globals]
    nb_bits = 752
    [email]
    enabled = 0
    mail_from = pyHIDS@no-reply.com
    mail_to = you_address
    smtp = SMTP_server
    username = your_username
    password = your_password


RSA keys and base generation

You can configure the number of bits of the RSA keys. By default the number is 752 for performance reasons.


Email alerts

To receive email alerts, it just need to set some variable in the **email**
section of the file **conf.cfg**.
If you do not want to receive email alerts, simply set **enabled** to **0**.


Test
----
To test the program, enter the commands:

    $ ./genKeys.py
    $ ./genBase.py
    $ ./pyHIDS.py


Example
-------

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
