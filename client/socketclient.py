import errno
import json
import socket
import sys
from time import sleep
import pickle

from log import logger


class SocketClient(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket()
        self.socket.settimeout(5)
        self.size = 2048

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
            serialized = pickle.dumps(data)
        except (TypeError, ValueError), e:
            logger.error('SocketClient: Serialization: %s', e)
        self.socket.sendall(serialized)
        return self

    def recv(self):
        if not self.socket:
            logger.error('You have to connect first before receiving data')
        try:
            data = self.socket.recv(self.size)
            deserialized = pickle.loads(data)
        except BaseException as e:
            logger.error('SocketClient: Some problem with deserialization')
            return None
        return deserialized

    def recv_and_close(self):
        data = self.recv()
        self.close()
        return data

    def close(self):
        if self.socket:
            self.socket.close()
        self.socket = None
