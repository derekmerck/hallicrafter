from .device import Device

class AmpStereo20W(Device):

    id = 0

    def __init__(self, i2c, name=None, *args, **kwargs):
        if not name:
            name = "amp{}".format(AmpStereo20W.id)
        AmpStereo20W.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

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
