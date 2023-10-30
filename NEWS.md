# pyHIDS project news


### 0.9.4 (2023-10-30)

#### Changes

- [MISP lookup] The SHA1 values are now submitted in a single query;
- [MISP lookup] A new argument lets the user specify if the final output must
  be returned as a list of PyMISP Objects instead of the plain json output;
- [MISP lookup] Added possibility to specify the return format (json, stix2, csv, etc.);
- [core] Errors are always displayed, even in non-verbose mode.


### 0.9.3 (2023-10-14)

#### Changes

- improved files handling and exit codes;
- improved checks on the loaded database;
- route errors from subprocess.run() to /dev/null.


### 0.9.2 (2023-10-13)

#### Fix

Fixed an issue related to the function responsible of returning the version of
the software.


### 0.9.1 (2023-10-13)

#### Changes

- various improvements to the command line;
- new argument in order to specify if the output must be more verbose;
- new argument in order to display the version of the software;
- improved the creation of the default folders (for the YARA rules, Bloom
  filter and Cuckoo filter).


### 0.9.0 (2023-10-10)

#### New

It is now possible to export the database of pyHIDS in a Bloom or a
Cuckoo filter.

#### Changes

Various improvements and minor fixes.


### 0.8.0 (2023-10-06)

#### New

YARA can now be used in order to look for malicious files in the database
of pyHIDS.


### 0.7.1 (2023-10-05)

Small fixes and improvements.


### 0.7.0 (2023-10-04)

#### New

A MISP server can be queried in order to find potentially malicious files
from the checksums in the database of pyHIDS.



### 0.5.3 (2023-07-19)

### New

Generating a RSA signature and verifying the integrity of the database
is now optional: you can use an other tool.

#### Changes

Major improvements to the arguments parser.
