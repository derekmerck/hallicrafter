from .device import Device


class Microprocessor(Device):

    id = 0

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            name = "cpu{}".format(Microprocessor.id)
        Microprocessor.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import microcontroller
        self.cpu = microcontroller.cpu

    def read(self):

        return {"temperature": self.cpu.temperature}
