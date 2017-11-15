import serial
import serial.tools.list_ports
from log import logger
from time import sleep
from threading import Thread


class Uart:
    def __init__(self):
        self.BAUD = 57600
        self.TIMEOUT = 0
        self.serial = None
        self._waiter_thread = None

        self.waiter()

    def write(self, data):
        self.serial.write(data)

    def readline(self):
        try:
            return self.serial.readline()
        except serial.SerialException as e:
            logger.error("UART: %s", e)
            return 0

    def waiter(self):
        self._waiter_thread = Thread(target=self.waiter, args = (10, ))
        self._waiter_thread.daemon = True
        self._waiter_thread.start()
        logger.info("UART: Waiting for serial device")
        while self.serial is None:
            for port in self.available_ports():
                if "USB" in port.name:
                    logger.info("UART: Found device: %s %s", port.name, port.manufacturer)
                    self.connect(port.device)

            sleep(2)
        # self._waiter_thread.join()

    def connect(self, device):
        try:
            self.serial = serial.Serial(device, baudrate=self.BAUD, timeout=self.TIMEOUT)
            logger.info("UART: Connected")
        except serial.SerialException as e:
            logger.error("UART: %s", e)

    def available_ports(self):
        return serial.tools.list_ports.comports()

    def stop(self):
        self._waiter_thread.join()
