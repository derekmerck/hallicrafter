import board
from .device import Device

class Battery(Device):

    def __init__(self, name="bat0", interval=5.0, *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        try:
            import analogio
            self.voltage = analogio.AnalogIn(board.VOLTAGE_MONITOR)
        except:
            self.voltage = None
            print("Warning: No battery voltage available")

    def read(self):
        if self.voltage:
            val = self.voltage.value * 3.3 / 65536 * 2
            return {"voltage": val}
