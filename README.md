pyHIDS
======

Presentation
------------
pyHIDS is a little [HIDS](http://en.wikipedia.org/wiki/Host-based_intrusion_detection_system)
(written for my personal needs) for verifying the integrity of a system.




Configuration
-------------
The configuration is very easy. 


    pyhids_location = "/home/cedric/python/pyhids/"

    # address of the log file :
    log_location = pyhids_location + "log"
    # address of the saved base of hash values :
    base_location = pyhids_location + "base"

    # address of the private key
    # (used only by genBase.py to crypt the base of hash values) :
    priv_key_location = pyhids_location + "cle_priv"
    # address of the public key (used to decrypt the base of hash values) :
    pub_key_location = pyhids_location + "cle_pub"

    # mail of admins
    admin_mail = ["yourmail@mail.com"]
    # mail of the sender
    sender = "sendermail@mail.com"

    # specific files to scan :
    specific_files_to_scan = [ \
            pyhids_location + "pyHIDS.py",
            pyhids_location + "conf.py",
            pyhids_location + "rsa/__init__.py",
            #pyhids_location + "genBase.py", (genBase.py should not stay on the computer)
            "/etc/cron.hourly/pyHIDS", \
            "/boot/grub/menu.lst", \
            "/etc/shadow", \
            "/etc/crontab", \
            "/etc/networks"]

    # rules to scan folders :
    folder_rules = [ \
        ("conf", "/etc")]
    # used by search_files() in genBase.py



RSA keys and base generation
----------------------------
You can configure the number of bits of the RSA keys. By default the number is 256 for performance reasons.
That said, a 256-bit encryption for this application is sufficient.


Email alerts
------------
To receive email alerts, it just need to fill the list **admin_mail** in the file **conf.py**.
This list contains people to prevent when a file has been modified. It must also configure the sender.
If you do not want to receive email alerts, simply leave the list empty.


=== General configuration ===

    * address of pyHIDS on your system: **pyhids_location**.


=== So, you just have to configure ===
* the address of pyHIDS on your system;
* email(s) for alerts;
* if needed: folder_rules.

== Test ==
To test the program, enter the commands:

    python genKeys.py
    python genBase.py
    python pyHIDS.py


=== Example ===

    [cedric@localhost pyhids]$ python3.1 genKeys.py
    Generating 256 bits RSA keys ...
    Dumping Keys
    Done.

    [cedric@localhost pyhids]$ python3.1 genBase.py
    Loading public key
    Generating data base...
    552 files in the base

    [cedric@localhost pyhids]$ python3.1 pyHIDS.py
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

    [cedric@localhost pyhids]$ python3.1 pyHIDS.py
    [07/03/10 15:05:13] HIDS starting.
    .
    .
    .
    [07/03/10 15:05:31] [warning] /etc/httpd/conf/httpd.conf hash has changed :
    573edeed49818cb20ff1efd4f8ce7d6db7e6e28fe831f8d60de40b6298b8d555!=33027d530eeebc9d5355855016b3543a8bf2000c4986bb0eb8aa8e244a827e8a
    [07/03/10 15:05:31] [notice] /etc/gconf/gconf.xml.defaults/%gconf-tree-yo.xml ok
    .
    .
    .
    [07/03/10 15:05:35] [notice] /etc/gconf/gconf.xml.defaults/%gconf-tree-crh.xml ok
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
[pyHIDS](https://bitbucket.org/cedricbonhomme/pyaggr3g470r/) is under [GPLv3](http://www.gnu.org/licenses/gpl-3.0.txt) license.




Contact
-------
[My home page](http://cedricbonhomme.org/).