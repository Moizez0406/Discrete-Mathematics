import socket, json


def send_msg(sock, data: dict):
    line = json.dumps(data) + "\n"
    sock.sendall(line.encode())


def rcv_msg(sock) -> dict:
    buf = b""
    while not buf.endswith(b"\n"):
        chunk = sock.recv(4060)
        if not chunk:
            break
        buf += chunk
    return json.loads(buf.decode())
