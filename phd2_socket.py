import socket
import json
import logging

logger = logging.getLogger('astropypi')


class PH2Socket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''
    MSGLEN = 1024

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def disconnect(self):
        if self.sock:
            self.sock.close()

    def receive(self):
        chunks = []
        bytes_recd = 0
        chunk = self.sock.recv(PH2Socket.MSGLEN)
        if chunk == '':
            raise RuntimeError("socket connection broken")
        str_data = ''.join(chunk)
        try:
            return json.loads(str_data)
        except ValueError:
            logger.warning("Error parsing: " + str_data)