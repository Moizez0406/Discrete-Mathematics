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

def decrypt_large_message(words, d, n):
    msg_bytes = b''
    max_word_bytes = (n.bit_length() - 1) // 8 - 1
    
    for c in words:
        m = pow(c, d, n)
        word_bytes = m.to_bytes(max_word_bytes, byteorder='big')
        msg_bytes += word_bytes
    
    return msg_bytes.rstrip(b'\x00').decode('utf-8')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5003))
print("Eve| Connected to channel")

public_key = utils.rcv_msg(client)
n = int(public_key["n"])
e = int(public_key["e"])

print(f"Eve| Intercepted public key: n={n}, e={e}")

start = time.time()
p, q = factor_trial_division(n)

if p is None:
    print("Eve| Failed to factor n")
    d = None
else:
    phi = (p - 1) * (q - 1)
    d = mod_inverse(e, phi)
    end = time.time()
    print(f"Eve| Found p={p}, q={q}")
    print(f"Eve| Recovered private key d={d}")
    print(f"Eve| Attack time: {end - start:.6f} seconds")

words = []
expected_len = 0

while True:

    try:
        msg = utils.rcv_msg(client)
        if not msg:
            print("Eve| Connection closed")
            break

        if msg["type"] == "done":
            print("Eve| Done signal received")
            break

        elif msg["type"] == "ciphertext":
            c = int(msg["c"])
            if d is not None:
                m = pow(c, d, n)
                plaintext = rsa.int2string(m)
                print(f"Eve| Intercepted: '{plaintext}'")

        elif msg["type"] == "words":
            expected_len = int(msg["len"])
            words = []
            print(f"Eve| Large message incoming ({expected_len} blocks)")

        elif msg["type"] == "cipherword":
            c = int(msg["c"])
            words.append(c)
            if len(words) == expected_len and d is not None:
                result = decrypt_large_message(words, d, n)
                print(f"Eve| Intercepted large message: '{result}'")
                words = []
                expected_len = 0

    except Exception as e:
        print(f"Eve| Error: {e}")
        break

client.close()
print("Eve| Disconnected")
