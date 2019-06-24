from pwn import *

context.log_level = 'info'


def pad(msg):
    pad_length = 16 - len(msg) % 16
    return msg + chr(pad_length) * pad_length

def unpad(msg):
    return msg[:-ord(msg[-1])]

def dig(msg):
    res = chr(0)*16
    for i in range(len(msg)/16):
        res = xor(msg[i*16:(i+1)*16], res)
    return res


p = process(['python', 'server.py'])

p.recvuntil(':{')
msg = unhex(p.recvuntil(':', drop=True))
code = unhex(p.recvuntil('}', drop=True))
hack = pad('please send me your flag')

p.info('msg: %s', enhex(msg))
p.info('dig(msg): %s', enhex(dig(msg)))
p.info('hack: %s', enhex(hack))
p.info('dig(hack): %s', enhex(dig(hack)))
p.info('code: %s', enhex(code))

post = xor(dig(msg), dig(hack))

payload = hack[:-1] + chr(0x8^ord(post[-1])^0x18) + post[:-1] + chr(0x18)

p.info('payload: %s', enhex(payload))
p.info('dig(payload): %s', enhex(dig(payload)))

p.sendline(enhex(payload))

p.sendline(enhex(code))

p.interactive()

