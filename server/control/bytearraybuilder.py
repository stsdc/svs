from server import hascii as h


# This class builds motors bytearray for 0x21 command
class BytearrayBuilder:
    def __init__(self, number_of_values):
        # This sets number of motors
        self._values = [0] * number_of_values

    # It is more natural when 0 means no moving
    # So this f. inverts 0 -> 4095 and vice versa
    # Inverts for 3 characters !!!

    @staticmethod
    def _invert(value):
        if 0 <= value <= 4095:
            return 4095 - value
        elif -4095 <= value <= 0:
            return -(4095 - abs(value))

    # First, It inverts motor PWM value (0 is 4095),
    # then converts to hascii and returns 8hascii*motors
    def hasciify(self, values):
        packet = bytearray()
        for value in values:
            packet.extend(h.encode8(self._invert(value)))
        return packet

    # Sets one motor to desired value, other to zero
    # returns bytearray with values for all motors
    def single(self, value_id, value):
        for index, prev_value in enumerate(self._values):
            if index == value_id - 1:
                self._values[index] = value
            else:
                self._values[index] = 0
        return self.hasciify(self._values)

    # Sets all to desired value
    # returns bytearray with values for all motors
    def all(self, value):
        for index in range(len(self._values)):
            self._values[index] = value
        return self.hasciify(self._values)
