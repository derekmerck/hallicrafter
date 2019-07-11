from .device import Device

class AmpStereo20W(Device):

    def __init__(self, i2c, name="amp0", interval=0.1, *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_max9744
        self.amp = adafruit_max9744.MAX9744(i2c.bus)

        self.amp.volume = 0

    def write(self):

        if self.data.get("incr"):
            for i in range(self.data["incr"]):
                self.amp.volume_up()
            self.data["incr"] = 0

        elif self.data.get("decr"):
            for i in range(self.data["decr"]):
                self.amp.volume_down()
            self.data["incr"] = 0

        elif self.data.get("volume"):
            self.amp.volume = self.data["volume"]
