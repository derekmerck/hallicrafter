from .device import Device


class System(Device):

    def __init__(self, interval=5.0, *args, **kwargs):

        Device.__init__(self, name="sys0", interval=interval, *args, **kwargs)

        import busio
        import board

        self.spi_bus = None
        try:
            self.spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        except RuntimeError:
            print("SPI unavailable!")

        self.i2c_bus = None
        try:
            self.bus = busio.I2C(board.SCL, board.SDA)
        except RuntimeError:
            print("I2C unavailable!")

        if self.i2c_bus:
            self.enumerate_i2c()
            print("i2c hw addrs: {}".format(self.data["i2c_addrs"]))

        import gc
        self.free = gc.mem_free

        import microcontroller
        self.cpu = microcontroller.cpu

        self.data["cycles"] = 0

    def read(self):
        # Remove introspection by setting `system.read = None` in `code.py`

        cyc_per_sec = self.data.get("cycles", 0) / self.interval
        self.data["cycles"] = 0

        # print("Cycles per sec: {}".format(cyc_per_sec))

        return {"cycles/sec": cyc_per_sec,
                "mem free": self.free(),
                "cpu tmp":  self.cpu.temperature}

    def enumerate_i2c(self):

        while not self.bus.try_lock():
            pass

        self.data["i2c_addrs"] = [hex(x) for x in self.bus.scan()]

        self.bus.unlock()

    def run(self):
        while True:
            for device in Device.registry.values():
                device.poll()
            self.data["cycles"] += 1
