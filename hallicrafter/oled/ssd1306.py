import time
import attr
from PIL import Image, ImageDraw, ImageFont

from ..drivers import board, digitalio, adafruit_ssd1306, sysinfo
from ..bus import i2c

# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

@attr.s
class OLED(object):

    hardware = attr.ib(init=False)
    delay = attr.ib(default=0.1)
    width = attr.ib(default=128)
    height = attr.ib(default=64)

    buffer = attr.ib(init=False)
    @buffer.default
    def make_buffer(self):
        return Image.new('1', (self.width, self.height))

    font = attr.ib(init=False, factory=ImageFont.load_default)

    def update(self):

        tic = time.time()

        if tic > self.last_update + self.delay:
            self.update_buffer()
            self.hardware.show()
            self.last_update = tic

    def update_buffer(self):
        raise NotImplementedError

    def put_text(self, text):
        raise NotImplementedError


@attr.s
class SSD1306(OLED):

    reset_pin = attr.ib(default=board.D4)

    hardware = attr.ib(init=False)
    @hardware.default
    def init_hardware(self):
        pin = digitalio.DigitalInOut(self.reset_pin)
        hw = adafruit_ssd1306.SSD1306_I2C(self.width, self.height, i2c, reset=pin, addr=0x3d)
        hw.fill(0)
        hw.show()
        return hw

    def test(self):

        self.hardware.fill(0)
        self.hardware.show()

        # Set a pixel in the origin 0,0 position.
        self.hardware.pixel(0, 0, 1)
        # Set a pixel in the middle 64, 16 position.
        self.hardware.pixel(64, 31, 1)
        # Set a pixel in the opposite 127, 31 position.
        self.hardware.pixel(127, 63, 1)
        self.hardware.show()


    def stats(self):

        info = sysinfo()

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(self.buffer)

        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        draw.text((0, 0),  info["ip"],   font=self.font, fill=255)
        draw.text((0, 8),  info["cpu"],  font=self.font, fill=255)
        draw.text((0, 16), info["mem"],  font=self.font, fill=255)
        draw.text((0, 25), info["disk"], font=self.font, fill=255)

        self.buffer = self.buffer.rotate(180)

        # Display image.
        self.hardware.image(self.buffer)
        self.hardware.show()