from peripherals import Keyboard

class Steerage:
    def __init__(self, manipulator, mobile_platform):
        self.manipulator = manipulator
        self.mobile_platform = mobile_platform

        # Init keyboard control
        self.keyboard = Keyboard()

        # self.peripherals.bd.when_double_pressed = self.make_snap

        # Control moving of Mobile Platform via keyboard
        self.keyboard.events.forward += self.forward
        self.keyboard.events.backward += self.backward
        self.keyboard.events.left += self.left
        self.keyboard.events.right += self.right
        self.keyboard.events.stop += self.stop

        # Control Manipulator via keyboard
        self.keyboard.events.get_some_debug_data += self.rbc_test

        self.motor_power = 20

    def move(self, motor_l, motor_r):
        self.mobile_platform.send(motor_l * self.motor_power, motor_r * self.motor_power)

    def forward(self):
        self.mobile_platform.send(1 * self.motor_power, 1 * self.motor_power)

    def backward(self):
        self.mobile_platform.send(-1 * self.motor_power, -1 * self.motor_power)

    def left(self):
        self.mobile_platform.send(int(0.2 * self.motor_power), 1 * self.motor_power)

    def right(self):
        self.mobile_platform.send(1 * self.motor_power, int(0.2 * self.motor_power))

    def stop(self):
        # Stop gracefully
        self.mobile_platform.send(0 * self.motor_power, 0 * self.motor_power)

    def rbc_test(self):
        self.manipulator.rbc_test()
