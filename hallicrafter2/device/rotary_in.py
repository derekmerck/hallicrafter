from .device import Device


class RotaryInput(Device):

    count = 0

    def __init__(self, pin_a, pin_b, pin_c=None, name=None, *args, **kwargs):
        if not name:
            name = "rot{}".format(RotaryInput.count)
        RotaryInput.count += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import rotaryio
        self.encoder = rotaryio.IncrementalEncoder(pin_a, pin_b)

        self.last_position = None

    def read(self):

        position = self.encoder.position

        if self.last_position is None or position != self.last_position:
            print(position)
        self.last_position = position

        return {self.name: self.last_position}

