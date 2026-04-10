import socket
import utils
import rsa
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))

bob_msg = utils.rcv_msg(client)
n = int(bob_msg["n"])
e = int(bob_msg["e"])
print(f"Alice| Connected to Bob. Public key: n={n}, e={e}")
print("Alice| Type your messages (or 'quit' to exit, 'large:' for large message)")
print("-" * 50)
messages = ['Hi!', 'Bop']
fat_message = 'I hope Eve is not hearing'

while True:
    msg = input("Enter message: ")

    if not msg or msg.lower() == 'quit':
        print("Alice| Sending quit signal...")
        utils.send_msg(client, {"type": "done"})
        time.sleep(1)
        break
    if msg.startswith('large:'):
        fat_message = msg[6:]
        print(f"Alice| Sending large message: {fat_message}")
        words = rsa.encryptLargeMessage(fat_message, e, n)
        utils.send_msg(client, {"type": "words", "len": len(words)})
        for w in words:
            utils.send_msg(client, {"type": "cipherword", "c": str(w)})
            time.sleep(1)
    else:
        try:
            m = rsa.string2int(msg)
            if m >= n:
                print(f"Alice| Message too large for key size! Use 'large:'")
                continue
            c = pow(m, e, n)
            utils.send_msg(client, {"type": "ciphertext", "c": str(c)})
            print(f"Alice| Sent: '{msg}'")
        except Exception as e:
            print(f"Alice| Error: {e}")
    #print(f"Alice| Sent message...({fat_message})")
    #words = rsa.encryptLargeMessage(fat_message,e, n)
    #utils.send_msg(client, {"type":"words", "len":len(words)})
    #for w in words:
    #    utils.send_msg(client, {"type":"cipherword", "c":str(w)})
    #    time.sleep(1)
    #utils.send_msg(client, {"type": "done"})
    #:words time.sleep(1)
client.close()
