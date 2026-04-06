import socket
import utils
import rsa
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5003))

public_key = utils.rcv_msg(client)
n = int(public_key["n"])
e = int(public_key["e"])
print(f"Eve| reads: n={n}, e={e}")

while True:
    msg = utils.rcv_msg(client)
    if not msg:
        breake
    print(f"Eve| reads from Alice: {msg}")
    # Implemet logic for decryption
client.close()
