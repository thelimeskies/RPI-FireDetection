"""
I2C LCD module

Raspberry Pi I2C LCD library for the HD44780 controller.
"""

import smbus2
import time
import configparser as ConfigParser


class Commands:
    """
    Commands class contains the commands for the LCD.
    """

    CLEAR_DISPLAY = 0x01
    RETURN_HOME = 0x02
    ENTRY_MODE_SET = 0x04
    DISPLAY_CONTROL = 0x08
    CURSOR_SHIFT = 0x10
    FUNCTION_SET = 0x20
    SET_CGRAM_ADDR = 0x40
    SET_DDRAM_ADDR = 0x80


class Flags:
    """
    Flags class contains the flags for the LCD.
    """

    # Flags for display entry mode
    ENTRY_RIGHT = 0x00
    ENTRY_LEFT = 0x02
    ENTRY_SHIFT_INCREMENT = 0x01
    ENTRY_SHIFT_DECREMENT = 0x00

    # Flags for display on/off control
    DISPLAY_ON = 0x04
    DISPLAY_OFF = 0x00
    CURSOR_ON = 0x02
    CURSOR_OFF = 0x00
    BLINK_ON = 0x01
    BLINK_OFF = 0x00

    # Flags for display/cursor shift
    DISPLAY_MOVE = 0x08
    CURSOR_MOVE = 0x00
    MOVE_RIGHT = 0x04
    MOVE_LEFT = 0x00

    # Flags for function set
    EIGHT_BIT_MODE = 0x10
    FOUR_BIT_MODE = 0x00
    TWO_LINE = 0x08
    ONE_LINE = 0x00
    FIVE_BY_TEN_DOTS = 0x04
    FIVE_BY_SEVEN_DOTS = 0x00

    # Flags for backlight control
    BACKLIGHT = 0x08
    NO_BACKLIGHT = 0x00

    En = 0b00000100  # Enable bit
    Rw = 0b00000010  # Read/Write bit
    Rs = 0b00000001  # Register select bit


class i2c_device:
    def __init__(self, addr, port=1):
        self.addr = addr
        self.bus = smbus2.SMBus(port)

    def write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        time.sleep(0.0001)

    def write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        time.sleep(0.0001)

    def write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        time.sleep(0.0001)

    def read(self):
        return self.bus.read_byte(self.addr)

    def read_data(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

    def read_block_data(self, cmd):
        return self.bus.read_block_data(self.addr, cmd)

    def close(self):
        self.bus.close()


class LCD:
    def __init__(self, addr: int = 0x27, bus: int = 1):
        self.lcd_device = i2c_device(addr, bus)
        self.commands = Commands()
        self.flags = Flags()

        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(0x03)
        self.lcd_write(self.commands.RETURN_HOME)

        self.lcd_write(
            self.commands.FUNCTION_SET
            | self.flags.TWO_LINE
            | self.flags.FIVE_BY_SEVEN_DOTS
            | self.flags.FOUR_BIT_MODE
        )

        self.lcd_write(self.commands.DISPLAY_CONTROL | self.flags.DISPLAY_ON)
        self.lcd_write(self.commands.CLEAR_DISPLAY)
        self.lcd_write(self.commands.ENTRY_MODE_SET | self.flags.ENTRY_LEFT)

    def lcd_strobe(self, data):
        self.lcd_device.write_cmd(data | self.flags.En | self.flags.BACKLIGHT)
        time.sleep(0.0005)
        self.lcd_device.write_cmd(((data & ~self.flags.En) | self.flags.BACKLIGHT))
        time.sleep(0.0001)

    def lcd_write_four_bits(self, data):
        self.lcd_device.write_cmd(data | self.flags.BACKLIGHT)
        self.lcd_strobe(data)

    def lcd_write(self, cmd, mode=0):
        self.lcd_write_four_bits(mode | (cmd & 0xF0))
        self.lcd_write_four_bits(mode | ((cmd << 4) & 0xF0))

    def lcd_write_char(self, charvalue, mode=1):
        self.lcd_write_four_bits(mode | (charvalue & 0xF0))
        self.lcd_write_four_bits(mode | ((charvalue << 4) & 0xF0))

    def lcd_write_string(self, string, line):
        if line == 1:
            self.lcd_write(0x80)
        if line == 2:
            self.lcd_write(0xC0)
        if line == 3:
            self.lcd_write(0x94)
        if line == 4:
            self.lcd_write(0xD4)

        for char in string:
            self.lcd_write(ord(char), self.flags.Rs)

    def lcd_clear(self):
        self.lcd_write(self.commands.CLEAR_DISPLAY)
        self.lcd_write(self.commands.RETURN_HOME)

    def lcd_backlight(self, state):
        if state == 1:
            self.lcd_device.write_cmd(self.flags.BACKLIGHT)
        elif state == 0:
            self.lcd_device.write_cmd(self.flags.NO_BACKLIGHT)

    def lcd_load_custom_chars(self, fontdata):
        self.lcd_write(0x40)
        for char in fontdata:
            for line in char:
                self.lcd_write_char(line)
