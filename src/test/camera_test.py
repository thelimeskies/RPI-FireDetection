"""
Test the camera module

This module is used to test the camera module. It will show a live feed from the camera
and ask if it is working properly. If the user presses 'y' then the camera is working
properly and the program will exit. If the user presses 'n' then the program will exit
and the user will have to troubleshoot the camera.
"""

import sys
import time
from pathlib import Path
from configparser import ConfigParser

import cv2


def test_camera():
    """Test the camera"""
    # Read config file
    config = ConfigParser()
    config.read("/home/pi/fire_detection/config.ini")

    # Get camera number
    camera_number = config["DEFAULT"]["camera"]

    # Get resolution
    resolution = config["DEFAULT"]["resolution"].split("x")
    width = int(resolution[0])
    height = int(resolution[1])

    # Get framerate
    framerate = int(config["DEFAULT"]["framerate"])

    # Create camera object
    camera = cv2.VideoCapture(int(camera_number))

    # Set camera resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Set camera framerate
    camera.set(cv2.CAP_PROP_FPS, framerate)

    print("Camera is warming up...")
    time.sleep(2)
    print("Camera is ready")
    print("Is the camera working properly?")
    print("Press 'y' for yes")
    print("Press 'n' for no")

    # Check if camera is working properly
    while True:
        # Read frame from camera
        _, frame = camera.read()

        # Show frame
        cv2.imshow("Camera Test", frame)

        # Wait for keypress
        key = cv2.waitKey(1)

        # If key is 'y' then exit
        if key == ord("y"):
            break
        # If key is 'n' then exit
        elif key == ord("n"):
            sys.exit(1)

    # Release camera
    camera.release()

    # Destroy all windows
    cv2.destroyAllWindows()
