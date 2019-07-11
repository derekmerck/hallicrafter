import time
from .device import Device

INPUT_UPDATE_INTERVAL = 0.1


class DigitalInput(Device):

    def __init__(self, pin, name="in_d0", pull="DOWN", interval=INPUT_UPDATE_INTERVAL,
                 *args, **kwargs):
        # Pull UP for switch

        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import digitalio

        self.input = digitalio.DigitalInOut(pin)
        self.input.direction = digitalio.Direction.INPUT
        if pull == "UP":
            _pull = digitalio.Pull.UP
        else:
            _pull = digitalio.Pull.DOWN
        self.input.pull = _pull

        self.last_value = None

    def read(self):

        value = self.input.value

        if self.last_value is None or value != self.last_value:
            print("{}: {}".format(self.name, value))
        self.last_value = value

        return {self.name: self.last_value}


class AnalogInput(Device):

    def __init__(self, pin, name="in_a0", interval=INPUT_UPDATE_INTERVAL,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import analogio
        self.input = analogio.AnalogIn(pin)

    def read(self):
        return {self.name: self.input.value}


class ThresholdEventInput(AnalogInput):
    # High resolution event counter with a timeout

    def __init__(self, pin, threshold=60000, timeout=2.0,
                 name="in_te0", interval=0.01, *args, **kwargs):

        AnalogInput.__init__(pin, name=name, interval=interval, *args, **kwargs)

        self.event_last_time = 0
        self.event_threshold = threshold
        self.event_timeout = timeout

    def read(self):

        current_time = time.monotonic()
        if self.input.value > self.event_threshold:
            if not self.data.get("event"):
                if not self.data.get("num_events"):
                    self.data["num_events"] = 0
                self.data["num_events"] += 1
                print("Event {}!".format(self.data["num_events"]))
            self.data["event"] = True
            self.event_last_time = current_time
        elif current_time > self.event_last_time + self.event_timeout:
            self.data["event"] = False


class RotaryInput(Device):

    def __init__(self, pin_a, pin_b, pin_c=None, pull="DOWN",
                 name="in_r0", interval=INPUT_UPDATE_INTERVAL, *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import rotaryio
        self.encoder = rotaryio.IncrementalEncoder(pin_a, pin_b)
        self.last_position = None

        import digitalio
        self.input = digitalio.DigitalInOut(pin_c)
        self.input.direction = digitalio.Direction.INPUT
        if pull == "UP":
            _pull = digitalio.Pull.UP
        else:
            _pull = digitalio.Pull.DOWN
        self.input.pull = _pull

        self.last_value = None

    def read(self):

        position = self.encoder.position
        if self.last_position is None or position != self.last_position:
            print(position)
        self.last_position = position

        value = self.input.value
        if self.last_value is None or value != self.last_value:
            print("{}: {}".format(self.name, value))
        self.last_value = value

        return {self.name + "-val": self.last_value,
                self.name + "-pos": self.last_position}
