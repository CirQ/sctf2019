#!/usr/bin/python
# -*- coding: utf-8 -*-

from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from binascii import *
from FLAG import flag
from MESSAGE import message


class telecom:
    def __init__(self, name):
        self.name = name
        self.key = get_random_bytes(16)
        self.iv = get_random_bytes(16)

        self.e = 3

        p = getPrime(512)
        q = getPrime(512)
        self.fn = (p-1)*(q-1)

        while True:
            if GCD(self.e, self.fn) != 1:
                p = getPrime(512)
                q = getPrime(512)
                self.fn = (p - 1) * (q - 1)
            else:
                break

        self.d = inverse(self.e, self.fn)
        self.n = p * q

    def RSA_encrypt(self, plaintext):
        assert bytes_to_long(plaintext).bit_length() < 512

        a = getPrime(512)
        b = getPrime(512)
        m = bytes_to_long(plaintext)
        c = pow(a * m + b, self.e, self.n)


        message = 'admin:'+self.name+', your ciphertext is: c='+hex(c)+'\nwith some parameters:a='+hex(a)+', b='+hex(b)+'\n'
        return message

    def RSA_decrypt(self):
        pass

    def broadcast(self):
        message = self.name+':'+'my pub-key is: '+'e='+str(self.e)+','+'n='+hex(self.n)+'\n'
        return message

    def pad(self, msg):
        pad_length = 16 - len(msg) % 16
        return msg + chr(pad_length) * pad_length

    def unpad(self, msg):
        return msg[:-ord(msg[-1])]

    def AES_encrypt(self, message):
        message = self.pad(message)
        aes = AES.new(self.key, AES.MODE_OFB, self.iv)
        return aes.encrypt(message)


    def AES_decrypt(self, message):
        aes = AES.new(self.key, AES.MODE_OFB, self.iv)
        return self.unpad(aes.decrypt(message))


def proof_of_work():
    p = getPrime(512)
    q = getPrime(512)
    n = p*q
    e = 65537
    fn = (p-1)*(q-1)
    d = inverse(e, fn)

    print "pubkey:{e, n}={65537, %s}\n" %hex(n)
    print 'Give me something you want to encrypt:'
    sys.stdout.flush()
    m = int(raw_input())
    c = pow(m, e, n)

    if m == pow(c, d, n):
        return False
    return True


if __name__ == '__main__':

    if not proof_of_work():
        exit()

    while True:
        print 'You have the following options to do:\n[1]monitor\n[2]forge the message'
        choice = raw_input()

        if int(choice) == 1:

            Alpha = telecom('Alpha')
            Bravo = telecom('Bravo')
            Charlie = telecom('Charlie')

            print Alpha.broadcast()
            print Bravo.broadcast()
            print Charlie.broadcast()

            print Alpha.RSA_encrypt(message)
            print Bravo.RSA_encrypt(message)
            print Charlie.RSA_encrypt(message)
            print 'Alpha:David, make sure you\'ve read this:' + hexlify(Alpha.AES_encrypt(message))+'\n'
        elif int(choice) == 2:
            print 'you can send message to David now:'
            input_cipher = raw_input()
            if Alpha.AES_decrypt(unhexlify(input_cipher)) == message.replace('afternoon', 'morning'):
                print 'you made it, this reward is prepared for you:' + flag
                exit()
            else:
                print 'you failed'
                exit()
        else:
            exit()
