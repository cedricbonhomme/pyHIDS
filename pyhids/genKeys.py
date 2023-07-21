#! /usr/bin/env python

"""Generates RSA public/private keys

Used for the encryption/decrytion of the base file.
"""

"""
pyHIDS. Python HIDS. Security software.
pyHIDS verify the integrity of your system.
Copyright (C) 2010-2023 Cedric Bonhomme

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

pyHIDS Copyright (C) 2010-2023 Cedric Bonhomme
This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
This is free software, and you are welcome to redistribute it
under certain conditions; type `show c' for details.
"""

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2010/03/06 $"
__revision__ = "$Date: 2013/02/16 $"
__copyright__ = "Copyright (c) 2010-2023 Cedric Bonhomme"
__license__ = "GPL v3"

import pickle

import rsa

import conf


def main(nb_bits=1024):
    print("Generating", nb_bits, "bits RSA keys ...")
    pub, priv = rsa.newkeys(nb_bits)

    public_key = open(conf.PUBLIC_KEY, "wb")
    private_key = open(conf.PRIVATE_KEY, "wb")

    print("Dumping Keys")
    pickle.dump(pub, public_key)
    pickle.dump(priv, private_key)

    public_key.close()
    public_key.close()

    print("Done.")


if __name__ == "__main__":
    main()
