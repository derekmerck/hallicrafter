import board
from .device import Device
try:
    import json
except ImportError:
    print("Failed to import JSON, KVConsole will fail")


class KVConsole(object):
    """
    Language definition for kv simple dev/k/v command set
    """

    _helpstr = \
"""
Hallicrafter KV Console
====================

Provides state inspection and manipulation.

Usage
-----
Terminate commands with ctrl-D (EOT)

input: `HELP`
result: Return this message

input: `LIST`
result: Listing of all device names from 
        Device.registry.keys()

input: `PUT device key value`
result: Set device.data[key] = value

input: `GET device {key key ...}`
result: Get values stored at device.data[keys]
        as json if those keys exist

Successful operations return "OK" and result.

Error conditions return "NOK" and error message.\n
"""

    _prompt = "> "

    @classmethod
    def handle_input(cls, msg):
        print("CONSOLE RX: " + msg)

        # Parse rx
        inst, *args = msg.rstrip().lstrip().split(" ")

        if inst == "HELP":
            response = "\nOK HELP\n"
            response += cls._helpstr

        elif inst == "PUT":
            device_name = args[0]
            device = Device.registry.get(device_name)
            if not device:
                response = "\nNOK No such device {}\n".format(device_name)
            else:
                key = args[1]
                value = " ".join(args[2:]).rstrip()
                response = "\nOK PUT {}.{} = {}\n".format(device_name, key, value)
                device.data[key] = value

        elif inst == "GET":
            device_name = args[0]
            device = Device.registry.get(device_name)
            if not device:
                response = "\nNOK No such device {}\n".format(device_name)
            else:
                keys = args[1:]
                response = "\nOK GET {}.{}\n".format(device_name, keys)
                result = {}
                for key in keys:
                    if key in device.data.keys():
                        result[key] = device.data[key]
                result_str = json.dumps(result)
                response += result_str + "\n"

        elif inst == "LIST":
            result = list(Device.registry.keys())
            result_str = json.dumps(result)
            response = "\nOK LIST\n"
            response += result_str + "\n"

        else:
            response = "\nNOK Unknown command {}\n".format(inst)

        print("CONSOLE TX: " + response, end="")
        return response + cls._prompt


class SerialIO(Device):

    def __init__(self, tx_pin=board.TX, rx_pin=board.RX,
                 baudrate=115200, tx_led=None, rx_led=None,
                 name="ser0", interval=0.1,
                 *args, **kwargs):
        Device.__init__(self, name=name, interval=interval, *args, **kwargs)

        import busio
        import digitalio

        self.tx_led = tx_led
        if self.tx_led:
            self.tx_led = digitalio.DigitalInOut(tx_led)
            self.tx_led.direction = digitalio.Direction.OUTPUT

        self.rx_led = None
        if self.rx_led and self.rx_led == tx_led:
            self.rx_led = self.tx_led
        elif self.rx_led:
            self.rx_led = digitalio.DigitalInOut(rx_led)
            self.rx_led.direction = digitalio.Direction.OUTPUT

        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=0)

        self.data["rx_buffer"] = ""
        self.data["tx_buffer"] = None  # Don't send _helpstr w/o connecting

        self.console = KVConsole()

    def read(self):

        data = self.uart.read(64)

        if data:
            if self.rx_led:
                self.rx_led.value = True

            # convert bytearray to string and append to input
            self.data["rx_buffer"] += ''.join([chr(b) for b in data])
            self.data["tx_buffer"] = data.decode()  # Echo back to user

            if self.rx_led:
                self.rx_led.value = False

            if self.data["rx_buffer"].endswith("\x04"):
                msg = self.data["rx_buffer"][:-1]  # Throw out ctrl-D
                self.data["rx_buffer"] = ""
                response = self.console.handle_input(msg)
                self.data["tx_buffer"] += response

    @staticmethod
    def mk_bytes(s):
        s = s.replace("\n", "\n\r")
        _s = s.encode()
        return _s

    def write(self):

        if self.data["tx_buffer"]:

            if self.tx_led:
                self.tx_led.value = True

            _bytes = SerialIO.mk_bytes(self.data["tx_buffer"])

            self.uart.write(_bytes)
            self.data["tx_buffer"] = None

            if self.tx_led:
                self.tx_led.value = False
