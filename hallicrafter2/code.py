import time
import board
from device import Device, LEDStrip, Microprocessor, \
    OLEDPanel, HDRLightSensor, TempHumSensor, Button, \
    AnalogInput, SerialIO

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 1
LED_STRIP2_CTRL_PIN = board.A5
LED_STRIP2_NUM_LEDS = 24
OLED_RESET_PIN = board.D9  # D6 is A1 on cpx
OLED_DIMS = (128,64)
IR_DIODE_PIN = board.A0


# -------------------------------
# Create the led strip
# -------------------------------

led_strip  = LEDStrip(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.01)

from utils.rgb import rgb_wheel_gen as gen
rgb_gen = gen(step=1)
def wheel_callback(self):
    self.fill(next(rgb_gen))
led_strip.callbacks.append(wheel_callback)

#
# led_strip2  = LEDStrip(LED_STRIP2_CTRL_PIN, LED_STRIP2_NUM_LEDS, interval=0.1)
#
# def wheel_callback2():
#     led_strip2.fill(next(rgb_gen))
# led_strip2.callback = wheel_callback2

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

light_sensor = HDRLightSensor(interval=5)
temp_hum_sensor = TempHumSensor(interval=5)

ir_sensor = AnalogInput(IR_DIODE_PIN, name="ird0", interval=0.001)

last_hit_time = time.time()
def detect_hit(self):

    global last_hit_time
    current_time = time.monotonic()
    if self.input.value > 60000:
        if not self.data.get("hit"):
            print("Hit!")
            if not self.data.get("num_hits"):
                self.data["num_hits"] = 0
            self.data["num_hits"] += 1
        self.data["hit"] = True
        last_hit_time = current_time
    elif current_time > last_hit_time + 2.0:
        self.data["hit"] = False

ir_sensor.callbacks.append(detect_hit)

# -------------------------------
# Create the OLED panel
# -------------------------------

# This is _very_ slow (0.5 secs), don't update more than 1/sec
oled_panel = OLEDPanel(OLED_DIMS, OLED_RESET_PIN, interval=5.0)

def read_sensors(self):
    # self.data.update(light_sensor.data)
    # self.data.update(temp_hum_sensor.data)
    self.data["cpu temp"] = cpu.data["temperature"]
    self.data["num hits"] = ir_sensor.data.get("num_hits")
    # print(oled_panel.data)

oled_panel.callbacks.append(read_sensors)

cpu = Microprocessor()

ser = SerialIO(interval=0.1)


# -------------------------------
# Main loop
# -------------------------------

while True:
    current_time = time.monotonic()
    for device in Device.registry.values():
        device.poll()
    polling_time = time.monotonic() - current_time
    oled_panel.data["poll tm"] = polling_time
