# coding=utf-8

# base code borrowed from https://github.com/chrisvoncsefalvay/diffiehellman
# modified to support DH group 2 and short keys (128 bits)

#
# The MIT License (MIT)
#
# Copyright (c) 2016 Chris von Csefalvay
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#




"""
diffiehellmann declares the main key exchange class.
"""

__version__ = '0.13.4'

from hashlib import sha256

from dh.decorators import requires_private_key
from dh.exceptions import MalformedPublicKey, RNGError
from dh.primes import PRIMES

try:
    from ssl import RAND_bytes
    rng = RAND_bytes
except(AttributeError, ImportError):
    raise RNGError


class DiffieHellman:
    """
    Implements the Diffie-Hellman key exchange protocol.

    """

    def __init__(self,
                 group=2,
                 key_length=256):

        self.key_length = max(100, key_length)
        self.generator = PRIMES[group]["generator"]
        self.prime = PRIMES[group]["prime"]

    def generate_private_key(self):
        """
        Generates a private key of key_length bits and attaches it to the object as the __private_key variable.

        :return: void
        :rtype: void
        """
        key_length = self.key_length // 8 + 8
        key = 0

        try:
            key = int.from_bytes(rng(key_length), byteorder='big')
        except:
            key = int(hex(rng(key_length)), base=16)

        self.__private_key = key

    def verify_public_key(self, other_public_key):
        return self.prime - 1 > other_public_key > 2 and pow(other_public_key, (self.prime - 1) // 2, self.prime) == 1

    @requires_private_key
    def generate_public_key(self):
        """
        Generates public key.

        :return: void
        :rtype: void
        """
        self.public_key = pow(self.generator,
                              self.__private_key,
                              self.prime)
        self.public_key_bytes = self.public_key.to_bytes(self.prime.bit_length() // 8, byteorder='big')

    @requires_private_key
    def generate_shared_secret(self, other_public_key):
        """
        Generates shared secret from the other party's public key.

        :param other_public_key: Other party's public key
        :type other_public_key: int
        :return: void
        :rtype: void
        """
        if self.verify_public_key(other_public_key) is False:
            raise MalformedPublicKey

        self.shared_secret = pow(other_public_key,
                                 self.__private_key,
                                 self.prime)

        length = self.shared_secret.bit_length() // 8
        if(self.shared_secret.bit_length() % 8 != 0):
            length += 1
        shared_secret_as_bytes = self.shared_secret.to_bytes(length, byteorder='big')
        if(len(shared_secret_as_bytes) < self.prime.bit_length() // 8):
            shared_secret_as_bytes = shared_secret_as_bytes.ljust(self.prime.bit_length() // 8, b"\x00")
        self.shared_secret_bytes = shared_secret_as_bytes
       