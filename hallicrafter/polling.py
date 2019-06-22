from abc import ABC
import time
import attr


@attr.s
class Polling(ABC):

    delay = attr.ib(default=2.0)
    last_update = attr.ib(init=False, default=0)

    def update(self):

        tic = time.time()

        if tic > self.last_update + self.delay:
            self._update()
            self.last_update = tic

    def _update(self):
        raise NotImplementedError


@attr.s
class InputMixin(ABC):

    data = attr.ib(init=False)

    def get_data(self):
        return self.data


@attr.s
class RenderingMixin(ABC):

    buffer = attr.ib(init=False)

    def render(self):
        raise NotImplementedError
