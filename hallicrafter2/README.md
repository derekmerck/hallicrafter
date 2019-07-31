Hallicrafter Controller
=======================

Derek Merck
Summer 2019

CircuitPython interface controller for the Hallicrafter Smart Radio project.
  
Refactored for use on stand-alone microcontroller because the Neopixel control line and i2c bus create electronic interference on the Raspberry Pi audio DAC.

This code requires an M4 or better chip (ie, Feather M4, Metro M4) to use the OLED, but seems to work fine on an M0 otherwise.

Usage
-----------------------

Basic program that creates a single LED NeoPixel array (as on a Feather Mx) and cycles the color.

```.python
import board
from device import *
from device.led_strip import rgb_wheel_gen

sys = System()
led_strip  = LEDStrip(board.NEOPIXEL, 1, interval=0.01)

# Cycle colors
rgb_gen = rgb_wheel_gen()
def wheel_callback(self):
    self.fill(next(rgb_gen))
led_strip.callbacks.append(wheel_callback)

# -------------------------------
# Main loop
# -------------------------------

if __name__ == "__main__":
    sys.run()

```


Extending the Hallicrafter Device Library
-----------------------

Most classes are simple wrappers around Adafruit-provided libraries for their hardware.
  
New object classes may be easily added by providing `read`, and/or `write` functions to be executed at fixed intervals.  

Object _instances_ can be specialized by registering additional callback functions that will be executed between `read` and `write`, as in the sample shown above.


Serial Console
-----------------------

The serial console provides a basic key/value interface to any device's "data" kv registry.  The base "Device" class is designed to accept instructions from, read from, and write to it's private kv registry.

Intended usage is for a controller host to be able to periodically poll for input values or push UI output updates over the UART interface.

Note that the serial console implementation is _completely unsecured_.


Raspberry Pi UART
----------------------

1. Disable the Linux login terminal on serial in `raspi-config`
2. Add device-tree options to `/boot/config.txt`

```
enable_uart=1
dtoverlay=pi3-disable-bt
```

3. Reboot
4. Connect with `screen /dev/ttyAMA0 115200`


LoRa
----------------------

1. There is a bug in the single channel forwarder.  When a packet is received, the subprocess spits out both the packet data and a "gateway status update" message, which confuses the json parser.

Fix:

```.python
# read incoming packet info
pkt_json = proc.stdout.readline().decode('utf-8')

if pkt_json.endswith("gateway status update\n"):
   pkt_json = pkt_json[:-len("gateway status update\n")]
```

2. For packet creation, I use python's `struct` class.  There is an equivalent JavaScript port of the class available as `JSPack`.

As an example:

Encoded: `b'9CBC5F46FC877840BC077E445C5A823CEDB10D00F0AC5342A4A8C141'`

Decoded:
```.json
{
    "gas": 897517,
    "humidity": 52.91888427734375,
    "pressure": 1016.120849609375,
    "temperature": 24.20734405517578,
    "uptime": 14319.15234375,
    "uv": 0.01591222733259201,
    "voltage": 3.8832998275756836
}
```

Decoding with JSPack on TTN:

```javascript
// include functions from https://raw.githubusercontent.com/pgriess/node-jspack/master/jspack.js

function Decoder(bytes, port) {

  var p = new JSPack()
  var result = p.Unpack(">ffffiff", bytes);

  return {uptime: result[0],
          voltage: result[1],
          pressure: result[2],
          uv: result[3],
          gas: result[4],
          humidity: result[5],
          temperature: result[6]

  };
}
```