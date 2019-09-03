# Refactored test program for Raspberry Pi with LORA shield
#
# Originally from:
# https://learn.adafruit.com/lora-and-lorawan-radio-for-raspberry-pi/rfm9x-raspberry-pi-setup

# sudo pip3 install adafruit-circuitpython-ssd1306
# sudo pip3 install adafruit-circuitpython-framebuf
# sudo pip3 install adafruit-circuitpython-rfm9x

import board
from device import System, DigitalInput, LoRaRadio, OLEDPanel


sys = System()

btnA = DigitalInput(board.D5,  pull="UP")
btnB = DigitalInput(board.D6,  pull="UP")
btnC = DigitalInput(board.D12, pull="UP")
oled = OLEDPanel(sys.i2c_bus, dims=(128,32), addr=0x3c, interval=1.0)
lora = LoRaRadio(sys.spi_bus, board.CE1, board.D25)


def btn_cb(self):
    if not self.last_value:
        state = "Pressed {}".format(self.name)
        lora.data["tx_buffer"] = state

btnA.callbacks.append(btn_cb)
btnB.callbacks.append(btn_cb)
btnC.callbacks.append(btn_cb)


def lora_cb(self):
    if self.data["rx_buffer"]:
        oled.data["rx"] = self.data["rx_buffer"]
    if self.data["tx_buffer"]:
        oled.data["tx"] = self.data["tx_buffer"]

lora.callbacks.append(lora_cb)


if __name__ == "__main__":
    sys.run()
