from .device import Device

class LEDStrip(Device):

    def __init__(self, num_leds, name="led0", interval=0.01,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        self.pixels = None
        self.num_leds = num_leds

    def fill(self, rgb):
        self.pixels.fill(rgb)

    def write(self):
        # print("Rendering px strip with {} px".format(self.num_leds))
        self.pixels.show()


class DotStarLEDs(LEDStrip):

    def __init__(self, data_pin, clk_pin, num_leds, name="led0", interval=0.01,
                 *args, **kwargs):

        LEDStrip.__init__(self, num_leds, name=name, interval=interval, *args, **kwargs)

        from adafruit_dotstar import DotStar
        self.pixels = DotStar(data_pin, clk_pin, num_leds,
                               auto_write=True,
                               brightness=0.1)
        self.fill((0, 255, 128))


class NeopixelLEDs(LEDStrip):
    # Neopixels

    def __init__(self, ctrl_pin, num_leds, name="led0", interval=0.01,
                 *args, **kwargs):

        LEDStrip.__init__(self, num_leds, name=name, interval=interval, *args, **kwargs)

        from neopixel import NeoPixel
        self.pixels = NeoPixel(ctrl_pin, num_leds,
                               auto_write=True,
                               brightness=0.1)
        self.fill((0, 255, 128))


def rgb_wheel_gen(step=1):

    def rgb_from_wheel_pos(pos):
        # Input a value 0 to 255 to get a color value.
        # The colours are a transition r - g - b - back to r.
        if pos < 85:
            return (int(pos * 3), int(255 - (pos * 3)), 0)
        elif pos < 170:
            pos -= 85
            return (int(255 - (pos * 3)), 0, int(pos * 3))
        else:
            pos -= 170
            return (0, int(pos * 3), int(255 - pos * 3))

    i = 0
    while True:
        i += step
        i %= 256
        yield rgb_from_wheel_pos(i)
