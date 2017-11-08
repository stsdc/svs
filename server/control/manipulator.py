from server.uart import Uart
from log import logger

class Manipulator:
    def __init__(self, uart):
        self.uart = uart

    def rbc_test(self):

        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x21)
        packet.append(0x2A)
        packet.append(0x0A)

        self.uart.write(packet)
        response = self.uart.readline()
        response = response[3:]
        time = response[:8]
        logger.debug(self.hascii82dec(time))

    def hascii82dec(self, data):
        return int(data, 16)


