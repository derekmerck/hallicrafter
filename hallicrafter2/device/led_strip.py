from .device import Device


class LEDStrip(Device):

    def __init__(self, ctrl_pin, num_leds, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import neopixel
        self.pixels = neopixel.NeoPixel(ctrl_pin, num_leds,
                                        auto_write=True,
                                        brightness=0.1)

        self.fill((0, 255, 128))
        self.num_leds = num_leds

    def fill(self, rgb):
        self.pixels.fill(rgb)

    def write(self):
        # print("Rendering px strip with {} px".format(self.num_leds))
        self.pixels.show()
