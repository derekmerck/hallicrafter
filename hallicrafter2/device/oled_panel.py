from .device import Device
from .i2c import i2c_bus
import digitalio


class OLEDPanel(Device):

    def __init__(self, dims, reset_pin, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import adafruit_ssd1306
        pin = digitalio.DigitalInOut(reset_pin)
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            dims[0], dims[1],
            i2c_bus,
            reset=pin,
            addr=0x3d
        )

        self.fill(1)

    def fill(self, bw):
        self.oled.fill(bw)

    def render(self):
        self.oled.show()
