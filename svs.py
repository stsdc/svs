import socket
import log

if (socket.gethostname() == 'main_unit'):
    import server
else:
    import client
