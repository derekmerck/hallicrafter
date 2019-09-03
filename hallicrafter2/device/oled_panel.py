from .device import Device


class OLEDPanel(Device):

    def __init__(self, i2c, dims, reset_pin=None, name="oled0",
                 interval=5.0, addr=0x3d, *args, **kwargs):

        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_ssd1306

        if reset_pin:
            import digitalio
            reset = digitalio.DigitalInOut(reset_pin)
        else:
            reset = None

        self.oled = adafruit_ssd1306.SSD1306_I2C(
            dims[0], dims[1],
            i2c.bus,
            reset=reset,
            addr=addr
        )

        self.fill(0)
        self.oled.text('Hallicrafter v2', 0, 0, 100)
        self.oled.text('Hello world', 0, 10, 100)

    def fill(self, bw):
        self.oled.fill(bw)

    def render_data(self):
        self.oled.fill(0)
        i = 0
        for k, v in self.data.items():
            self.oled.text("{:<6}: {}".format(k[0:6], v), 0, i*10, 100)
            i+=1

    def write(self):
        self.render_data()
        self.oled.show()
