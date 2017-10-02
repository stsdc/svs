import select
import socket
import sys
from threading import Thread
import json
from time import sleep
from hotspot import HotSpot

from log import logger


class SocketServer(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.daemon = True
        self.host = host
        self.port = port
        self.backlog = 2
        self.size = 1024
        self.server = None
        self.threads = []
        self.running = 1

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.host, self.port))
            self.server.listen(self.backlog)
            logger.info("Listening...")
        except socket.error as e:
            if self.server:
                self.server.close()
            logger.error("Could not open socket: %s", e)
            sys.exit(1)

    def handle_data(self):
        # maybe remove this select?
        self.open_socket()
        input = [self.server, sys.stdin]
        while getattr(self, "do_run", True):
            inputready, outputready, exceptready = select.select(input, [], [])

            for s in inputready:

                if s == self.server:
                    # handle the server socket
                    client = Client(self.server.accept())
                    client.start()
                    self.threads.append(client)

    def stop(self):
        # close all client threads
        if self.server:
            self.server.close()
            logger.warning("SocketServer: Stop")

        if self.threads:
            for client in self.threads:
                client.join()

        self.do_run = False
        self.join()

    def check_connectivity(self):
        hotspot = HotSpot()
        if bool(hotspot.clients):
            for mac in hotspot.clients:
                logger.info("HotSpot: Connected client: %s, %s, %s", hotspot.clients[mac][4], hotspot.clients[mac][3],
                            hotspot.clients[mac][5])
            return True
        else:
            logger.warning("HotSpot: No clients")
        return False

    def run(self):
        is_client_connected = False
        while is_client_connected is not True:
            sleep(3)
            is_client_connected = self.check_connectivity()
        try:
            self.handle_data()
        except BaseException as e:
            logger.error("Error when starting server: %s", e)
            logger.warning("Checking connection and restarting server")
            self.run()


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
            data = self._recv(self.client)
            print data
            if data:
                self._send(self.client, data)
            else:
                self.client.close()
                running = 0

    def _send(self, client, data):
        try:
            serialized = json.dumps(data)
        except (TypeError, ValueError) as e:
            raise Exception('You can only send JSON-serializable data')
        # send the length of the serialized data first
        d = '%d\n' % len(serialized)
        client.send(d.encode('utf-8'))
        # send the serialized data
        client.sendall(serialized.encode('utf-8'))

    def _recv(self, client):
        # read the length of the data, letter by letter until we reach EOL
        length_str = ''
        char = client.recv(1).decode('utf-8')

        while char != '\n':
            length_str += char
            char = client.recv(1).decode('utf-8')

        total = int(length_str)
        # use a memoryview to receive the data chunk by chunk efficiently
        view = memoryview(bytearray(total))
        next_offset = 0
        while total - next_offset > 0:
            recv_size = client.recv_into(view[next_offset:], total - next_offset)
            next_offset += recv_size
        try:
            view = view.tobytes()
            deserialized = json.loads(view.decode('utf-8'))
        except (TypeError, ValueError) as e:
            raise Exception('Data received was not in JSON format')
        return deserialized


