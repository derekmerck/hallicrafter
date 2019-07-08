import time
from .device import Device
import board
import json

_helpstr = \
"""
Hallicrafter Console
====================

Provides state inspection and manipulation for manager node.

Usage
-----
Terminate commands with ctrl-D (EOT)

input: `HELP`
result: Return this message

input: `PUT key value`
result: Return "OK" and set local.data[key] = value

input: `GET key {key key ...}`
result: Return "OK" and values stored at local.data[keys]
        as json if those keys exist
        
input: `DLIST`
result: Listing of all device names from Device.registry.keys()

input: `DPUT device key value`
result: Return "OK" and set device.data[key] = value

input: `DGET device {key key ...}`
result: Return "OK" and values stored at device.data[keys]
        as json if those keys exist

Any error conditions will return "NOK" and a brief 
explanation.\n
"""

_prompt = "> "


def mk_bytes(s):
    return bytearray(s.replace("\n", "\n\r") + _prompt)


class SerialIO(Device):

    id = 0

    def __init__(self, tx_pin=board.TX, rx_pin=board.RX,
                 baudrate=115200, tx_led=None, rx_led=None,
                 name=None, *args, **kwargs):
        if not name:
            name = "ser{}".format(SerialIO.id)
        SerialIO.id += 1
        Device.__init__(self, name=name, *args, **kwargs)

        import busio
        import digitalio

        self.tx_led = None
        if tx_led:
            self.tx_led = digitalio.DigitalInOut(tx_led)
            self.tx_led.direction = digitalio.Direction.OUTPUT

        self.rx_led = None
        if rx_led == tx_led:
            self.rx_led = self.tx_led
        elif rx_led:
            self.rx_led = digitalio.DigitalInOut(rx_led)
            self.rx_led.direction = digitalio.Direction.OUTPUT

        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=0)

        self.rx_buffer = ""
        self.rx_data = None

        self.tx_data = mk_bytes(_helpstr)

    def handle_rx(self):

        print("RX: " + self.rx_data)

        # Parse rx
        inst, *args = self.rx_data.rstrip().lstrip().split(" ")

        if inst == "HELP":
            response = "\nOK HELP\n"
            response += _helpstr

        elif inst == "PUT":
            key = args[0]
            value = " ".join(args[1:])
            response = "\nOK PUT {} = {}\n".format(key, value)
            self.data[key] = value

        elif inst == "GET":
            keys = args
            response = "\nOK GET {}\n".format(keys)
            result = {}
            for key in keys:
                if key in self.data.keys():
                    result[key] = self.data[key]
            result_str = json.dumps(result)
            response += result_str + "\n"

        elif inst == "DPUT":
            device_name = args[0]
            device = Device.registry.get(device_name)
            if not device:
                response = "\nNOK No such device {}\n".format(device_name)

            else:
                key = args[1]
                value = " ".join(args[2:]).rstrip()
                response = "\nOK PUT {}.{} = {}\n".format(device_name, key, value)
                device.data[key] = value

        elif inst == "DGET":
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

        elif inst == "DLIST":
            result = list(Device.registry.keys())
            result_str = json.dumps(result)
            response = "\nOK DLIST\n"
            response += result_str + "\n"

        else:
            response = "\nNOK Unknown command {}\n".format(inst)

        print("TX: " + response, end="")
        self.tx_data += mk_bytes(response)

    def read(self):
        data = self.uart.read(128)  # read up to 128 bytes

        if data:
            if self.rx_led:
                self.rx_led.value = True

            # convert bytearray to string and append to input
            self.rx_buffer += ''.join([chr(b) for b in data])
            # print(self.rx_buffer)
            self.tx_data = data  # Echo back to user

            if self.rx_led:
                self.rx_led.value = False

            if self.rx_buffer.endswith("\x04"):
                self.rx_data = self.rx_buffer[:-1]  # Throw out ctrl-D
                self.rx_buffer = ""
                self.handle_rx()

    def write(self):

        if self.tx_data:

            if self.tx_led:
                self.tx_led.value = True

            self.uart.write(self.tx_data)
            self.tx_data = None

            if self.tx_led:
                self.tx_led.value = False
