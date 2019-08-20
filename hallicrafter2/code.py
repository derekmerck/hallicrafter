import board
from device import *
from device.led_strip import rgb_wheel_gen

# Hallicrafter v4 pinout

STATION_NAME = "PANASONIC"

LED_INDICATOR_CLK_PIN  = board.APA102_SCK
LED_INDICATOR_CTRL_PIN = board.APA102_MOSI

LED_STRIP_CTRL_PIN = board.D5  # ItsyBitsy 5v logic
LED_STRIP_NUM_LEDS = 20        # station specific

VOL_0_PIN = board.D12
VOL_1_PIN = board.D11
VOL_MUTE_PIN  = board.D4
VOL_MUTE_PIN_PULL = "UP"
VOL_INIT  = 24

AMP_MUTE_PIN = board.D9

# Feather proto pinout

# LED_INDICATOR_CTRL_PIN = board.NEOPIXEL


# -------------------------------
# Create sys objects
# -------------------------------

sys = System()
ser = SerialIO()


# -------------------------------
# Create LED strip
# -------------------------------

dotstar = DotStarLEDs(LED_INDICATOR_CLK_PIN,
                      LED_INDICATOR_CTRL_PIN, 1, interval=0.01)

rgb_wheel0 = rgb_wheel_gen(step=1)

def wheel0_callback(self):
    self.fill(next(rgb_wheel0))

dotstar.callbacks.append(wheel0_callback)

npx = NeopixelLEDs(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.01, name="led1")

rgb_wheel = rgb_wheel_gen(step=1)

def wheel_callback(self):
    self.fill(next(rgb_wheel))

npx.callbacks.append(wheel_callback)


# -------------------------------
# Create UI
# -------------------------------

# Pull UP if complemented with ground
vol = RotaryInput(VOL_0_PIN, VOL_1_PIN, VOL_MUTE_PIN,
                  pull=VOL_MUTE_PIN_PULL, name="vol")


# -------------------------------
# Create amp controller and subscribe to vol
# -------------------------------

amp = AmpStereo20W(sys.i2c_bus, mute_pin=AMP_MUTE_PIN)
# amp.data["volume"] = VOL_INIT

vol.pressed = False
vol.pos = 0

def set_vol(self):
    # This should really be a partial function

    if self.last_position > self.pos:
        amp.data["incr"] = self.last_position - self.pos
    elif self.last_position < self.pos:
        amp.data["decr"] = self.pos - self.last_position
    self.pos = self.last_position

    if not self.pressed and self.last_value:     # newly pressed
        self.pressed = True
        amp.data["mute"] = not amp.data.get("mute", False)
        print("Mute: {}".format(amp.data.get("mute")))
    elif self.pressed and not self.last_value:   # newly released
        self.pressed = False

vol.callbacks.append(set_vol)


# -------------------------------
# Create sensors
# -------------------------------

tmp_hum_sensor = TempHumSensor(sys.i2c_bus)

def print_data(self):
    print(self.data)

tmp_hum_sensor.callbacks.append(print_data)


# # -------------------------------
# # Create the OLED panel
# # -------------------------------
#
# # This is _very_ slow - it blocks for 0.5 secs
# oled_panel = OLEDPanel(sys.i2c_bus, OLED_DIMS, OLED_RESET_PIN, interval=5.0)
#
#
# def read_sensors(self):
#     self.data.update(uv_sensor.data)
#     self.data.update(tmp_hum_gas_sensor.data)
#
#     # self.data["cpu_t"] = cpu.data["temperature"]
#     # self.data["poll_t"] = cpu.data.get("poll_t")
#     # self.data["free_mem"] = mem.data.get("free")
#     # self.data["num hits"] = ir_sensor.data.get("num_hits")
#     # print(oled_panel.data)
#
# oled_panel.callbacks.append(read_sensors)


# -------------------------------
# Main loop
# -------------------------------

if __name__ == "__main__":

    sys.run()
