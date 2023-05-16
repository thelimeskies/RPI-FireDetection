from src.modules.lcd_i2c import LCD
# The LCD display is a 16x2 display that is connected to the Raspberry Pi via I2C.


def test_lcd():
    lcd = LCD()
    lcd.write("Hello World")

    while True:
        print("Is the LCD working properly?")
        print("1. Yes")
        print("2. No")
        choice = input("Enter your choice: ")
        if choice == "1":
            lcd.clear()
            return True
        elif choice == "2":
            lcd.clear()
            return False
        else:
            print("Invalid choice")
            continue
