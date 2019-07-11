from .device import Device


class Button(Device):

    id = 0

    def __init__(self, pin, name=None, *args, **kwargs):
        if not name:
            name = "but{}".format(Button.id)
        Button.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import digitalio
        self.input = digitalio.DigitalInOut(pin)
        self.input.direction = digitalio.Direction.INPUT
        self.input.pull = digitalio.Pull.DOWN

        self.last_value = None

    def read(self):

        value = self.input.value

        if self.last_value is None or value != self.last_value:
            print("{}: {}".format(self.name, value))
        self.last_value = value

        return {self.name: self.last_value}


class Switch(Button):

    def __init__(self, pin, name=None, *args, **kwargs):
        if not name:
            name = "swt{}".format(Button.id)
        Button.id += 1
        Button.__init__(self, name=name, *args, **kwargs)

        import digitalio
        self.input.pull = digitalio.Pull.UP
