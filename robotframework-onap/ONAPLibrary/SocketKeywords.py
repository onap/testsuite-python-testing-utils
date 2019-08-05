import socket, ssl
from robot.api.deco import keyword


class SocketKeywords(object):
    """SocketKeywords are common resource for simple socket keywords."""

    def __init__(self):
        super(SocketKeywords, self).__init__()

    @keyword
    def send_binary_data(self, host, port, data, ssl_enabled=None, cert_required=None, ca=None, cert=None, key=None):
        """ send raw bytes over tcp socket with optional ssl """
        if ssl_enabled:
            if cert_required:
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                context.verify_mode = ssl.CERT_REQUIRED
                # Load CA cert
                context.load_verify_locations(str(ca))
                # Load Client cert and key
                context.load_cert_chain(str(cert), str(key))
            else:
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
                context.verify_mode = ssl.CERT_OPTIONAL
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ssock = context.wrap_socket(sock, server_hostname=str(host))
            # Connect to server over ssl and send data
            ssock.connect((str(host), int(port)))
            ssock.sendall(bytes(data))
            ssock.close()
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect to server and send data
            sock.connect((str(host), int(port)))
            sock.sendall(bytes(data))
            sock.close()
