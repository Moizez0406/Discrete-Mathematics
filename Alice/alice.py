import socket
import utils

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 5001))

msg = utils.rcv_msg(client)
n = int(msg["n"])
e = int(msg["e"])

m = 42
c = pow(m, e, n)
utils.send_msg(client, {"type": "ciphertext", "c": str(c)})
client.close()
