import time
import board
from device import *

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 10

SIREN_ACTIVE_PIN = board.A0
SIREN_SEL1_PIN = board.A1
SIREN_SEL2_PIN = board.A2

BUTTON_RT_PIN = board.BUTTON_A
BUTTON_LF_PIN = board.BUTTON_B
SWITCH_PIN = board.D7

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
# Create user input objects
# -------------------------------

lf_button = Button(BUTTON_LF_PIN, name="right")
rt_button = Button(BUTTON_RT_PIN, name="left-siren")
switch = Switch(SWITCH_PIN)

# -------------------------------
# Create the siren
# -------------------------------

siren = SirenIC(SIREN_ACTIVE_PIN, SIREN_SEL1_PIN, SIREN_SEL2_PIN)
from device.siren_ic import AlarmProfile
siren.data["profile"] = AlarmProfile.POLICE

def trigger_siren(self):
    siren.data["active"] = self.last_value


lf_button.callbacks.append(trigger_siren)


# -------------------------------
# Main loop
# -------------------------------

cpu = Microprocessor()

while True:
    current_time = time.monotonic()
    for device in Device.registry.values():
        device.poll()
    cpu.data["poll_time"] = time.monotonic() - current_time
