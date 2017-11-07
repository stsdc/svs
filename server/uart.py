import serial
from log import logger
from time import sleep

class Uart:
    def __init__(self):
        self.serial = None
        try:
            self.serial = serial.Serial('/dev/ttyUSB0', baudrate=57600, timeout=3.0)
            logger.info("Uart: device: %s", self.serial.name)
        except serial.SerialException as e:
            logger.error("Uart: %s", e)

        self.prev_data = ""

        # while True:
        #     self.rbc_test()
        #     sleep(1)

    def write(self, data):
        self.serial.write(data)

    def rbc_test(self):

        packet = bytearray()
        packet.append(0xFF)
        packet.append(0x21)
        packet.append(0x2A)
        packet.append(0x0A)

        self.serial.write(packet)
        response = self.serial.readline()
        response = response[3:]
        logger.debug(response)




