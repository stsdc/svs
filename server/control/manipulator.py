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
        # response = response.encode('hex')
        self.events.on_data(self.parse(response))

    def hascii82dec(self, data):
        try:
            dec = int(data, 16)
            return dec
        except ValueError as e:
            logger.error("Manipulator: %s", e)

    def parse(self, response):
        # the first three characters are junk
        response = response[2:]
        logger.debug("Manipulator: %s", response)
        # slicing bytearray and converting to dec
        return {
            "current1": response[13:16],  # 13, 14, 15
            "velocity1": response[16:24],
            "position1": response[24:32],

            "current2": response[32:35],
            "velocity2": response[35:43],
            "position2": response[43:51],

            "current3": response[51:54],
            "velocity3": response[54:62],
            "position3": response[62:70],

            "current4": response[70:73],
            "velocity4": response[73:81],
            "position4": response[81:89],
        }

    def stop(self):
        self._thread.cancel()
