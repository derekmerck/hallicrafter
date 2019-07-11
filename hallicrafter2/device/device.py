import time


class Device(object):

    registry = {}
    count = 0

    def __init__(self, interval=0.1, name=None, *args, **kwargs):
        self.name = name or "dev{}".format(self.count)
        Device.count += 1
        Device.registry[self.name] = self

        self.data = {}
        self.interval = interval
        self.last_update = 0.0  # Use w monotonic, i.e., secs since start
        self.callbacks = []

    def _update(self):
        try:
            result = self.read()
            if result:
                self.data.update(result)
        except NotImplementedError:
            pass

        for cb in self.callbacks:
            cb(self)

        try:
            self.write()
        except NotImplementedError:
            pass

    def poll(self):
        now = time.monotonic()
        if now >= self.last_update + self.interval:
            self._update()
            self.last_update = now

    def read(self):
        raise NotImplementedError

    def write(self):
        raise NotImplementedError
