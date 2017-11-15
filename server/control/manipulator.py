from log import logger
import threading
from events import Events
import binascii
import server.hascii as h


class Manipulator:
    def __init__(self, uart):
        self.events = Events()
        self.uart = uart
        self.prev_data = None

    def get_status(self):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x22)
        packet.append(0x2A)
        packet.append(0x0A)

        self.uart.write(packet)
        del packet

        response = self.uart.readline()

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

    def motor1_inc_pos(self):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x21)
        packet.append(0x21)

        # 0 -> 0x30 -> 0%

        # ON RbC-4242
        # 0x22: [MOT10 -> PIN10 MOT1 -> PIN1] [MOT3 -> PIN10 MOT2 -> PIN1]
        # 0x21: [MOT1 -> PIN1 MOT2 -> PIN10] [MOT3 -> PIN1 MOT2 -> PIN10]

        packet.extend(h.encode8(0))
        packet.extend(h.encode8(1300))  # MOT1
        packet.extend(h.encode8(0))
        packet.extend(h.encode8(0))

        packet.append(0x0A)

        if self.prev_data != packet:
            self.uart.write(packet)
            self.prev_data = packet
            logger.debug(binascii.hexlify(packet))

    def halt(self):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x21)
        packet.append(0x21)
        # 4095 -> 0xFF 0xFF 0xFF -> 100%
        packet.extend(h.encode8(4095))
        packet.extend(h.encode8(4095))
        packet.extend(h.encode8(4095))
        packet.extend(h.encode8(4095))
        packet.append(0x0A)

        self.uart.write(packet)
        self.prev_data = packet
