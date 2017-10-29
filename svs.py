import socket
import locale
locale.setlocale(locale.LC_ALL, 'C.UTF-8')

if socket.gethostname() == 'main_unit':
    from server import UI
    UI()

else:
    from client import Client
    client = Client()
    client.run()
