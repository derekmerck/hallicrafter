import logging
from pprint import pprint, pformat
from .sensor import Sensor
import adafruit_veml7700
import attr

from ..bus import i2c


@attr.s
class VEML7700Sensor(Sensor):
    # delay can be as little as 0.1 sec

    light = attr.ib(init=False)

    hardware = attr.ib(init=False)
    @hardware.default
    def init_hardware(self):
        return adafruit_veml7700.VEML7700(i2c)

    def poll_hardware(self):

        try:
            self.light = self.hardware.light
            logging.info(pformat(self.get_data()))
        except OSError as e:
            logging.error(e)

    def get_data(self):
        return {
            "light": self.light
        }

