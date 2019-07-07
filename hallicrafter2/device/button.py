from .device import Device


class Button(Device):

    def __init__(self, pin, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import digitalio
        self.button = digitalio.DigitalInOut(pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.DOWN

    def read(self):
        return {self.name: self.button.value}
