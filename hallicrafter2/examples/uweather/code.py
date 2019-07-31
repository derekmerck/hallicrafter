import board
from device import *
# import json
import time

STATION_NAME = "UWEATHER_01"

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 1

LORA_CS_PIN = board.D10
LORA_RESET_PIN = board.D11


# -------------------------------
# Create sys objects
# -------------------------------

sys = System()
# ser = SerialIO()

npx = LEDStrip(board.NEOPIXEL, 1)
npx.fill((0,255,0))


# -------------------------------
# Create the LoRa radio
# -------------------------------

# Simple LoRa radio:

# lora = LoRaRadio(sys.spi_bus, LORA_CS_PIN, LORA_RESET_PIN, interval=5.0)
# lora.data["tx_buffer"] = "Hello world!"

# LoRaWan/TTN radio:

# Copy from TTN, should look like this:
# dev_addr  = b'\x00\x00\x00\x00'
# nwk_key   = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
# app_key   = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

from secrets import dev_addr, nwk_key, app_key

lora = LoRaWanRadio(sys.spi_bus, LORA_CS_PIN, LORA_RESET_PIN,
                    dev_addr, nwk_key, app_key, interval=120.0)


# -------------------------------
# Create sensors
# -------------------------------

uv_sensor = UVLightSensor(sys.i2c_bus, interval=30.0)
tmp_hum_gas_sensor = TempHumGasSensor(sys.i2c_bus, interval=30.0)


# -------------------------------
# Create callbacks
# -------------------------------

def submit_data(self):
    for k,v in self.data.items():
        # print("{}: {}".format(k,v))

        if not lora.data.get("sensors"):
            lora.data["sensors"] = {}
        lora.data["sensors"][k] = v

uv_sensor.callbacks.append(submit_data)
tmp_hum_gas_sensor.callbacks.append(submit_data)


# def format_sensor_data(self):
#     # Data can be pushed as JSON for standard radio messages
#
#     npx.fill((128,64,255))
#
#     packet_data = {"station": STATION_NAME,
#                    "uptime": sys.uptime(),
#                    "battery": sys.voltage(),
#                    "sensors": self.data.get("sensors")}
#
#     self.data["tx_buffer"] = json.dumps(packet_data)
#
#     time.sleep(1.0)  # Show the pixel color
#     npx.fill((0,255,0))

# lora.callbacks.append(format_sensor_data)


def ttn_encode_sensor_data(self):
    # Data must be packed to bytes for TTN, see README for decoding

    npx.fill((128,64,255))

    if self.data.get("sensors"):
        sensors = self.data.get("sensors")

        import struct
        packet_data = struct.pack(">ffffiff",
                        time.monotonic(),
                        sys.voltage(),
                        sensors.get("pressure", -1),
                        sensors.get("uv_index", -1),
                        sensors.get("gas", -1),
                        sensors.get("humidity", -1),
                        sensors.get("temperature", -1))

        self.data["tx_buffer"] = packet_data

    time.sleep(1.0)  # Show the pixel color
    npx.fill((0, 255, 0))


lora.callbacks.append(ttn_encode_sensor_data)


# -------------------------------
# Main loop
# -------------------------------

if __name__ == "__main__":

    sys.run()
