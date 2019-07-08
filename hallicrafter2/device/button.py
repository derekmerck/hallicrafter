from .device import Device


class Button(Device):

    id = 0

    def __init__(self, pin, name=None, *args, **kwargs):
        if not name:
            name = "but{}".format(Button.id)
        Button.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import digitalio
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.DOWN

    def read(self):
        return {self.name: self.button.value}
