from collections import namedtuple
import pickle

MessageTuple = namedtuple('MessageTuple', ['n','a','b','c'])
  

# https://koclab.cs.ucsb.edu/teaching/cren/project/2017/chennagiri.pdf

msg = pickle.load(open('msg.pickle'))

n, a, b, c = map(list, zip(*msg))

ii = [[1,0,0],[0,1,0],[0,0,1]]

t = [crt(i, n) for i in ii]

G.<x> = PolynomialRing(Zmod(prod(n)))

gi = [t[i]*( (a[i]*x+b[i])**3 - c[i] ) for i in range(3)]

g = sum(gi).monic()

m = int(g.small_roots()[0])

print ''
print hex(m)[2:-1].decode('hex')
print ''

