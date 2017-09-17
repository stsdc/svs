import socket

if (socket.gethostname() == 'main_unit'):
    print("This is main unit")
else:
    print("This is slave unit")
