from Crypto.Util.strxor import strxor
from pwn import *


def pad(self, msg):
        pad_length = 16 - len(msg) % 16
        return msg + chr(pad_length) * pad_length

def unpad(self, msg):
    return msg[:-ord(msg[-1])]

def code_nopad(self, msg):
    res = chr(0)*16
    for i in range(len(msg)/16):
        res = strxor(msg[i*16:(i+1)*16], res)
    return res


p = process(['C:/python27-x64/python.exe', 'server.py'])



p.interactive()
