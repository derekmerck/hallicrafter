import logging


class Mock():

    # board
    D4 = "D4"
    D12 = "D12"
    D18 = "D18"
    SCL = "SCL"
    SDA = "SDA"

    # busio
    @classmethod
    def I2C(cls, *args, **kwargs):
        pass

    # digitalio
    @classmethod
    def DigitalInOut(cls, *args, **kwargs):
        pass

    class Instance():
        def fill(self, *args, **kwargs):
            pass

        def show(self, *args, **kwargs):
            pass

        def pixel(self, *args, **kwargs):
            pass

        def image(self, *args, **kwargs):
            pass

        def update(self, *args, **kwargs):
            pass

        def __setitem__(self, k, v):
            pass

        temperature = "temperature"
        relative_humidity = "rel_hum"
        light = "light"

    @classmethod
    def SSD1306_I2C(cls, *args, **kwargs):
        logging.warning("Mocking OLED interface")
        return cls.Instance()

    @classmethod
    def NeoPixel(cls, *args, **kwargs):
        logging.warning("Mocking NeoPixel interface")
        return cls.Instance()

    @classmethod
    def AM2320(cls, *args, **kwargs):
        logging.warning("Mocking AM2320 interface")
        return cls.Instance()

    @classmethod
    def VEML7700(cls, *args, **kwargs):
        logging.warning("Mocking VEML770 interface")
        return cls.Instance()