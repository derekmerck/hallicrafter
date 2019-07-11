from .device import Device

class SPIBus(Device):

    def __init__(self, *args, **kwargs):

        Device.__init__(self, name="spi", *args, **kwargs)

        import busio
        import board

        self.bus = None
        try:
            busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        except RuntimeError:
            print("SPI unavailable!")


class I2CBus(Device):

    def __init__(self, *args, **kwargs):

        Device.__init__(self, name="i2c", *args, **kwargs)

        import busio
        import board

        self.bus = None
        try:
            self.bus = busio.I2C(board.SCL, board.SDA)
        except RuntimeError:
            print("I2C unavailable!")

        if self.bus:
            self.enumerate()
            print("i2c hw addrs: {}".format(self.data["addrs"]))

    def enumerate(self):

        while not self.bus.try_lock():
            pass

        self.data["addrs"] = [hex(x) for x in self.bus.scan()]

        self.bus.unlock()


class Memory(Device):

    id = 0

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            name = "mem{}".format(Memory.id)
        Memory.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import gc
        self.free = gc.mem_free

    def read(self):

        return {"free": self.free()}


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
