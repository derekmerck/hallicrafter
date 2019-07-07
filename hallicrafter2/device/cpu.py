from .device import Device


class Microprocessor(Device):

    def __init__(self, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import microcontroller
        self.cpu = microcontroller.cpu

    def read(self):

        return {"temperature": self.cpu.temperature}
