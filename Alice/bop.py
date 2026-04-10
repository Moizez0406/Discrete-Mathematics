import socket
import utils
import rsa

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("localhost", 5002))  # Bob's own port
server.listen(1)
print("Bop| Waiting for connection...")

conn, addr = server.accept()
print("Bop| Connected, sending public key...")

#p = 2861
#q = 2803
p = 100987
q = 100937
n, e, d, phi = rsa.generate_key(p, q)
print(f"Key size: {phi}")
utils.send_msg(conn, {"type": "public_key", "n": str(n), "e": str(e)})

words = []
expected_len = 0
while True:
    msg = utils.rcv_msg(conn)
    if not msg:
        break
    if msg["type"] == "done":
        break
    elif msg["type"] == "ciphertext":
        c = int(msg["c"])
        m = pow(c, d, n)
        print(f"[Bob] Decrypted: '{rsa.int2string(m)}'")
    elif msg["type"] == "words":
        expected_len = int(msg["len"])
        words = []
    elif msg["type"] == "cipherword":
        c = int(msg["c"])
        words.append(c)
        if len(words) == expected_len:
            result = rsa.decryptLargeMessage(words, d, n)
            print(f"[Bob] Decrypted large message: '{result}'")
            words = []
            expected_len = 0
conn.close()
