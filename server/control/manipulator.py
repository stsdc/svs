from log import logger
import threading
from events import Events
import binascii
import server.hascii as h


class Manipulator:
    def __init__(self, uart):
        self._thread = None
        self.events = Events()
        self.uart = uart

        # self.get_status()

        self.get_info()
        self.motor1_inc_pos()
        # self.get_info()

    def get_status(self):
        self._thread = threading.Timer(0.5, self.get_status)
        self._thread.start()

        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x22)
        packet.append(0x2A)
        packet.append(0x0A)


        self.uart.write(packet)
        packet = None

        response = self.uart.readline()
        # response = response.encode('hex')
        self.events.on_data(self.parse(response))

    def parse(self, response):
        # the first three characters are junk
        response = response[2:]

        # logger.debug("Manipulator: Recieved: %s", response)
        return {
            "current1": h.decode(response[13:16]),  # 13, 14, 15
            "velocity1": h.decode(response[16:24]),
            "position1": h.decode(response[24:32]),

            "current2": h.decode(response[32:35]),
            "velocity2": h.decode(response[35:43]),
            "position2": h.decode(response[43:51]),

            "current3": h.decode(response[51:54]),
            "velocity3": h.decode(response[54:62]),
            "position3": h.decode(response[62:70]),

            "current4": h.decode(response[70:73]),
            "velocity4": h.decode(response[73:81]),
            "position4": h.decode(response[81:89]),
        }

        # return {
        #     "current1": response[13:16],  # 13, 14, 15
        #     "velocity1": response[16:24],
        #     "position1": response[24:32],
        #
        #     "current2": response[32:35],
        #     "velocity2": response[35:43],
        #     "position2": response[43:51],
        #
        #     "current3": response[51:54],
        #     "velocity3": response[54:62],
        #     "position3": response[62:70],
        #
        #     "current4":response[70:73],
        #     "velocity4": response[73:81],
        #     "position4": response[81:89],
        # }

    def motor1_inc_pos(self):

        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x22)
        packet.append(0x21)
        #
        # packet.append(0x30)
        # packet.append(0x30)
        # packet.append(0x30)

        packet.extend(h.encode8(4095))

        packet.extend(h.encode8(4095)) # black

        packet.extend(h.encode8(0)) # max

        packet.extend(h.encode8(4095)) # black


        packet.append(0x0A)
        self.uart.write(packet)
        logger.debug(binascii.hexlify(packet))

    def get_info(self):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x22)
        packet.append(0x54)
        packet.append(0x33)  # silnik
        packet.append(0x31)  # tak musi byc
        packet.append(0x30)
        packet.append(0x0A)

        self.uart.write(packet)

        response = self.uart.readline()

        logger.debug(response[2:])

    def stop(self):
        self._thread.cancel()
