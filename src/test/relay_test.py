"""
Test the relay module

This module is used to test the relay module. It will ask the user if the relay is
working properly. If the user presses 'y' then the relay is working properly and the
program will exit. If the user presses 'n' then the program will exit and the user will
have to troubleshoot the relay.
"""

# Import modules
from configparser import ConfigParser
import RPi.GPIO as GPIO


def test_relay():
    """Test the relay"""
    # Read config file
    config = ConfigParser()
    config.read("/home/pi/camera/config.ini")

    # Get relay GPIO pin
    relay_gpio = int(config["DEFAULT"]["relay_gpio"])

    # Set GPIO mode to BCM
    GPIO.setmode(GPIO.BCM)

    # Set GPIO pin as output
    GPIO.setup(relay_gpio, GPIO.OUT)

    # Turn on relay
    GPIO.output(relay_gpio, GPIO.HIGH)

    # Check if relay is working properly
    while True:
        # Ask user if relay is working properly
        print("Is the relay working properly?")
        print("1. Yes")
        print("2. No")
        choice = input("Enter your choice: ")
        if choice == "1":
            # Turn off relay
            GPIO.output(relay_gpio, GPIO.LOW)
            return True
        elif choice == "2":
            # Turn off relay
            GPIO.output(relay_gpio, GPIO.LOW)
            return False
        else:
            print("Invalid choice")
            continue
