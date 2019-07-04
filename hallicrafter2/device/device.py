import time


class Device(object):

    registry = []

    def __init__(self, interval=1, *args, **kwargs):
        self.data = {}
        self.interval = interval
        self.last_update = time.time()
        Device.registry.append(self)

    def _update(self, *args, **kwargs):
        try:
            self.data = self.read()
        except NotImplementedError:
            pass

        try:
            self.callback()
        except NotImplementedError:
            pass

        try:
            self.render()
        except NotImplementedError:
            pass

    def poll(self):
        now = time.time()
        if now >= self.last_update + self.interval:
            self._update()
            self.last_update = now

    def read(self):
        raise NotImplementedError

    def callback(self):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

