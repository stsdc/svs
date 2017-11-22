import keyboard
from log import logger
from events import Events


class Keyboard:
    def __init__(self):
        self.events = Events()

        # refresh UI - doesn't work -> remove
        keyboard.add_hotkey('r', self.refresh)

        # control Mobile Platform
        keyboard.add_hotkey('w', self.forward)
        keyboard.add_hotkey('s', self.backward)
        keyboard.add_hotkey('a', self.left)
        keyboard.add_hotkey('d', self.right)

        keyboard.add_hotkey('z', self.get_some_debug_data)

        # control Manipulator
        keyboard.add_hotkey('up+1', self.manipulator_motor_1_forward)
        keyboard.add_hotkey('down+1', self.manipulator_motor_1_backward)
        keyboard.add_hotkey('up+2', self.manipulator_motor_2_forward)
        keyboard.add_hotkey('down+2', self.manipulator_motor_2_backward)
        keyboard.add_hotkey('up+3', self.manipulator_motor_3_forward)
        keyboard.add_hotkey('down+3', self.manipulator_motor_3_backward)
        keyboard.add_hotkey('up+4', self.manipulator_motor_4_forward)
        keyboard.add_hotkey('down+4', self.manipulator_motor_4_backward)
        keyboard.add_hotkey('up+5', self.manipulator_motor_5_forward)
        keyboard.add_hotkey('down+5', self.manipulator_motor_5_backward)

        keyboard.add_hotkey('u', self.manipulator_status_update)


        keyboard.on_release(self.halt)

    def forward(self):
        self.events.forward()

    def backward(self):
        self.events.backward()

    def left(self):
        self.events.left()

    def right(self):
        self.events.right()

    def halt(self, event):
        if self.is_mobile_platform_steerage_keys(event):
            self.events.mobile_platform_halt()

        if self.is_manipulator_steerage_keys(event):
            self.events.manipulator_halt()

    def refresh(self):
        logger.debug("refresh")
        self.events.refresh()

    def get_some_debug_data(self):
        self.events.get_some_debug_data()

    def manipulator_motor_1_forward(self):
        self.events.manipulator_forward(1)

    def manipulator_motor_1_backward(self):
        self.events.manipulator_backward(1)

    def manipulator_motor_2_forward(self):
        self.events.manipulator_forward(2)

    def manipulator_motor_2_backward(self):
        self.events.manipulator_backward(2)

    def manipulator_motor_3_forward(self):
        self.events.manipulator_forward(3)

    def manipulator_motor_3_backward(self):
        self.events.manipulator_backward(3)

    def manipulator_motor_4_forward(self):
        self.events.manipulator_forward(4)

    def manipulator_motor_4_backward(self):
        self.events.manipulator_backward(4)

    def manipulator_motor_5_forward(self):
        self.events.manipulator_forward(5)

    def manipulator_motor_5_backward(self):
        self.events.manipulator_backward(5)

    def manipulator_status_update(self):
        self.events.manipulator_status_update()

    # retuns True if pressed/released key is WSAD
    @staticmethod
    def is_mobile_platform_steerage_keys(event):
        return (keyboard.matches(event, 'w') or
                keyboard.matches(event, 's') or
                keyboard.matches(event, 'a') or
                keyboard.matches(event, 'd'))

    # retuns True if pressed/released key is up/down/left/right
    @staticmethod
    def is_manipulator_steerage_keys(event):
        return (keyboard.matches(event, 'up') or
                keyboard.matches(event, 'down') or
                keyboard.matches(event, 'left') or
                keyboard.matches(event, 'right'))
