import serial
import serial.tools.list_ports
from log import logger
from time import sleep
from threading import Thread
from events import Events


class Uart(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.events = Events()
        self.BAUD = 57600
        self.TIMEOUT = 0
        self.serial = None


    def run(self):
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
        while self.serial is None:
            logger.info("UART: Waiting for serial device")
            for port in self.available_ports():
                if "AMA0" in port.name:
                    logger.info("UART: Found device: %s %s", port.name, port.manufacturer)
                    self.connect(port.device)
            sleep(2)

    def connect(self, device):
        try:
            self.serial = serial.Serial(device, baudrate=self.BAUD, timeout=self.TIMEOUT)
            self.events.on_connected()
            logger.info("UART: Connected")
        except serial.SerialException as e:
            logger.error("UART: %s", e)

    def available_ports(self):
        return serial.tools.list_ports.comports()

    def stop(self):
        self.join()
