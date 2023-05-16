"""
Author: Asikhalaye Samuel
Date: 3rd May, 2023

Creates Config file for the application from the
user's input on commandline and make it available for the application
makes the application run on startup by creating a startup
file for the application on raspberry pi
"""

import sys
import subprocess
from pathlib import Path
from configparser import ConfigParser
from src.test import test


def create_config_option(config=ConfigParser()):
    # Ask user if they want to use the default settings
    # or they want to use their own settings
    print("Do you want to use the default settings?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice: ")
    if choice == "1":
        # Use default settings
        config["DEFAULT"] = {
            "camera": "0",
            "resolution": "640x480",
            "framerate": "30",
            "relay_gpio": "17",
            "i2c_address": "0x27",
            "i2c_port": "1",
        }
    elif choice == "2":
        # Use custom settings
        camera = input("Enter camera: ")
        resolution = input("Enter resolution: ")
        framerate = input("Enter framerate: ")
        relay_gpio = input("Enter relay GPIO: ")
        i2c_address = input("Enter I2C address: ")
        i2c_port = input("Enter I2C port: ")
        config["DEFAULT"] = {
            "camera": camera,
            "resolution": resolution,
            "framerate": framerate,
            "relay_gpio": relay_gpio,
            "i2c_address": i2c_address,
            "i2c_port": i2c_port,
        }
    else:
        print("Invalid choice")
        sys.exit(1)


def create_config_file():
    """Creates config file for the application"""
    config = ConfigParser()
    config["DEFAULT"] = {
        "camera": "0",
        "resolution": "640x480",
        "framerate": "30",
        "relay_gpio": "17",
        "i2c_address": "0x27",
        "i2c_port": "1",
    }

    # check if config file exists
    config_file = Path("/home/pi/fire_detection/config.ini")
    if config_file.exists():
        # if config file exists, ask user if they want to
        # overwrite the file
        print("Config file already exists")
        print("Do you want to overwrite the file?")
        print("1. Yes")
        print("2. No")
        choice = input("Enter your choice: ")
        if choice == "1":
            create_config_option(config)
        elif choice == "2":
            sys.exit(0)
        else:
            print("Invalid choice")
            sys.exit(1)
    else:
        create_config_option(config)


def create_startup_file():
    """Creates startup file for the application"""
    # check if startup file exists
    startup_file = Path("/home/pi/fire_detection/startup.sh")
    if startup_file.exists():
        # if startup file exists, ask user if they want to
        # overwrite the file
        print("Startup file already exists")
        print("Do you want to overwrite the file?")
        print("1. Yes")
        print("2. No")
        choice = input("Enter your choice: ")
        if choice == "1":
            with open("/home/pi/fire_detection/startup.sh", "w") as startupfile:
                startupfile.write(
                    "#!/bin/sh\n" "cd /home/pi/fire_detection\n" "python3 -m src.main\n"
                )
        elif choice == "2":
            sys.exit(0)
        else:
            print("Invalid choice")
            sys.exit(1)
    else:
        with open("/home/pi/fire_detection/startup.sh", "w") as startupfile:
            startupfile.write(
                "#!/bin/sh\n" "cd /home/pi/fire_detection\n" "python3 -m src.main\n"
            )


def install_dependencies():
    """Installs dependencies for the application"""
    print("Installing dependencies...")
    # install dependencies from requirements.txt
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])


def main():
    """Main function"""
    # create config file
    create_config_file()

    # Test
    # if not test():
    #     print("Test failed")
    #     print("Exiting...")
    #     sys.exit(1)

    # create startup file
    create_startup_file()

    # install dependencies
    install_dependencies()

    print("Installation successful")
