import keyboard
from log import logger
from events import Events


class Keyboard:
    def __init__(self):
        self.events = Events()

        # refresh UI
        keyboard.add_hotkey('r', self.refresh)

        # control Mobile Platform
        keyboard.add_hotkey('w', self.forward)
        keyboard.add_hotkey('s', self.backward)
        keyboard.add_hotkey('a', self.left)
        keyboard.add_hotkey('d', self.right)

        keyboard.add_hotkey('z', self.get_some_debug_data)

        keyboard.on_release(self.stop)

    def forward(self):
        self.events.forward()

    def backward(self):
        self.events.backward()

    def left(self):
        self.events.left()

    def right(self):
        self.events.right()

    def stop(self, event):
        if self.is_mobile_platform_steerage_keys(event):
            self.events.stop()

    def refresh(self):
        logger.debug("refresh")
        self.events.refresh()

    def get_some_debug_data(self):
        self.events.get_some_debug_data()

    # retuns True if pressed/released key is WSAD
    @staticmethod
    def is_mobile_platform_steerage_keys(event):
        return (keyboard.matches(event, 'w') or
                keyboard.matches(event, 's') or
                keyboard.matches(event, 'a') or
                keyboard.matches(event, 'd'))
