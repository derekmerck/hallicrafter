from abc import ABC
import attr
from .pixel_renderer import PixelRenderer


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return r, g, b


@attr.s
class RainbowPixelRenderer(PixelRenderer):

    j = attr.ib(init=False, default=0)

    def update_state(self):
        # print("Updating")
        self.j += 1

    def render_pixel(self, i):

        # Map 1-4 -> 0-256 -> (0-256 + offset) % 255
        pixel_index = ( (i * 256 // self.npixels) + self.j ) % 255
        # print(pixel_index)
        return wheel(pixel_index & 255)
