import logging
from pprint import pprint, pformat
import attr

from ..polling import Polling, InputMixin

from ..drivers import adafruit_am2320
from ..bus import i2c


@attr.s
class AM2320Sensor(Polling, InputMixin):
    # delay should be more than 2 secs

    hardware = attr.ib(init=False)
    @hardware.default
    def init_hardware(self):
        return adafruit_am2320.AM2320(i2c)

    def _update(self):

        try:
            self.data = {
                "temperature": self.hardware.temperature,
                "humidity": self.hardware.relative_humidity
            }
            logging.info(pformat(self.get_data()))
        except OSError as e:
            logging.error(e)


