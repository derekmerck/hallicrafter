# Hallicrafter Controller v2

Derek Merck  
Summer 2019  

Design and application stack for "smart" multi-room audio server and players.


## Desiderata

### Music

- Wireless multiroom playback ([Logitech Media Server][])
- Minimal physical controls (volume, mute, skip)
- Sync'd back lighting
- Display title/artist info

[Logitech Media Server]: https://mysqueezebox.com/index/Home

### Sensor Data

- Temp
- Humidity
- Ambient light

### Room Activity Monitoring

- Still or video feed
- Minimal physical controls (privacy)

### Alexa/GHA Voice Monitoring

- Microphone


## Hardware

- Enclosure (old radios are good)
- Raspberry Pi 3/0 w WiFi ([Adafruit Pi Zero][], [Canakit Pi 3B+])
- Audio DAC ([Adafruit i2s bonnet][], [Pimaroni phat dac][], hifiberry or clone, usb dac)
- 15-20W audio amplifier ([Adafruit 20W amp][], [Drok 20W amp][])
- 1 or 2 15-20W audio drivers ([Adafruit 20W driver][], [Drok 15W driver][])
- 8-32 NeoPixels/WS2812B pixel strip ([Alitove 60px strip][])
- Diode (WS2812B strip requires slight voltage reduction to use RPi control line)
- 2-3x SPST switches (audio, backlight, camera)
- 1x pot/rotary encoder (volume)
- 12-20V psu (I use old laptop chargers)
- Buck converter/5V downstepper
- Small protoboard
- Small OLED ([Adafruit SSD1306][])
- Temp, humidity, lux sensors ([Adafruit][])
- Pi cam (optional, use w MotionEye, [Canakit official 8Mpx][], [Arducam 5Mpx][])
- Pi cam cable for Pi Zero (req for Pi Zero w cam, [iUniker Pi Zero cam cable][])
- USB microphone?

[Adafruit Zero]: https://www.adafruit.com/product/3708
[Canakit Pi 3B+]: https://www.canakit.com/raspberry-pi-3-model-b-plus.html

[Adafruit i2s bonnet]: https://www.adafruit.com/product/4037
[Pimaroni phat dac]: https://www.amazon.com/dp/B019U9VC9E/ref=cm_sw_em_r_mt_dp_U_CcdaDbH8AAQY2

[Adafruit 20+20W amp]: https://www.adafruit.com/product/1752
[Drok 15+15W amp]: https://www.amazon.com/dp/B077M526SB/ref=cm_sw_em_r_mt_dp_U_g8caDbHSD9BBQ

[Adafruit 20W driver]: https://www.adafruit.com/product/1732
[Drok 15W driver]: https://www.amazon.com/dp/B01IN8YI4Y/ref=cm_sw_em_r_mt_dp_U_3.caDbQBB57M0

[Alitove 60px strip]: https://www.amazon.com/gp/product/B01MG49QKD/

[Adafruit SSD1306]: https://www.adafruit.com/product/938

[Canakit official 8Mpx]: https://www.canakit.com/raspberry-pi-camera-v2-8mp.html
[Arducam 5Mpx]: https://www.amazon.com/Arducam-Megapixels-Sensor-OV5647-Raspberry/dp/B012V1HEP4

[iUniker Pi Zero cam cable]: https://www.amazon.com/Camera-Cable-iUniker-Raspberry-Ribbon/dp/B07H8Z4XLL/

## Notes:

- Requires SDA/SDC and 2 open pins (pixels, oled reset)
- Pixel pins have limited options

- Setting up squeezelite -- `raspi-config` -> boot -> wait for network


## Todo:

- lms connection (title, etc) pylms
- [cava][] -- bar vu data (drive leds)

- oled controller
- light detection

- cli version
- daemonize
- hab server

[cava]: https://github.com/karlstav/cava