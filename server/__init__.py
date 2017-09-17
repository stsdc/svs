from log import logger
import socket
import sys
import multiprocessing

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
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)
        logger.info("Listening")

        while True:
            conn, address = self.socket.accept()
            logger.debug("Got connection")
            process = multiprocessing.Process(target=handle, args=(conn, address))
            process.daemon = True
            process.start()
            logger.debug("Started process %r", process)

# if __name__ == "__main__":
logger.debug("Initializing %s", socket.gethostname())

server = Server("", 9000)
try:
    server.start()
except:
    logger.exception("Unexpected exception")
finally:
    logger.info("Shutting down")
    for process in multiprocessing.active_children():
        logger.info("Shutting down process %r", process)
        process.terminate()
        process.join()
    logger.info("All done")
