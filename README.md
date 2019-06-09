# Hallicrafter Controller v2


## Desiderata

### Music

- Wireless multiroom playback (LMS)
- Minimal controls (volume, mute, skip)
- Sync'd back lighting
- Title/artist info

### Sensor Data

- Temp
- Humidity
- Ambient light

### Room Activity Monitoring

- Still or video feed
- Minimal controls (privacy)

### Alexa/GHA Voice Monitoring

- Microphone


## Hardware

- Enclosure (old radios are good)
- Raspberry Pi 3/0 w WiFi
- Audio DAC (adafruit i2s, hifiberry clone, usb dac)
- Amp (5-20W)
- 1 or 2 5-20W speakers
- 8-32 NeoPixels/WS2812B pixel strip
- 2-3x SPST switches (audio, backlight, camera)
- 1x pot/rotary encoder (volume)
- 12-20V psu
- Buck converter/5V downstepper
- Small protoboard
- Small OLED (SSD1306)
- Temp, humidity sensor ()
- Pi/audrino cam (optional, use w MotionEye)
- USB microphone?

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