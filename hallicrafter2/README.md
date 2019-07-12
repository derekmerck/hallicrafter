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
