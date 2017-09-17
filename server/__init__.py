from log import logger
import socket
import sys

HOST = ''   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

logger.info("Initializing Main Unit")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
logger.info("Socket created")

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    logger.error('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

logger.info('Socket bind complete')

#Start listening on socket
s.listen(10)
logger.info('Socket now listening')

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    logger.info('Connected with ' + addr[0] + ':' + str(addr[1]))

s.close()
