from collections import namedtuple
import pickle
from pwn import *

context.log_level = 'info'

MessageTuple = namedtuple('MessageTuple', ['n','a','b','c'])


def get_rsaenc(n):
    p.recvuntil('c=')
    c = int(p.recvuntil('L',True), 16)
    p.recvuntil('a=')
    a = int(p.recvuntil('L',True), 16)
    p.recvuntil('b=')
    b = int(p.recvuntil('L',True), 16)
    return MessageTuple(n, a, b, c)



def get_msg():
    p.sendlineafter('[2]forge the message\n', '1')
    p.recvuntil('n=')
    an = int(p.recvuntil('L',True), 16)
    p.recvuntil('n=')
    bn = int(p.recvuntil('L',True), 16)
    p.recvuntil('n=')
    cn = int(p.recvuntil('L',True), 16)
    amsg = get_rsaenc(an)
    bmsg = get_rsaenc(bn)
    cmsg = get_rsaenc(cn)
    p.recvuntil('this:')
    enc = unhex(p.recvline(False))
    return amsg, bmsg, cmsg, enc

def pad(msg):
    pad_length = 16 - len(msg) % 16
    return msg + chr(pad_length) * pad_length

def unpad(msg):
    return msg[:-ord(msg[-1])]


p = process(['python', 'server.py'])
p.sendlineafter('encrypt:\n', str(1<<2048))


amsg, bmsg, cmsg, _ = get_msg()
p.debug('A msg: %s', amsg)
p.debug('B msg: %s', bmsg)
p.debug('C msg: %s', cmsg)
with open('msg.pickle', 'wb') as w:
    pickle.dump([amsg, bmsg, cmsg], w)


_, _, _, enc = get_msg()
message = pad('I will send you the ticket tomorrow afternoon')
fake_message = pad('I will send you the ticket tomorrow morning')
c = xor(xor(enc, message), fake_message)


p.sendlineafter('[2]forge the message\n', '2')
p.sendline(enhex(c))

p.interactive()

