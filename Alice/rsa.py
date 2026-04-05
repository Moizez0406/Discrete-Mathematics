# S1: key generation
# P * Q = N
# Calculate phi(N) = (P-1)*(Q-1)
# Choose an e for 1 < e < phi(N) and gcd(e, phi(N)) = 1
# Which is e * d = k * phi(N) + 1 
# Pub = (N, e) & Priv = (d) 
# == == == == == == == == == == == == == == 
# Global variables
# k = 2
def gcd(e, phi):
    while phi:
        e, phi = phi, e%phi
    return e
def modinv(e, phi):
    old_r, r = e, phi
    old_s, s = 1, 0
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    return old_s % phi
def generate_key(p, q):
    n = p * q
    phi = (p-1)*(q-1)
    for i in range(3, phi): #if started from 2 e will almost always be 2
        e = i;
        if gcd(e, phi) == 1:
            break
    d = modinv(e, phi)
    return n, e, d, phi

# S2: Enryption
def string2int(msg):
    return int.from_bytes(msg.encode('utf-8'), byteorder='big') 
def int2string(n):
    return n.to_bytes((n.bit_length()+7)//8, byteorder='big').decode('utf-8')

# EXAMPLE
# msg = 'Alo'
# m = string2int(msg) 
# c = pow(m, e, n)
# assert m < n, f"Message too large! m={m}, n={n}"
# print(f"Message c = {c}")
# 
# decripted = pow(c, d, n)
# print(f"Decripted m ={int2string(decripted)}")
