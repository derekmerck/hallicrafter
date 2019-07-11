import board
from .device import Device
try:
    import json
except ImportError:
    try:
        import ujson as json
    except ImportError:
        pass


class SerialIO(Device):

    id = 0

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
    
        input: `LIST`
        result: Listing of all device names from 
                Device.registry.keys()
    
        input: `PUT device key value`
        result: Return "OK" and set device.data[key] = value
    
        input: `GET device {key key ...}`
        result: Return "OK" and values stored at device.data[keys]
                as json if those keys exist
    
        Any error conditions will return "NOK" and a brief 
        explanation.\n
        """

    _prompt = "> "

    @classmethod
    def mk_bytes(cls, s):
        return bytearray(s.replace("\n", "\n\r") + cls._prompt)

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
        self.tx_buffer = None  # Don't send _helpstr w/o connecting
    def read(self):

        data = self.uart.read(64)

        if data:
            if self.rx_led:
                self.rx_led.value = True

            # convert bytearray to string and append to input
            self.rx_buffer += ''.join([chr(b) for b in data])
            self.tx_buffer = data  # Echo back to user

            if self.rx_led:
                self.rx_led.value = False

            if self.rx_buffer.endswith("\x04"):
                msg = self.rx_buffer[:-1]  # Throw out ctrl-D
                self.rx_buffer = ""
                response = handle_message(msg)
                self.tx_buffer += SerialIO.mk_bytes(response)

    def write(self):

        if self.tx_buffer:

            if self.tx_led:
                self.tx_led.value = True

            self.uart.write(self.tx_buffer)
            self.tx_buffer = None

            if self.tx_led:
                self.tx_led.value = False


def handle_message(msg):
    """
    Override this function to handle a different syntax
    """

    print("RX: " + msg)

    # Parse rx
    inst, *args = msg.rstrip().lstrip().split(" ")

    if inst == "HELP":
        response = "\nOK HELP\n"
        response += SerialIO._helpstr

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

    print("TX: " + response, end="")
    return response
