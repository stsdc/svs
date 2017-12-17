from log import logger
import threading
from events import Events
import binascii
from rbc4242 import RbC4242
from time import sleep

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

        # self.get_status()

    def get_status(self):
        self._thread_get_motors_status = threading.Timer(1, self.get_status)
        self._thread_get_motors_status.daemon = True
        self._thread_get_motors_status.start()

        packet_21 = self.module_21.get_motors_status()
        packet_22 = self.module_22.get_motors_status()

        self.uart.write(packet_21)
        sleep(0.5)

        self.uart.write(packet_22)

        res_21 = self.uart.readline()
        sleep(0.5)
        res_22 = self.uart.readline()

        # this is bad
        parsed_21 = self.module_21.parse_status(res_21)
        if parsed_21:
            parsed_22 = self.module_22.parse_status(res_22)
        else:
            parsed_21 = self.module_21.parse_status(res_22)
            parsed_22 = self.module_22.parse_status(res_21)

        self.events.on_data([parsed_21, parsed_22])

    def forward(self, motor_id, value=4000):
        if motor_id < 5:
            packet = self.module_21.set_single_motor_pwm(motor_id, value)
        else:
            packet = self.module_22.set_single_motor_pwm(motor_id - 4, value)
        self.send(packet)

    def backward(self, motor_id, value=-4000):
        if motor_id < 5:
            packet = self.module_21.set_single_motor_pwm(motor_id, value)
        else:
            packet = self.module_22.set_single_motor_pwm(motor_id - 4, value)
            self.send(packet)
        self.send(packet)

    def send(self, packet):
        # Send only if data changed
        # Canceling thread to prevent multiple errors
        if self.prev_data != packet:
            # if self._thread_get_motors_status:
            #     self._thread_get_motors_status.cancel()
            #     del self._thread_get_motors_status

            self.uart.write(packet)
            self.prev_data = packet
            logger.debug(binascii.hexlify(packet))

            # self.get_status()

    def halt(self):
        packet_21 = self.module_21.set_all_motors_pwm(0)
        self.send(packet_21)

        packet_22 = self.module_22.set_all_motors_pwm(0)
        self.send(packet_22)


    def stop(self):
        self.halt()
        self._thread_get_motors_status.join()
