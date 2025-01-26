import board
import busio
import displayio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
import terminalio

class OLED:
    def __init__(self, width=128, height=64, i2c_address=0x3C, sda_pin=board.GP4, scl_pin=board.GP5):
        displayio.release_displays()
        i2c = busio.I2C(scl=scl_pin, sda=sda_pin)
        display_bus = displayio.I2CDisplay(i2c, device_address=i2c_address)
        self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=width, height=height)
        self.group = displayio.Group()
        self.display.root_group = self.group

    def clear(self):
        while len(self.group) > 0:
            self.group.pop()

    def print_text(self, text, x=0, y=32, font=terminalio.FONT, color=0xFFFFFF, scale=1):
        text_area = label.Label(font, text=text, color=color)
        scaled_group = displayio.Group(scale=scale)
        scaled_group.append(text_area)
        scaled_group.x = x
        scaled_group.y = y
        self.group.append(scaled_group)

    def update_text(self, text, x=0, y=32, font=terminalio.FONT, color=0xFFFFFF, scale=1):
        self.clear()
        self.print_text(text, x, y, font, color, scale)