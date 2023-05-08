import os
from modules.lcd_i2c import LCD
from modules.capture import Capture
from modules.relay import Relay

# Use ConfigParser to read config file
from configparser import ConfigParser

config = ConfigParser()
config.read("/home/pi/camera/config.ini")

# Get the camera, resolution, framerate, and relay GPIO from config file
camera = int(config["DEFAULT"]["camera"])
resolution = tuple(map(int, config["DEFAULT"]["resolution"].split("x")))
framerate = int(config["DEFAULT"]["framerate"])
relay_gpio = int(config["DEFAULT"]["relay_gpio"])
i2c_address = int(config["DEFAULT"]["i2c_address"], 16)
i2c_port = int(config["DEFAULT"]["i2c_port"])


class App:
    """
    Capture images from camera and predicts if fire is present or not.

    If fire is present, the relay will be turned on and the LCD will display
    "Fire Detected".Otherwise, the relay will be turned off and the LCD will
    display "No Fire Detected".
    """

    def __init__(self, fire_cascade_path: str):
        self.lcd = LCD(i2c_address, i2c_port)
        self.capture = Capture(camera, resolution, framerate)
        self.relay = Relay(relay_gpio)

        self.fire_cascade_path = fire_cascade_path
        self.fire_cascade = self.capture.cascade(self.fire_cascade_path)

    def run(self):
        """
        Run the application.
        """

        while True:
            frame = self.capture.get_frame()
            gray = self.capture.gray(frame)
            fire = self.fire_cascade.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=5
            )

            if len(fire) > 0:
                self.relay.on()
                self.lcd.write("Fire Detected")
            else:
                self.relay.off()
                self.lcd.write("No Fire Detected")

            self.capture.imshow("Fire Detection", frame)

            if self.capture.wait_key() == ord("q"):
                break

        self.capture.release()


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CASCADE_DIR = os.path.join(BASE_DIR, "hsv_colour/fire_detection.xml")

    app = App(CASCADE_DIR)
    app.run()
