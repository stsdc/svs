import serial
from log import logger
from time import sleep

class Uart:
    def __init__(self):
        self.serial = None
        try:
            self.serial = serial.Serial('/dev/ttyUSB0', baudrate=57600, timeout=0)
            logger.info("UART: device: %s", self.serial.name)
        except serial.SerialException as e:
            logger.error("UART: %s", e)

        # while True:
        #     self.rbc_test()
        #     sleep(1)

    def write(self, data):
        self.serial.write(data)

    def readline(self):
        try:
            return self.serial.readline()
        except serial.SerialException as e:
            logger.error("UART: %s", e)
            return 0





