from bytearraybuilder import BytearrayBuilder
from log import logger
import binascii
import server.hascii as h


class RbC4242:
    def __init__(self, address, number_of_motors):
        self._address = address
        self.motors = BytearrayBuilder(number_of_motors)

    def get_motors_status(self):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(self._address)
        packet.append(0x6F)
        packet.append(0x0A)
        return packet

    def set_pwm(self, values):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(self._address)
        packet.append(0x21)
        packet.extend(values)
        packet.append(0x0A)
        return packet

    def set_single_motor_pwm(self, motor_id, value):
        return self.set_pwm(self.motors.single(motor_id, value))

    def set_all_motors_pwm(self, value):
        return self.set_pwm(self.motors.all(value))

    def parse_status(self, response):
        try:
            logger.debug("RbC %s: Received: %s", hex(self._address), binascii.hexlify(response))
            if binascii.hexlify(response[0:3]) == self.prefix():
                response = response[2:]
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
            else:
                return False
        except IndexError as e:
            logger.error("RbC %s: %s", hex(self._address), e)

    def prefix(self):
        return "ff" + format(self._address, "x") + format(0x6F, "x")


