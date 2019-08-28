# Copyright 2019 AT&T Intellectual Property. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import ssl
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
