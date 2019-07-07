from .device import Device


class AnalogInput(Device):

    def __init__(self, pin, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import analogio
        self.input = analogio.AnalogIn(pin)

    def read(self):
        return {self.name: self.input.value}
