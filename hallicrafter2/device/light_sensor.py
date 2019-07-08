from .device import Device

class HDRLightSensor(Device):

    id = 0

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            name = "lth{}".format(HDRLightSensor.id)
        HDRLightSensor.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import adafruit_tsl2591
        from .i2c import i2c_bus
        self.sensor = adafruit_tsl2591.TSL2591(i2c_bus)

    def read(self):
        try:
            return {"lux": self.sensor.lux,
                    "visible": self.sensor.visible,
                    "infrared": self.sensor.infrared}
        except (OSError, RuntimeError) as e:
            print(e)

    # def render(self):
    #     print(self.data)


class LightSensor(Device):
    # delay can be as little as 0.1 sec

    id = 0

    def __init__(self, name=None, *args, **kwargs):
        if not name:
            name = "lit{}".format(LightSensor.id)
        LightSensor.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import adafruit_veml7700
        self.sensor = adafruit_veml7700.VEML7700(i2c_bus)

    def read(self):

        try:
            return {
                "light": self.sensor.light
            }
        except (OSError, RuntimeError) as e:
            print(e)
