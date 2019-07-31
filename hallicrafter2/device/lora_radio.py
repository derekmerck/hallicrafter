#define RFM95_CS  10   // "B"
#define RFM95_RST 11   // "A"
#define RFM95_INT  6   // "D"

from .device import Device


class LoRaWanRadio(Device):

    def __init__(self, spi, cs_pin, reset_pin,
                 dev_addr, nwk_key, app_key, tx_led=None,
                 name="lrw0", interval=10.0, *args, **kwargs):

        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa
        import digitalio

        cs = digitalio.DigitalInOut(cs_pin)
        reset = digitalio.DigitalInOut(reset_pin)

        self.tx_led = tx_led
        if self.tx_led:
            self.tx_led = digitalio.DigitalInOut(tx_led)
            self.tx_led.direction = digitalio.Direction.OUTPUT

        ttn_config = TTN(dev_addr, nwk_key, app_key, country='US')
        # Suppose to be cs, irq, rst, ttn_config?
        self.lora = TinyLoRa(spi, cs, reset, ttn_config)

        self.data["tx_buffer"] = None

    def write(self):

        if self.tx_led:
            self.tx_led.value = True

        if self.data["tx_buffer"]:
            data = self.data["tx_buffer"]
            self.lora.send_data(data, len(data), self.lora.frame_counter)

            print("LORAWAN TX: {}".format(self.data["tx_buffer"]))
            self.data["tx_buffer"] = None

            self.lora.frame_counter += 1

        if self.tx_led:
            self.tx_led.value = False


class LoRaRadio(Device):

    def __init__(self, spi, cs_pin, reset_pin, tx_led=None ,
                 name="lra0", interval=10.0, *args, **kwargs):
        # tx_power may be 5-23 (default 13)

        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        from adafruit_rfm9x import RFM9x
        import digitalio

        cs = digitalio.DigitalInOut(cs_pin)
        reset = digitalio.DigitalInOut(reset_pin)

        self.tx_led = tx_led
        if self.tx_led:
            self.tx_led = digitalio.DigitalInOut(tx_led)
            self.tx_led.direction = digitalio.Direction.OUTPUT

        self.rfm9x = RFM9x(spi, cs, reset, 915.0)
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
