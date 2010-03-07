#! /usr/bin/python
#-*- coding: utf-8 -*-

import sys
import math
import zlib
import random
import base64
import hashlib

from pickle import dumps, loads

from rsa import utils


class RSA(object):
    """
    RSA public-key encryption.
    """
    def __init__(self, p = None, q = None, b = None, nb_bits = 256):
        """Initialization of keys.

        Generates 'p' and 'q' prime numbers randomly.
        Computes a, b and n thanks to phi.
        """
        if p == None and q == None and b == None:
            p = random.getrandbits(nb_bits)
            q = random.getrandbits(nb_bits)
            while not utils.miller_rabin(p):
                p = random.getrandbits(nb_bits)
            while not utils.miller_rabin(q):
                q = random.getrandbits(nb_bits)
        n   = p * q
        phi = (p - 1) * (q - 1)
        if b == None:
            while True:
                b = random.randint(2, phi - 1)
                if utils.premier(b, phi):
                    break
        a  = utils.inv_modulo(b, phi)
        self.a = a
        self.b = b
        self.n = n

    def encrypt_int(self, x):
        """Encrypts the message."""
        return utils.expo_modulaire_rapide(x, self.b, self.n)

    def decrypt_int(self, y):
        """Decrypts the message."""
        return utils.expo_modulaire_rapide(y, self.a, self.n)

    def encrypt_text(self, message):
        """Encrypts a string 'message' with the public key"""
        return self.chopstring(message, self.encrypt_int)

    def decrypt_text(self, cypher):
        """Decrypts a cypher with the private key"""
        return self.gluechops(cypher, self.decrypt_int)

    def chopstring(self, message, funcref):
        """Cut 'message' in blocs.

        Used by encrypt_text.
        """
        msglen = len(message)
        mbits = msglen * 8
        nbits = int(math.floor(utils.log(self.n, 2)))
        nbytes = int(nbits / 8)
        blocks = int(msglen / nbytes)

        if msglen % nbytes > 0:
            blocks += 1

        cypher = []

        for bindex in range(blocks):
            offset = bindex * nbytes
            block = message[offset:offset+nbytes]
            value = utils.bytes2int(block)
            cypher.append(funcref(value))

        return self.picklechops(cypher)

    def gluechops(self, chops, funcref):
        """Reconstructs blocs into string.

        Used by decryt_text.
        """
        message = ""

        chops = self.unpicklechops(chops)

        for cpart in chops:
            mpart = funcref(cpart)
            message += utils.int2bytes(mpart)

        return message

    def picklechops(self, chops):
        """Serializes and transforms 'chops' in base 64."""
        value = zlib.compress(dumps(chops))
        encoded = base64.encodestring(value)
        return encoded.strip()

    def unpicklechops(self, string):
        """Deserializes 'string'."""
        return loads(zlib.decompress(base64.decodestring(string)))

    def __str__(self):
        """Pretty print of keys."""
        return """\
            Private key : %s
            Public key : %s
            Modulo: %s""" % (self.a, self.b, self.n)


if __name__ == '__main__':
    # Point of entry in execution mode
    rsa = RSA(nb_bits = 128)
    print(rsa)
    cr = rsa.encrypt_text("Bonjour, comment allez-vous ?\nJe vais très bien, merci.")
    dcr = rsa.decrypt_text(cr)
    print()
    print("Cipher text :")
    print(cr)
    print()
    print("Plain text :")
    print(dcr)