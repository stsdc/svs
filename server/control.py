from bluedot import BlueDot
from log import logger


class Control:
    def __init__(self):
        self.bd = BlueDot()
        self.bd.print_messages = False
        logger.info("Control: Bluetooth server started...")

        self.bd.when_client_connects = self.is_connected
        self.bd.when_double_pressed = self.make_snap

    def is_connected(self):
        logger.info("BluetoothControl: Client connected")

    def make_snap(self, pos):
        logger.info("BluetoothControl: Snap %s", pos)
