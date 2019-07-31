import board
import time
from .device import Device
from .power import Battery


class System(Device):

    def __init__(self, interval=5.0, *args, **kwargs):

        Device.__init__(self, name="sys0", interval=interval, *args, **kwargs)

        import busio
        import board

        self.spi_bus = None
        try:
            self.spi_bus = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        except RuntimeError as e:
            print(e)
            print("SPI unavailable!")

        self.i2c_bus = None
        try:
            self.i2c_bus = busio.I2C(board.SCL, board.SDA)
        except RuntimeError as e:
            print(e)
            print("I2C unavailable!")

        if self.i2c_bus:
            self.enumerate_i2c()
            print("i2c hw addrs: {}".format(self.data["i2c_addrs"]))

        import gc
        self.free = gc.mem_free

        import microcontroller
        self.cpu = microcontroller.cpu

        self.data["cycles"] = 0

        self.battery = Battery()

    def read(self):
        # Remove introspection by setting `system.read = None` in `code.py`

        cyc_per_sec = self.data.get("cycles", 0) / self.interval
        self.data["cycles"] = 0

        # print("Cycles per sec: {}".format(cyc_per_sec))

        return {"cycles/sec": cyc_per_sec,
                "mem free": self.free(),
                "cpu temp":  self.cpu.temperature}

    def voltage(self):
        return self.battery.data.get("voltage")

    def uptime(self):

        seconds = time.monotonic()

        seconds_in_day = 86400
        seconds_in_hour = 3600
        seconds_in_minute = 60

        days = seconds // seconds_in_day
        seconds = seconds - (days * seconds_in_day)

        hours = seconds // seconds_in_hour
        seconds = seconds - (hours * seconds_in_hour)

        minutes = seconds // seconds_in_minute
        seconds = seconds - (minutes * seconds_in_minute)

        return "{:02}d:{:02}h:{:02}m:{:02}s".format(days, hours, minutes, int(seconds))

    def enumerate_i2c(self):

        while not self.i2c_bus.try_lock():
            pass

        self.data["i2c_addrs"] = [hex(x) for x in self.i2c_bus.scan()]

        self.i2c_bus.unlock()

    def run(self):
        while True:
            for device in Device.registry.values():
                device.poll()
            self.data["cycles"] += 1
