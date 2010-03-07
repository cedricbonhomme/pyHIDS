#! /usr/local/bin/python
#-*- coding: utf-8 -*-

"""Generates RSA public/private keys

Used for the encryption/decrytion of the base file.
"""

"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010 Cedric Bonhomme

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

pyHIDS Copyright (C) 2010 Cedric Bonhomme
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Cedric Bonhomme"
__date__ = "$Date: 2010/03/06 $"
__copyright__ = "Copyright (c) 2010 Cedric Bonhomme"
__license__ = "GPL v3"


import pickle

from rsa import rsa
import conf # variables used by the program

NB_BITS = 256
# stronger RSA keys implies lower performance :-(

print(("Generating", NB_BITS, "bits RSA keys ..."))
key = rsa.RSA(nb_bits = NB_BITS)
pub, priv = (key.b, key.n), (key.a, key.n)

cle_pub = open(conf.pub_key_location, "wb")
cle_priv = open(conf.priv_key_location, "wb")

print("Dumping Keys")
pickle.dump(pub, cle_pub)
pickle.dump(priv, cle_priv)

cle_pub.close()
cle_priv.close()

print("Done.")