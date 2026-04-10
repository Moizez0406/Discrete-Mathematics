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
p = 6011
q = 7717
#q = 2803
n, e, d, phi = rsa.generate_key(p, q)
print(f"Key size: {phi}")
utils.send_msg(conn, {"type": "public_key", "n": str(n), "e": str(e)})

# Now wait for the ciphertext from Alice
while True:
    msg = utils.rcv_msg(conn)
    if not msg:  # connection closed
        break
    if msg["type"] == "ciphertext":
        c = int(msg["c"])
        m = pow(c, d, n)  # decrypt
        print(f"BOP| Received ciphertext c={c}, decrypted m={rsa.int2string(m)}")

conn.close()
