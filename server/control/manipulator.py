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
        logger.debug(response[3:])
        self.events.on_data(self.parse(response))

    def hascii82dec(self, data):
        try:
            dec = int(data, 16)
            return dec
        except ValueError as e:
            logger.error("Manipulator: %s", e)

    def parse(self, response):
        # the first three characters are junk
        response = response[3:]
        # slicing bytearray and converting to dec
        return {
            "time": self.hascii82dec(response[0:8]),
            "adc0": self.hascii82dec(response[8:11]),
            "adc1": self.hascii82dec(response[11:14]),
            "adc2": self.hascii82dec(response[14:17]),
            "current": self.hascii82dec(response[17:20]),
            "velocity": self.hascii82dec(response[20:28]),
            "position": self.hascii82dec(response[28:36]),
        }

    def stop(self):
        self._thread.cancel()
