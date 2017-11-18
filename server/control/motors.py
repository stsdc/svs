from server import hascii as h


class Motors:
    def __init__(self):
        self._motors = [0, 0, 0, 0]

    # It is more natural when 0 means no moving
    # So this f. inverts 0 -> 4095 and vice versa

    @staticmethod
    def _invert(value):
        if 0 <= value <= 4095:
            return 4095 - value
        elif -4095 <= value <= 0:
            return -(4095 - abs(value))

    def set(self, motors):
        packet = bytearray()
        for motor in motors:
            packet.extend(h.encode8(self._invert(motor)))
        return packet

    def _set_m1(self, value):
        return self.set([value, 0, 0, 0])

    def _set_m2(self, value):
        return self.set([0, value, 0, 0])

    def _set_m3(self, value):
        return self.set([0, 0, value, 0])

    def _set_m4(self, value):
        return self.set([0, 0, 0, value])

    def motor(self, motor_id, value):
        if motor_id == 1:
            return self._set_m1(value)
        elif motor_id == 2:
            return self._set_m2(value)
        elif motor_id == 3:
            return self._set_m3(value)
        elif motor_id == 4:
            return self._set_m4(value)
        else:
            return self.set([0, 0, 0, 0])
