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
    #e = 65537
    for i in range(3, phi): 
        e = i;
        if gcd(e, phi) == 1:
            break
    d = modinv(e, phi)
    return n, e, d, phi

def string2int(msg):
    return int.from_bytes(msg.encode('utf-8'), byteorder='big') 
def int2string(n):
    return n.to_bytes((n.bit_length()+7)//8, byteorder='big').decode('utf-8')

def encryptLargeMessage(fat_message,e, n):
    msg_bytes = fat_message.encode('utf-8')
    words= []
    max_word_bytes = (n.bit_length() - 1) // 8 - 1
    for i in range(0, len(msg_bytes), max_word_bytes):
        word = msg_bytes[i:i + max_word_bytes]
        if len(word) < max_word_bytes:
            word = word.ljust(max_word_bytes, b'\x00')
        m = int.from_bytes(word, byteorder='big')
        c = pow(m, e, n)
        words.append(c)
    return words
def decryptLargeMessage(words, d, n):
    max_word_bytes = (n.bit_length() - 1) // 8 - 1
    msg_bytes = b''

    for c in words:
        m = pow(c, d, n)
        word_bytes = m.to_bytes(max_word_bytes, byteorder='big')
        msg_bytes += word_bytes

    return msg_bytes.rstrip(b'\x00').decode('utf-8')
# msg = 'Alo'
# m = string2int(msg) 
# c = pow(m, e, n)
# assert m < n, f"Message too large! m={m}, n={n}"
# print(f"Message c = {c}")
# 
# decripted = pow(c, d, n)
# print(f"Decripted m ={int2string(decripted)}")
