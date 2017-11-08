from log import logger
import threading
from events import Events


class Manipulator:
    def __init__(self, uart):
        self._thread = None
        self.events = Events()
        self.uart = uart

        self.rbc_test()

    def rbc_test(self):
        self._thread = threading.Timer(0.5, self.rbc_test)
        self._thread.start()

        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x21)
        packet.append(0x2A)
        packet.append(0x0A)

        self.uart.write(packet)
        packet = None

        response = self.uart.readline()
        response = response[3:]
        time = response[:8]
        self.events.on_data(self.hascii82dec(time))
        logger.debug(self.hascii82dec(time))

    def hascii82dec(self, data):
        try:
            dec = int(data, 16)
            return dec
        except ValueError as e:
            logger.error("Manipulator: %s", e)

    def stop(self):
        self._thread.cancel()


