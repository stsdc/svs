import serial
from log import logger


class Radio:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=3.0)
        logger.info("RadioControl: device: %s", self.serial.name)
        self.prev_data = ""

    def send(self, motor_l, motor_r):
        data = self.build_string(motor_l, motor_r)
        # made this to send data only once, since keyboard module sends it over and
        # over again. Should be done in keyboard module
        if self.prev_data != data:
            logger.debug("RadioControl: send: %s", data.replace("\r\n", ""))
            self.serial.write(data)
        self.prev_data = data

    def build_string(self, motor_l, motor_r):
        prefix = "FF2029"
        postfix = "$0A\r\n"
        return prefix + self.convert(motor_l) + self.convert(motor_r) + postfix

    def convert(self, motor):
        if motor >= 0:
            return "+" + str(motor)
        return str(motor)



