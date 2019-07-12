# Setup a Raspberry Pi receiver node

See [Adafruit's setup guide](https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/rfm9x-raspberry-pi-setup)

1. Use `raspi-config` to enable `i2c` and `spi`.

2. Install CircuitPython and sample code:

````.bash
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install python3-pip
$ pip3 install RPI.GPIO adafruit-blinka
$ pip3 install adafruit-circuitpython-ssd1306 adafruit-circuitpython-framebuf adafruit-circuitpython-rfm9x
$ mkdir -p dev/lora
$ cd dev/lora
$ curl https://github.com/adafruit/Adafruit_CircuitPython_framebuf/raw/master/examples/font5x8.bin -O -L
$ curl https://learn.adafruit.com/pages/14606/elements/3014285/download -o rfm9x_check.py
$ python3 rfm9x_check

$ curl https://learn.adafruit.com/pages/14608/elements/3014295/download -o radio_rfm9x.py
````

