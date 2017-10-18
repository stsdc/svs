from bluedot import BlueDot
from log import logger
from events import Events


class Control:
    def __init__(self, core):
        self.bd = BlueDot()
        self.bd.print_messages = False
        logger.info("Control: Bluetooth server started...")

        self.bd.when_client_connects = self.is_connected

    def is_connected(self):
        logger.info("Control: Client connected via bluetooth")
