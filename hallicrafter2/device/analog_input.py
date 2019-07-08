from .device import Device


class AnalogInput(Device):

    id = 0

    def __init__(self, pin, name=None, *args, **kwargs):
        if not name:
            name = "ain{}".format(AnalogInput.id)
        AnalogInput.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import analogio
        self.input = analogio.AnalogIn(pin)

    def read(self):
        return {self.name: self.input.value}
