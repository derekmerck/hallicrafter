import time
import board
from device import *

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 1
OLED_RESET_PIN = board.D9  # D6 is A1 on cpx
OLED_DIMS = (128, 64)


# -------------------------------
# Create sys objects
# -------------------------------

sys = System()

LORA_CS_PIN = board.D10
LORA_RESET_PIN = board.D11
lora = LoRaRadio(sys.spi_bus, LORA_CS_PIN, LORA_RESET_PIN)

lora.tx_buffer = "Hello world!"


ser = SerialIO()

# -------------------------------
# Create LED strip
# -------------------------------

led_strip  = LEDStrip(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.01)

from device.led_strip import rgb_wheel_gen
rgb_gen = rgb_wheel_gen(step=1)

def wheel_callback(self):
    self.fill(next(rgb_gen))

led_strip.callbacks.append(wheel_callback)

#
# # -------------------------------
# # Create sensors
# # -------------------------------
#
# lt_sensor = HDRLightSensor(sys.i2c_bus)
# uv_sensor = UVLightSensor(sys.i2c_bus)
# tmp_hum_sensor = TempHumSensor(sys.i2c_bus)
# tmp_hum_gas_sensor = TempHumGasSensor(sys.i2c_bus)
#
# IR_DIODE_PIN = board.D6
# ir_sensor = ThresholdEventInput(IR_DIODE_PIN, name="ir_diode0",
#                                 threshold=60000, timeout=2.0, interval=0.01)
#
#
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

while True:
    for device in Device.registry.values():
        device.poll()
    sys.data["cycles"] += 1
