from bytearraybuilder import BytearrayBuilder


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
