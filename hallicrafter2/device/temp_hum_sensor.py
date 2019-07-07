from .device import Device


class TempHumSensor(Device):

    def __init__(self, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)

        import adafruit_am2320
        from .i2c import i2c_bus
        self.sensor = adafruit_am2320.AM2320(i2c_bus)

        # Order is vdd, sda, gnd, scl (l->r, facing grid)

    def read(self):
        try:
            return {
                "temperature": self.sensor.temperature,
                "humidity": self.sensor.relative_humidity
            }
        except (OSError, RuntimeError) as e:
            print(e)

    # def render(self):
    #     print(self.data)
