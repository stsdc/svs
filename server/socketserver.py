import multiprocessing
import socket
import sys

from log import logger


def handle(connection, address):
    try:
        logger.debug("Connected %r at %r", connection, address)
        while True:
            data = connection.recv(1024)
            if data == "":
                logger.debug("Socket closed remotely")
                break
            logger.debug("Received data %r", data)
            connection.sendall(data)
            logger.debug("Sent data")
    except:
        logger.exception("Problem handling request")
    finally:
        logger.debug("Closing socket")
        connection.close()


class Server(object):
    client = None

    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.bind((host, port))
        # Listen for 2 connections
        self.socket.listen(2)
        logger.info("Listening...")

    def __del__(self):
        self.close()

    def accept(self):
        if self.client:
            logger.info("Client is already connected, disconnecting...")
            self.client.close()
        self.client, self.client_addr = self.socket.accept()
        return self

    def send(self, data):
        if not self.client:
            logger.exception('Cannot send data, no client is connected')
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError), e:
            logger.exception('You can only send JSON-serializable data')
        # send the length of the serialized data first
        socket.send('%d\n' % len(serialized))
        # send the serialized data
        socket.sendall(serialized)
        return self

    def recv(self):
        if not self.client:
            logger.exception('Cannot receive data, no client is connected')
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
            logger.exception('Data received was not in JSON format', e)
        return deserialized

    def close(self):
        if self.client:
            self.client.close()
            self.client = None
        if self.socket:
            self.socket.close()
            self.socket = None
