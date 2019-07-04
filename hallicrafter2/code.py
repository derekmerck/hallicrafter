import time
import board
from device import Device, LEDStrip, HDRLightSensor, \
    TempHumSensor, Button, OLEDPanel

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 10
OLED_RESET_PIN = board.D6  # D6 is A1 on cpx
OLED_DIMS = (128,64)

# -------------------------------
# Create the led strip
# -------------------------------

# led_strip  = LEDStrip(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.1)
#
# from utils.rgb import rgb_wheel_gen as gen
# rgb_gen = gen(step=2)
# def wheel_callback():
#     led_strip.fill(next(rgb_gen))
#
# led_strip.callback = wheel_callback


# -------------------------------
# Create the button objects
# -------------------------------

# lf_button = Button(board.BUTTON_A)
#
# def lf_button_callback():
#     print("left button = {}".format(lf_button.button.value))
#
# lf_button.callback = lf_button_callback

# -------------------------------
# Create the sensor objects
# -------------------------------

# light_sensor = HDRLightSensor()
# temp_hum_sensor = TempHumSensor()

# -------------------------------
# Create the OLED panel
# -------------------------------

oled_panel = OLEDPanel(OLED_DIMS, OLED_RESET_PIN)

# -------------------------------
# Main loop
# -------------------------------

while True:
    for device in Device.registry:
        device.poll()
    time.sleep(0.01)
