from box import Box
import os
from server.network import Network
import threading

class ServerBox(Box):
    def __init__(self, h, w, y, x):
        super(ServerBox, self).__init__(h, w, y, x)
        self.net = Network()

        self._thread = None

        self.set_colors_scheme()

        self.title("Server")

        self.add(0, 0, "PID:")
        self.add(0, 7, "%16s" % os.getpid())

        self.add(1, 0, "ETH:")
        self.add(1, 7, "%16s" % self.net.eth_ip())

        self.add(2, 0, "WLAN:")
        self.add(2, 7, "%16s" % self.net.wlan_ip())

        self.add(3, 0, "GPU TEMP:")
        self.add(3, 9, "%16s" % "")

        self.add(3, 0, "", self.default_colors)

        self.add(5, 0, "CONNECTED:")
        self.add(5, 11, "%12s" % "NO")

        self._temperature()

    def update_status(self, status):
        if status:
            self.add(5, 11, "%12s" % "YES")
        else:
            self.add(5, 11, "%12s" % "NO")

    def _temperature(self):
        self._thread = threading.Timer(2.0, self._temperature)
        self._thread.start()
        c = u"\u00B0"
        celsius = c.encode('utf-8')
        res = os.popen("vcgencmd measure_temp").readline()
        res = (res.replace("temp=", "").replace("'", celsius))
        self.add(3, 9, "%16s" % res, self.default_colors)
        self.set_colors_scheme()

    def close(self):
        self._thread.cancel()
