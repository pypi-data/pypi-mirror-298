import warnings
warnings.simplefilter('ignore')
import logger

from gpiozero import DigitalOutputDevice, BadPinFactory
import time

logging = logger.Logger()


class Relay():
    gpio_number = None
    relay = None

    def __init__(self, gpio_number):
        self.gpio_number = gpio_number

    def on(self):
        try:
            self.relay = DigitalOutputDevice(self.gpio_number)
            logging.debug("GPIO " + str(self.gpio_number) + " trigger")
        except BadPinFactory as error:
            logging.warning(str("Unable to open the relay via GPIO. Not a raspberry pi? emulating GPIO " + str(self.gpio_number)) + " trigger")

    def off(self):
        try:
            self.relay.close()
            logging.debug("GPIO " + str(self.gpio_number) + " release")
        except:
            logging.warning(str("Unable to close the relay via GPIO. Not a raspberry pi? emulating GPIO " + str(self.gpio_number)) + " release")
