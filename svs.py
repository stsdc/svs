#!/home/unit0/.virtualenvs/cv/bin/python

import socket
import log

if (socket.gethostname() == 'main_unit'):
    import server
else:
    from client import Client
    Client()
