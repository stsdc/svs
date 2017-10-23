from control import KeyboardControl
from radio import Radio


class Steerage:
    def __init__(self):
        self.keyboard_control = KeyboardControl()

        # self.control.bd.when_double_pressed = self.make_snap
        self.keyboard_control.events.forward += self.forward
        self.keyboard_control.events.backward += self.backward
        self.keyboard_control.events.stop += self.stop

        self.motor_power = 20
        self.radio = Radio()

    def move(self, motor_l, motor_r):
        self.radio.send(motor_l * self.motor_power, motor_r * self.motor_power)

    def forward(self):
        self.radio.send(1 * self.motor_power, 1 * self.motor_power)

    def backward(self):
        self.radio.send(-1 * self.motor_power, -1 * self.motor_power)

    def stop(self):
        # Stop gracefully
        self.radio.send(0 * self.motor_power, 0 * self.motor_power)
