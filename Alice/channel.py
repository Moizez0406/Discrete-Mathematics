import socket
import utils

# ALICE's SERVER
alice_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
alice_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
alice_server.bind(("localhost", 5001))
alice_server.listen(1)
# EVEs' SERVER
eve_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
eve_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
eve_server.bind(("localhost", 5003))
eve_server.listen(1)

# BOP
bob_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bob_conn.connect(("localhost", 5002))
print("SERVER| Connected to Bop")

# Wait for Alice
print("SERVER| Waiting for Alice...")
alice_conn, _ = alice_server.accept()
eve_conn, _ = eve_server.accept()
print("SERVER| Alice connected")

msg = utils.rcv_msg(bob_conn)  # Bob → Alice (public key)
utils.send_msg(alice_conn, msg)
print(f"[Eve intercepts] {msg}")
utils.send_msg(eve_conn, msg) # Eve save msg
while True:
    msg = utils.rcv_msg(alice_conn)  # Alice → Bob
    if not msg:
        break
    utils.send_msg(eve_conn, msg) # Eve save msg
    print(f"[Eve intercepts] {msg}")
    utils.send_msg(bob_conn, msg)
