import socket
import utils
import rsa
import math
import time

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception("No modular inverse")
    return x % m

def factor_trial_division(n):
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i, n // i
    return None, None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5003))

public_key = utils.rcv_msg(client)
n = int(public_key["n"])
e = int(public_key["e"])

print(f"Eve| Intercepted public key: n={n}, e={e}")

start = time.time()
p, q = factor_trial_division(n)

if p is None:
    print("Eve| Failed to factor n")
    client.close()
    exit()

phi = (p - 1) * (q - 1)
d = mod_inverse(e, phi)
end = time.time()

print(f"Eve| Found p={p}, q={q}")
print(f"Eve| Recovered private key d={d}")
print(f"Eve| Attack time: {end - start:.6f} seconds")

while True:
    msg = utils.rcv_msg(client)
    if not msg:
        break

    print(f"Eve| Intercepted: {msg}")

    if msg["type"] == "ciphertext":
        c = int(msg["c"])
        m = pow(c, d, n)
        plaintext = rsa.int2string(m)

        print(f"Eve| Ciphertext: {c}")
        print(f"Eve| Decrypted message: {plaintext}")

client.close()
