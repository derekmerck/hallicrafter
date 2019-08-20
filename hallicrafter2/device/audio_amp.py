from .device import Device

class AmpStereo20W(Device):

    def __init__(self, i2c_bus, mute_pin=None, name="amp0", interval=0.1, *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_max9744
        self.amp = adafruit_max9744.MAX9744(i2c_bus)

        self.amp.volume = 0

        self.mute = None
        if mute_pin:

            import digitalio

            self.mute = digitalio.DigitalInOut(mute_pin)
            self.mute.direction = digitalio.Direction.OUTPUT

    def write(self):

        if self.data.get("incr"):
            for i in range(self.data["incr"]):
                self.amp.volume_up()
            self.data["incr"] = 0

        elif self.data.get("decr"):
            for i in range(self.data["decr"]):
                self.amp.volume_down()
            self.data["decr"] = 0

        elif self.data.get("volume"):
            self.amp.volume = self.data["volume"]
            # self.data["volume"] = None

        if self.mute:
            self.mute.value = self.data.get("mute")
