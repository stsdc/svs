from log import logger
import threading
from events import Events
import binascii
import server.hascii as h
from motors import Motors
from rbc4242 import RbC4242

# ON RbC-4242
# 0x22: [MOT10 -> PIN10 MOT1 -> PIN1] [MOT3 -> PIN10 MOT2 -> PIN1]
# 0x21: [MOT1 -> PIN1 MOT2 -> PIN10] [MOT3 -> PIN1 MOT2 -> PIN10]

class Manipulator:
    def __init__(self, uart):
        self.events = Events()
        self.uart = uart
        self.prev_data = None
        self._thread = None
        self.module_21 = RbC4242(0x21)
        self.module_22 = RbC4242(0x22)
        self.motors = Motors(4)

    def get_status(self):
        self._thread = threading.Timer(2, self.get_status)
        self._thread.start()

        packet = self.module_21.get_motors_status()
        self.uart.write(packet)
        response = self.uart.readline()
        # self.parse(response)
        self.events.on_data(self.parse(response))

    def parse(self, response):
        # the first three characters are junk
        response = response[2:]

        logger.debug("Manipulator: Recieved: %s", response)
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

    def forward(self, motor_id, value=4000):
        motors_pwm_values = self.motors.motor(motor_id, value)
        packet = self.module_21.set_motors_pwm(motors_pwm_values)
        self.send(packet)

    def backward(self, motor_id, value=-4000):
        motors_pwm_values = self.motors.motor(motor_id, value)
        packet = self.module_21.set_motors_pwm(motors_pwm_values)
        self.send(packet)


    def send(self, packet):
        # send only if data chenged
        if self.prev_data != packet:
            self.uart.write(packet)
            self.prev_data = packet
            logger.debug(binascii.hexlify(packet))

    def halt(self):
        motors_pwm_values = self.motors.all(0)
        packet = self.module_21.set_motors_pwm(motors_pwm_values)
        self.send(packet)

    def stop(self):
        self._thread.join()
