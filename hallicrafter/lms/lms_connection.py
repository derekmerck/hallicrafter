import logging
from pprint import pprint, pformat
import attr
from pylms.server import Server
from pylms.player import Player

from ..polling import Polling, InputMixin


@attr.s
class LMSConnection(Polling, InputMixin):

    server_hostname = attr.ib(default=None)
    player_name = attr.ib(default=None)
    server_port = attr.ib(default=9090)

    server = attr.ib(init=False, type=Server)
    @server.default
    def connect_to_server(self):
        server = Server(hostname=self.server_hostname, port=self.server_port)
        server.connect()

        logger = logging.getLogger("LMS")
        logger.info("Logged in: %s" % server.logged_in)
        logger.info("Version: %s" % server.get_version())

        return server

    player = attr.ib(init=False, type=Player)
    @player.default
    def set_tracked_player(self):
        players = self.server.get_players()
        for p in players:
            if p.name == self.player_name:
                return p

    def _update(self):
        return {
            "name": self.player.get_name(),
            "mode": self.player.get_mode(),
            "connected": self.player.is_connected,
            "track_title": self.player.get_track_title(),
            "track_artist": self.player.get_track_artist(),
            "track_time": self.player.get_time_elapsed(),
            "track_remaining": self.player.get_time_remaining()
        }

