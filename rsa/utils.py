#! /usr/local/bin/python
#-*- coding: utf-8 -*-

"""Some usefull functions.
"""

import math
import types
import random
import operator

def gcd_bezout(x, y):  # a > b > 0
    """
    Extended great common divisor, returns x , y
    and gcd(a,b) so ax + by = gcd(a,b)
    """
    if x % y == 0:
        return (0, 1, y)
    q = []
    while x % y != 0:
        q.append(-1*(x//y))
        (x, y)=(y, x%y)
    (x, y, gcd) = (1, q.pop(), y)
    while q:
        (x,y) = (y, y*q.pop()+x)
    return (gcd, x, y)

def gcd(x,y):
    """Return GCD of x and y."""
    while y:
        (x, y) = (y, x%y)
    return abs(x)

def premier(a, b):
    """Return True if a and b are coprime.
    """
    return gcd(a, b) == 1

def log(x, base = 10):
    """Return neperian logarithm of 'x'."""
    return math.log(x) / math.log(base)

def miller_rabin_pass(a, n):
    d = n - 1
    s = 0
    while d & 1:
        d = d >> 1
        s = s + 1

    a_to_power = expo_modulaire_rapide(a, d, n)
    if a_to_power == 1:
        return True
    for i in range(s-1):
        if a_to_power == n - 1:
            return True
        a_to_power = (a_to_power * a_to_power) % n
    return a_to_power == n - 1

def miller_rabin(n):
    for repeat in range(20):
        a = 0
        while a == 0:
            a = random.randrange(n)
        if not miller_rabin_pass(a, n):
            return False
    return True

def expo_modulaire_rapide(a, p ,n):
    """Calcul l'exposant modulaire (pow()).

    Selon Wikipédia (http://fr.wikipedia.org/wiki/Exponentiation_modulaire)
    """
    result = a % n
    remainders = []
    while p != 1:
        remainders.append(p & 1)
        p = p >> 1
    while remainders:
        rem = remainders.pop()
        result = ((a ** rem) * result ** 2) % n
    return result

def inv_modulo(a,m):
    """Retourne l'inverse modulaire de a modulo m.
    """
    (d, x, _) = gcd_bezout(a, m)
    if d == 1:
        return x % m
    return None

def bytes2int(bytes):
    """
    >>> (128*256 + 64)*256 + + 15
    8405007
    >>> l = [128, 64, 15]
    >>> bytes2int(l)
    8405007
    """
    # Convert byte stream to integer
    integer = 0
    for byte in bytes:
        integer <<= 8 #integer *= 256
        byte = ord(byte)
        integer += byte

    return integer

def int2bytes(number):
    """
    >>> bytes2int(int2bytes(123456789))
    123456789
    """
    string = ""

    while number > 0:
        string = "%s%s" % (chr(number & 0xFF), string)
        number >>= 8 #integer /= 256

    return string

if __name__ == '__main__':
    # Point of entry in execution mode.
    pass