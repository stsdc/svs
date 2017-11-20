class RbC4242:
    def __init__(self, address):
        self._address = address

    def get_motors_status(self):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(self._address)
        packet.append(0x6F)
        packet.append(0x0A)
        return packet

    def set_motors_pwm(self, ):
        packet = bytearray()
        packet.append(0xFF)
        packet.append(self._address)
        packet.append(0x21)
