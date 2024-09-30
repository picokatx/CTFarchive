from Crypto.Util.number import inverse
p, q = 17, 101
N = p*q
phi = (p-1)*(q-1)
E = 3
D = inverse(E, phi)

