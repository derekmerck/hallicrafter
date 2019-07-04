from .device import Device
from .i2c import i2c_bus


class TempHumSensor(Device):

    def __init__(self, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import adafruit_am2320
        self.sensor = adafruit_am2320.AM2320(i2c_bus)

    def read(self):
        try:
            return {
                "temperature": self.sensor.temperature,
                "humidity": self.sensor.relative_humidity
            }
        except (OSError, RuntimeError) as e:
            print(e)

    def render(self):
        print(self.data)
