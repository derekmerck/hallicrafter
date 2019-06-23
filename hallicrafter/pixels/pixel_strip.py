import time
import attr
import logging

from ..drivers import board, neopixel
from .renderers import RainbowPixelRenderer, FirePixelRenderer

@attr.s
class PixelStrip(object):

    pin = attr.ib(default=board.D18)
    npixels = attr.ib(default=16)
    brightness = attr.ib(default=0.2)
    delay = attr.ib(default=0.05)

    pixels = attr.ib(init=False)
    @pixels.default
    def create_pixels(self):
        return neopixel.NeoPixel(self.pin, self.npixels, brightness=self.brightness, auto_write=False)

    renderer = attr.ib()
    @renderer.default
    def set_renderer(self):
        return RainbowPixelRenderer(npixels=self.npixels)

    last_update = attr.ib(init=False, default=0)

    def update(self):

        tic = time.time()

        if tic > self.last_update + self.delay:

            self.renderer.update_state()
            for i in range(0, self.npixels):
                self.pixels[i] = self.renderer.render_pixel(i)
            self.pixels.show()
            self.last_update = tic

        # logger = logging.getLogger("Pixels")
        # logger.debug("Updating")
