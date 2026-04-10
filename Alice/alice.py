import socket
import utils
import rsa
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))

bob_msg = utils.rcv_msg(client)
n = int(bob_msg["n"])
e = int(bob_msg["e"])
while True:
    #msg = input("Enter message: ")
    messages = ['A','Al', 'Alo','Hi!', 'Bop', 'Eve', 'is','bad']
    for msg in messages:
        print(f"Alice| Sent message...({msg} size: {rsa.string2int(msg)})")
        if not msg:
            break
        m = rsa.string2int(msg)
        assert m < n, f"Message too large for key size"
        c = pow(m, e, n)
        utils.send_msg(client, {"type": "ciphertext", "c": str(c)})
        time.sleep(1)
client.close()
