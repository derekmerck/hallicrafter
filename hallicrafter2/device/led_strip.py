from .device import Device


class LEDStrip(Device):

    id = 0

    def __init__(self, ctrl_pin, num_leds, name=None, *args, **kwargs):
        if not name:
            name = "led{}".format(LEDStrip.id)
        LEDStrip.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

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
