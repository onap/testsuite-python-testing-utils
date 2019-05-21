import socket


class SocketUtils:
    """SocketUtils is common resource for simple socket keywords."""

    def __init__(self):
        pass

    def send_binary_data(self, host, port, data):
        """ send raw bytes over tcp socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        sock.connect((host, int(port)))
        sock.sendall(bytes(data))
