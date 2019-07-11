#define RFM95_CS  10   // "B"
#define RFM95_RST 11   // "A"
#define RFM95_INT  6   // "D"

from .device import Device


class LoRaRadio(Device):

    def __init__(self, spi, cs_pin, reset_pin, tx_led=None ,
                 name="lra0", interval=10.0, *args, **kwargs):
        # tx_power may be 5-23 (default 13)

        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import adafruit_rfm9x
        import digitalio

        cs = digitalio.DigitalInOut(cs_pin)
        reset = digitalio.DigitalInOut(reset_pin)

        self.tx_led = tx_led
        if self.tx_led:
            self.tx_led = digitalio.DigitalInOut(tx_led)
            self.tx_led.direction = digitalio.Direction.OUTPUT

        self.rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)
        self.data["tx_buffer"] = None
        self.data["tx_power"] = None   # Default 13

    def write(self):

        if self.data.get("tx_power") and \
                self.data["tx_power"] != self.rfm9x.tx_power:
            self.rfm9x.tx_power = self.data["tx_power"]

        if self.tx_led:
            self.tx_led.value = True

        if self.data["tx_buffer"]:
            self.rfm9x.send(self.data["tx_buffer"])

            print("LORA TX: {}".format(self.data["tx_buffer"]))
            self.data["tx_buffer"] = None

        if self.tx_led:
            self.tx_led.value = False
