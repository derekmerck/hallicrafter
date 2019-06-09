from abc import ABC
import attr


@attr.s
class PixelRenderer(ABC):

    npixels = attr.ib()

    def update_state(self):
        return

    def render_pixel(self, i):
        raise NotImplementedError

