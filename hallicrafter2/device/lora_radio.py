#define RFM95_CS  10   // "B"
#define RFM95_RST 11   // "A"
#define RFM95_INT  6   // "D"

from .device import Device

class LoRa(Device):

    id = 0

    def __init__(self, spi, cs_pin, rst_pin, name=None, *args, **kwargs):
        # tx_power may be 5-23 (default 13)

        if not name:
            name = "lra{}".format(LoRa.id)
        LoRa.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import adafruit_rfm9x
        import digitalio

        cs = digitalio.DigitalInOut(board.D5)
        reset = digitalio.DigitalInOut(board.D6)

        self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs_pin, rst_pin, 915.0)
        self.tx_buffer = None
        self.data["tx_power"] = None # Default 13
        self.data["rssi"] = None


    # def read(self):
    #
    #     msg = self.rfm9x.receive()
    #     if msg:
    #         self.rx_buffer = msg
    #         self.data["rssi] = self.rfm9x.rssi

    # Print out some chip state:
    # print('Temperature: {0}C'.format(rfm69.temperature))
    # print('Frequency: {0}mhz'.format(rfm69.frequency_mhz))
    # print('Bit rate: {0}kbit/s'.format(rfm69.bitrate / 1000))
    # print('Frequency deviation: {0}hz'.format(rfm69.frequency_deviation))

    def write(self):

        if self.data.get("tx_power") and \
                self.data["tx_power"] != self.rfm9x.tx_power:
            self.rfm9x.tx_power = self.data["tx_power"]

        if self.tx_buffer:
            self.rfm9x.send(self.tx_buffer)
