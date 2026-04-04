import socket
import utils

# ALICE's SERVER
alice_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
alice_server.bind(("localhost", 5001))
alice_server.listen(1)

# BOP
bob_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_conn.connect(("localhost", 5002))
print("SERVER| Connected to Bop")

# Wait for Alice
print("SERVER| Waiting for Alice...")
alice_conn, _ = alice_server.accept()
print("SERVER| Alice connected")

# Forward everything in both directions, Eve reads along
while True:
    msg = utils.rcv_msg(bob_conn)  # Bob → Alice (public key)
    if not msg:
        break
    print(f"[Eve intercepts] {msg}")
    utils.send_msg(alice_conn, msg)

    msg = utils.rcv_msg(alice_conn)  # Alice → Bob
    if not msg:
        break
    print(f"[Eve intercepts] {msg}")
    utils.send_msg(bob_conn, msg)
