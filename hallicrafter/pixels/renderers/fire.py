import random
import attr
from .pixel_renderer import PixelRenderer


def clamp(val, min_v, max_v):
    return max(min(val, max_v), min_v)


@attr.s
class FirePixelRenderer(PixelRenderer):

    cooling = attr.ib()
    @cooling.default
    def set_cooling(self):
        if self.npixels > 32:
            return 0.045
        elif self.npixels > 16:
            return 0.1
        else:
            return 0.15

    sparking = attr.ib(default=0.45)

    dir_mode = attr.ib(default=0)
    # direction (and symmetry) of fire
    #   one-sided:  0 - from head, 1 - from tail
    #   symmetric:  2 - from ends, 3 - from middle

    npixels_used = attr.ib(init=False)
    @npixels_used.default
    def set_npixels_used(self):
        if self.dir_mode < 2:  # pixelCount with respect to dirMode
            return self.npixels
        else:
            self.cooling += 0.04  # use a little more cooling to match
            return self.npixels // 2

    heat_state = attr.ib(init=False)
    @heat_state.default
    def init_heat_state(self):
        return [0] * self.npixels_used

    heat_pallet = attr.ib(init=False)

    @heat_pallet.default
    def init_heat_pallet(self):

        # create HeatColors 8-bit palette:  0x000000,
        # 0x330000, 0x660000, 0x990000, 0xCC0000, 0xFF0000,
        # 0xFF3300, 0xFF6600, 0xFF9900, 0xFFCC00, 0xFFFF00,
        # 0xFFFF33, 0xFFFF66, 0xFFFF99, 0xFFFFCC, 0xFFFFFF

        r = [0.0]*256
        g = [0.0]*256
        b = [0.0]*256

        for i in range(256):
            if i < 85:
                r[i] = (i / 85)
            else:
                r[i] = 1
            if i >= 85:
                if i < 170:
                    g[i] = ((i - 85) / 85)
                else:
                    g[i] = 1
            if i >= 170:
                b[i] = ((i - 170) / 85)

        return {"r": r,"g": g,"b": b}


    def update_state(self):

        # step 1:  cool down the entire strip
        for i in range(self.npixels_used):
            self.heat_state[i] -= random.random() * self.cooling

        # step 2:  carry heat 'up' the strip
        for i in range(self.npixels_used-1, 2, -1):
            self.heat_state[i] = (self.heat_state[i - 1] + self.heat_state[i - 2]
                                  + self.heat_state[i - 2]) / 3

        # step 3:  add sparks to the base of the flame
        if self.sparking > random.random():
            base = max(self.npixels_used//10, 2)
            i = random.randint(0,base)  # sparks form in first 10% of strip
            self.heat_state[i] = self.heat_state[i] + random.random() * 0.37 + 0.63
            # add a minimum amount of heat to the pixel

        for i in range(self.npixels_used):
            self.heat_state[i] = clamp(self.heat_state[i], 0, 1)


    def render_pixel(self, index):
        if self.dir_mode == 0:
            heat_index = clamp(self.heat_state[index] * 256, 0, 255)
        if self.dir_mode == 1:
            heat_index = clamp(self.heat_state[self.npixels_used - index - 1] * 256, 0, 255)
        if self.dir_mode == 2:
            if index < self.npixels_used:
                heat_index = clamp(self.heat_state[index] * 256, 0, 255)
            else:
                heat_index = clamp(self.heat_state[(2 * self.npixels_used) - index - 1] * 256, 0, 255)

        if self.dir_mode == 3:
            if index < self.npixels_used:
                heat_index = clamp(self.heat_state[self.npixels_used - index - 1] * 256, 0, 255)
            else:
                heat_index = clamp(self.heat_state[index - self.npixels_used] * 256, 0, 255)

        heat_index = int(heat_index)
        r = self.heat_pallet["r"][heat_index] * 255
        g = self.heat_pallet["g"][heat_index] * 255
        b = self.heat_pallet["b"][heat_index] * 255
        return int(r), int(g), int(b)


