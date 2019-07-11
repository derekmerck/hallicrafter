import time
import board
from device import *

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 1


# -------------------------------
# Create the led strip
# -------------------------------

led_strip  = LEDStrip(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.01)

from device.led_strip import rgb_wheel_gen
rgb_gen = rgb_wheel_gen(step=1)
def wheel_callback(self):
    self.fill(next(rgb_gen))
led_strip.callbacks.append(wheel_callback)


# -------------------------------
# Main loop
# -------------------------------

cpu = Microprocessor()

while True:
    current_time = time.monotonic()
    for device in Device.registry.values():
        device.poll()
    cpu.data["poll_time"] = time.monotonic() - current_time
