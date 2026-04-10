import socket
import utils
import rsa
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))

bob_msg = utils.rcv_msg(client)
n = int(bob_msg["n"])
e = int(bob_msg["e"])
    #while True:
    #msg = input("Enter message: ")
messages = ['Hi!', 'Bop']
fat_message = 'I hope Eve is not hearing'
for msg in messages:
    print(f"Alice| Sent message...({msg} size: {rsa.string2int(msg)})")
    if not msg:
        break
    m = rsa.string2int(msg)
    assert m < n, f"Message too large for key size"
    c = pow(m, e, n)
    utils.send_msg(client, {"type":"ciphertext", "c":str(c)})
    time.sleep(1)

print(f"Alice| Sent message...({fat_message})")
words = rsa.encryptLargeMessage(fat_message,e, n)
utils.send_msg(client, {"type":"words", "len":len(words)})
for w in words:
    utils.send_msg(client, {"type":"cipherword", "c":str(w)})
    time.sleep(1)
utils.send_msg(client, {"type": "done"})
time.sleep(1)
client.close()
