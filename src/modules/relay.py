"""
Relay module controls the relay board on the Raspberry Pi.

Gets the relay pin from the config file and sets the pin to output.
"""

import RPi.GPIO as GPIO


class Relay:
    """
    Relay class controls the relay board on the Raspberry Pi.
    """

    def __init__(self, pin: int = 17):
        """
        Constructor for the Relay class.
        """

        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        """
        Turns on the relay.
        """

        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        """
        Turns off the relay.
        """

        GPIO.output(self.pin, GPIO.LOW)
