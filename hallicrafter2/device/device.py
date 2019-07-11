import time


class Device(object):

    registry = {}

    def __init__(self, name, interval=0.1, *args, **kwargs):
        self.name = name
        self.data = {}
        self.interval = interval
        self.last_update = 0.0  # Use w monotonic, i.e., secs since start
        self.callbacks = []

        Device.register(self)

    @classmethod
    def register(cls, item):
        if item.name in cls.registry.keys():
            raise ValueError("Duplicate device name found in registry: {}".format(item.name))
        cls.registry[item.name] = item

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
