import errno
import json
import socket
import sys
from time import sleep

from log import logger


class SocketClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.settimeout(5)

    def connect(self):
        while True:
            try:
                self.socket.connect((self.host, self.port))
                break
            except socket.error as e:
                if e.errno == errno.ECONNREFUSED:
                    logger.warning("SocketClient: %s", e)
                # else:
                #     logger.exception("SocketClient: %s", e)
                #     continue
            sleep(1)

    def __del__(self):
        self.close()

    def send(self, data):
        serialized = ""
        if not self.socket:
            logger.error('You have to connect first before sending data')
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError), e:
            logger.error('You can only send JSON-serializable data')
        # send the length of the serialized data first
        self.socket.send('%d\n' % len(serialized))
        # send the serialized data
        self.socket.sendall(serialized)
        return self

    def recv(self):
        if not self.socket:
            logger.error('You have to connect first before receiving data')
        length_str = ''
        char = self.socket.recv(1)
        while char != '\n':
            length_str += char
            char = self.socket.recv(1)
        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = self.socket.recv_into(view[next_offset:],
                                              total - next_offset)
            next_offset += recv_size
        try:
            deserialized = json.loads(view.tobytes())
        except (TypeError, ValueError), e:
            logger.error('Data received was not in JSON format', e)
        return deserialized

    def recv_and_close(self):
        data = self.recv()
        self.close()
        return data

    def close(self):
        if self.socket:
            self.socket.close()
        self.socket = None
