from .device import Device

SENSOR_UPDATE_INTERVAL = 5.0


class TempHumSensor(Device):

    def __init__(self, i2c_bus, name="sns_th0", interval=SENSOR_UPDATE_INTERVAL,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_am2320
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


class TempHumGasSensor(Device):

    def __init__(self, i2c_bus, name="sns_thg", interval=SENSOR_UPDATE_INTERVAL,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_bme680
        self.sensor = adafruit_bme680.Adafruit_BME680_I2C(i2c_bus)

    def read(self):
        try:
            return {
                "temperature": self.sensor.temperature,
                "humidity": self.sensor.humidity,
                "pressure": self.sensor.pressure,
                "gas": self.sensor.gas
            }
        except (OSError, RuntimeError) as e:
            print(e)


class UVLightSensor(Device):

    def __init__(self, i2c_bus, name="sns_uv0", interval=SENSOR_UPDATE_INTERVAL,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_veml6075
        self.sensor = adafruit_veml6075.VEML6075(i2c_bus, integration_time=100)

    def read(self):
        try:
            return {
                "uv_index": self.sensor.uv_index
            }
        except (OSError, RuntimeError) as e:
            print(e)


class HDRLightSensor(Device):

    id = 0

    def __init__(self, i2c_bus, name="sns_hdlt", interval=SENSOR_UPDATE_INTERVAL,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_tsl2591
        self.sensor = adafruit_tsl2591.TSL2591(i2c_bus)

    def read(self):
        try:
            return {
                "lux": self.sensor.lux,
                "visible": self.sensor.visible,
                "infrared": self.sensor.infrared
            }
        except (OSError, RuntimeError) as e:
            print(e)


class LightSensor(Device):
    # delay can be as little as 0.1 sec

    id = 0

    def __init__(self, i2c_bus, name="sns_lt0", interval=SENSOR_UPDATE_INTERVAL,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_veml7700
        self.sensor = adafruit_veml7700.VEML7700(i2c_bus)

    def read(self):

        try:
            return {
                "light": self.sensor.light
            }
        except (OSError, RuntimeError) as e:
            print(e)
