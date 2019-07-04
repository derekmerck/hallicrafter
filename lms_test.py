import logging
from hallicrafter.lms import LMSConnection

server_hostname = "boxwood"
player_name = "hallicrafter"

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)

    l = LMSConnection(server_hostname=server_hostname, player_name=player_name)

    l.update()
