from lcd_display import test_lcd
from camera_test import test_camera
from relay_test import test_relay


def test():
    """
    Test the modules.
    """
    print("Testing LCD display...")
    lcd = test_lcd()
    if lcd:
        print("LCD display is working properly")
    else:
        print("LCD display is not working properly")

    print("Testing camera...")
    camera = test_camera()
    if camera:
        print("Camera is working properly")
    else:
        print("Camera is not working properly")

    print("Testing relay...")
    relay = test_relay()
    if relay:
        print("Relay is working properly")
    else:
        print("Relay is not working properly")

    print("Testing complete")
    print("Proced with installation?")
    print("1. Yes")
    print("2. No")
    choice = input("Enter your choice: ")
    if choice == "1":
        return True
    elif choice == "2":
        return False
