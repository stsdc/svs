from server.uart import Uart
from log import logger


class MobilePlatform:
    def __init__(self, uart):
        self.uart = uart
        self.prev_data = ""

    def send(self, motor_l, motor_r):
        data = self.build_string(motor_l, motor_r)
        # made this to send data only once, since keyboard module sends it over and
        # over again. Should be done in keyboard module
        if self.prev_data != data:
            logger.debug("MobilePlatform: send: %s", data.replace("\r\n", ""))
            self.uart.write(data)
        self.prev_data = data

    def build_string(self, motor_l, motor_r):
        prefix = "FF2029"
        postfix = "$0A\r\n"
        return prefix + self.convert(motor_l) + self.convert(motor_r) + postfix

    def convert(self, power):
        if power >= 0:
            return "+" + self.canonicalize(power)
        if power < 0:
            return "-" + self.canonicalize(abs(power))

    def canonicalize(self, power):
        power = str(power)
        if len(power) == 1:
            return "00" + power
        if len(power) == 2:
            return "0" + power
        if len(power) == 3:
            return power
