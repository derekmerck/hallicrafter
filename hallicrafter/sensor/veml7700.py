import logging
from pprint import pprint, pformat
import adafruit_veml7700
import attr

from ..polling import Polling, InputMixin
from ..bus import i2c


@attr.s
class VEML7700Sensor(Polling, InputMixin):
    # delay can be as little as 0.1 sec

    light = attr.ib(init=False)

    hardware = attr.ib(init=False)
    @hardware.default
    def init_hardware(self):
        return adafruit_veml7700.VEML7700(i2c)

    def _update(self):

        try:
            self.light = self.hardware.light
            logging.info(pformat(self.get_data()))
        except OSError as e:
            logging.error(e)


