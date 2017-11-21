from log import logger
import threading
from events import Events
import binascii
from rbc4242 import RbC4242


# ON RbC-4242
# 0x22: [MOT10 -> PIN10 MOT1 -> PIN1] [MOT3 -> PIN10 MOT2 -> PIN1]
# 0x21: [MOT1 -> PIN1 MOT2 -> PIN10] [MOT3 -> PIN1 MOT2 -> PIN10]

class Manipulator:
    def __init__(self, uart):
        self.events = Events()
        self.uart = uart
        self.prev_data = None
        self._thread_get_motors_status = None
        self.module_21 = RbC4242(0x21, 4)
        self.module_22 = RbC4242(0x22, 4)

        self.get_status()

    def get_status(self):
        self._thread_get_motors_status = threading.Timer(2, self.get_status)
        self._thread_get_motors_status.start()

        packet_21 = self.module_21.get_motors_status()
        packet_22 = self.module_22.get_motors_status()

        self.uart.write(packet_21)
        response_from_21 = self.uart.readline()
        parsed = self.module_21.parse_status(response_from_21)

        self.events.on_data(parsed)

    def forward(self, motor_id, value=4000):
        packet = self.module_21.set_single_motor_pwm(motor_id, value)
        self.send(packet)

    def backward(self, motor_id, value=-4000):
        packet = self.module_21.set_single_motor_pwm(motor_id, value)
        self.send(packet)

    def send(self, packet):
        # Send only if data changed
        # Canceling thread to prevent multiple errors
        if self.prev_data != packet:
            if self._thread_get_motors_status:
                self._thread_get_motors_status.cancel()

            self.uart.write(packet)
            self.prev_data = packet
            logger.debug(binascii.hexlify(packet))

            if not self._thread_get_motors_status:
                self.get_status()

    def halt(self):
        packet = self.module_21.set_all_motors_pwm(0)
        self.send(packet)

    def stop(self):
        self._thread_get_motors_status.join()
