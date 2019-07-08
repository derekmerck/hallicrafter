from .device import Device


class OLEDPanel(Device):

    id = 0

    def __init__(self, dims, reset_pin, name=None, *args, **kwargs):
        if not name:
            name = "olp{}".format(OLEDPanel.id)
        OLEDPanel.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import adafruit_ssd1306
        from .i2c import i2c_bus
        import digitalio
        pin = digitalio.DigitalInOut(reset_pin)
        self.oled = adafruit_ssd1306.SSD1306_I2C(
            dims[0], dims[1],
            i2c_bus,
            reset=pin,
            addr=0x3d
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