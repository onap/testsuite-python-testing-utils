import socket, ssl
from robot.api.deco import keyword


class SocketKeywords(object):
    """SocketKeywords are common resource for simple socket keywords."""

    def __init__(self):
        super(SocketKeywords, self).__init__()

    @keyword
    def send_binary_data(self, host, port, data):
        """ send raw bytes over tcp socket"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        sock.connect((host, int(port)))
        sock.sendall(bytes(data))
        sock.close()

    @keyword
    def send_binary_data_over_ssl(self, host, port, ca, cert, key, data):
        """ send raw bytes over tcp ssl socket """
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(str(ca))
        context.load_cert_chain(str(cert), str(key))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ssock = context.wrap_socket(sock, server_hostname=str(host))
        ssock.connect((str(host), int(port)))
        ssock.sendall(bytes(data))
        ssock.close()
