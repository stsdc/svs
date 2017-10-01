import select
import socket
import sys
from threading import Thread
import json
from log import logger


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.backlog = 2
        self.size = 1024
        self.server = None
        self.threads = []

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
            logger.info("Listening...")
        except socket.error, (value, message):
            if self.server:
                self.server.close()
            logger.exception("Could not open socket: " + message)
            sys.exit(1)

    def run(self):
        self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            inputready, outputready, exceptready = select.select(input, [], [])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    client = Client(self.server.accept())
                    client.start()
                    self.threads.append(client)

                elif s == sys.stdin:
                    # handle standard input
                    junk = sys.stdin.readline()
                    running = 0

        # close all threads
        self.server.close()
        for client in self.threads:
            client.join()


class Client(Thread):
    def __init__(self, (client, address)):
        Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.daemon = True

    def run(self):
        running = 1
        while running:
            data = _recv(self.client)
            print data
            if data:
                _send(self.client, data)
            else:
                self.client.close()
                running = 0


def _send(socket, data):
    try:
        serialized = json.dumps(data)
    except (TypeError, ValueError) as e:
        raise Exception('You can only send JSON-serializable data')
    # send the length of the serialized data first
    d = '%d\n' % len(serialized)
    socket.send(d.encode('utf-8'))
    # send the serialized data
    socket.sendall(serialized.encode('utf-8'))


def _recv(socket):
    # read the length of the data, letter by letter until we reach EOL
    length_str = ''
    char = socket.recv(1).decode('utf-8')

    while char != '\n':
        length_str += char
        char = socket.recv(1).decode('utf-8')

    total = int(length_str)
    # use a memoryview to receive the data chunk by chunk efficiently
    view = memoryview(bytearray(total))
    next_offset = 0
    while total - next_offset > 0:
        recv_size = socket.recv_into(view[next_offset:], total - next_offset)
        next_offset += recv_size
    try:
        view = view.tobytes()
        deserialized = json.loads(view.decode('utf-8'))
    except (TypeError, ValueError) as e:
        raise Exception('Data received was not in JSON format')
    return deserialized
