import logging
from time import sleep
import board
from hallicrafter.pixels import PixelStrip
from hallicrafter.pixels.renderers import FirePixelRenderer, RainbowPixelRenderer
from hallicrafter.sensor import AM2320Sensor, VEML7700Sensor
from hallicrafter.oled import SSD1306

"""
config:
  host: hallicrafter
  
  services:
    lms_connection:
      driver: LMSConnection
      server_hostname: boxwood
      player_name: hallicrafter
      update: 5

    backlight: 
      driver: NeoPixels
      num_pixels: 33
      data_pin:  board.D12
      
    light_sensor:
      driver: veml770
      update: 0.1

    temp_hum_sensor:
      driver: am2320
      update: 3
      
    oled_display:
      driver: ssd1306
      size: [128,64]
      reset_pin: board.D4
      
"""

pixel_pin = board.D12
npixels = 33
oled_reset_pin = board.D4

has_oled = True
oled_size = [128,64]

loop_delay = 0.01


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Hallicrafter Controller")
    logging.info("-----------------------")

    renderer = RainbowPixelRenderer(npixels=npixels)
    pixels = PixelStrip(pin=pixel_pin, npixels=npixels)
    temp_hum_sensor = AM2320Sensor(delay=3)
    light_sensor = VEML7700Sensor(delay=0.5)
    oled = SSD1306()

    oled.test()

    while True:

        pixels.update()
        temp_hum_sensor.update()
        light_sensor.update()
        oled.stats()

        sleep(loop_delay)

