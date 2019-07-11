import time
import board
from device import Device, LEDStrip, OLEDPanel, AmpStereo20W, \
    HDRLightSensor, TempHumSensor, TempHumGasSensor, UVLightSensor, \
    Microprocessor, Memory, I2CBus, SPIBus, SerialIO

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 1
OLED_RESET_PIN = board.D9  # D6 is A1 on cpx
OLED_DIMS = (128, 64)


# -------------------------------
# Create sys objects
# -------------------------------

cpu = Microprocessor(interval=2.0)  # No need to update often
mem = Memory(interval=2.0)          # No need to update often
ser = SerialIO(interval=0.1)
# spi = SPIBus()
i2c = I2CBus()

# -------------------------------
# Create LED strip
# -------------------------------

led_strip  = LEDStrip(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.01)

from device.led_strip import rgb_wheel_gen
rgb_gen = rgb_wheel_gen(step=1)
def wheel_callback(self):
    self.fill(next(rgb_gen))
led_strip.callbacks.append(wheel_callback)


# -------------------------------
# Create sensors
# -------------------------------

lt_sensor = HDRLightSensor(i2c, interval=5)
uv_sensor = UVLightSensor(i2c, interval=5)
tmp_hum_sensor = TempHumSensor(i2c, interval=5)
tmp_hum_gas_sensor = TempHumGasSensor(i2c, interval=5)

# ir_sensor = AnalogInput(IR_DIODE_PIN, name="ird0", interval=0.001)
#
# last_hit_time = time.time()
# def detect_hit(self):
#
#     global last_hit_time
#     current_time = time.monotonic()
#     if self.input.value > 60000:
#         if not self.data.get("hit"):
#             if not self.data.get("num_hits"):
#                 self.data["num_hits"] = 0
#             self.data["num_hits"] += 1
#             print("Hit {}!".format(self.data["num_hits"]))
#         self.data["hit"] = True
#         last_hit_time = current_time
#     elif current_time > last_hit_time + 2.0:
#         self.data["hit"] = False
#
# ir_sensor.callbacks.append(detect_hit)

# -------------------------------
# Create the OLED panel
# -------------------------------

# This is _very_ slow - it blocks for 0.5 secs
oled_panel = OLEDPanel(i2c, OLED_DIMS, OLED_RESET_PIN, interval=4.0)

def read_sensors(self):
    self.data.update(uv_sensor.data)
    self.data.update(tmp_hum_gas_sensor.data)

    # self.data["cpu_t"] = cpu.data["temperature"]
    # self.data["poll_t"] = cpu.data.get("poll_t")
    # self.data["free_mem"] = mem.data.get("free")
    # self.data["num hits"] = ir_sensor.data.get("num_hits")
    # print(oled_panel.data)


oled_panel.callbacks.append(read_sensors)


# -------------------------------
# Main loop
# -------------------------------

while True:
    current_time = time.monotonic()
    for device in Device.registry.values():
        device.poll()
    polling_time = time.monotonic() - current_time
    cpu.data["poll_t"] = polling_time
