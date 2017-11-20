from server import hascii as h


class Motors:
    def __init__(self, number_of_motors):
        # This sets number of motors
        self._motors = [0] * number_of_motors

    # It is more natural when 0 means no moving
    # So this f. inverts 0 -> 4095 and vice versa

    @staticmethod
    def _invert(value):
        if 0 <= value <= 4095:
            return 4095 - value
        elif -4095 <= value <= 0:
            return -(4095 - abs(value))

    # First, It inverts motor PWM value (0 is 4095),
    # then converts to hascii
    def convert(self, motors):
        packet = bytearray()
        for motor in motors:
            packet.extend(h.encode8(self._invert(motor)))
        return packet

    def motor(self, motor_id, value):
        for index, prev_value in enumerate(self._motors):
            if index == motor_id - 1:
                self._motors[index] = value
            else:
                self._motors[index] = 0
        return self.convert(self._motors)

    def all(self, value):
        for index in range(len(self._motors)):
            self._motors[index] = value
        return self.convert(self._motors)


