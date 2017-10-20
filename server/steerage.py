import keyboard
from log import logger
from events import Events


class Steerage:
    def __init__(self):
        self.events = Events()

        keyboard.add_hotkey('w', self.forward)
        keyboard.add_hotkey('s', self.backward)
        keyboard.add_hotkey('a', self.left)
        keyboard.add_hotkey('d', self.right)

        keyboard.on_release(self.stop)

    def forward(self):
        self.events.forward(1, 1)

    def backward(self):
        logger.debug("BACKWARD")

    def left(self):
        logger.debug("LEFT")

    def right(self):
        logger.debug("RIGHT")

    def stop(self, event):
        # Stop gracefully
        self.events.stop(0, 0)
