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
        keyboard.add_hotkey('up', self.motor1_inc_pos)
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

    def motor1_inc_pos(self):
        self.events.motor1_inc_pos()

    def manipulator_status_update(self):
        self.events.manipulator_status_update()

    # retuns True if pressed/released key is WSAD
    @staticmethod
    def is_mobile_platform_steerage_keys(event):
        return (keyboard.matches(event, 'w') or
                keyboard.matches(event, 's') or
                keyboard.matches(event, 'a') or
                keyboard.matches(event, 'd'))

    @staticmethod
    def is_manipulator_steerage_keys(event):
        return (keyboard.matches(event, 'up') or
                keyboard.matches(event, 'down') or
                keyboard.matches(event, 'left') or
                keyboard.matches(event, 'right'))
