# uWeather Perpetual Station

Merck, Summer 2019

Roughly follows this [Adafruit air-quality sensor tutorial][].  Adds a photovoltaic charger and a LoRa radio for "off grid" data collection.

[Adafruit air-quality sensor tutorial]: https://learn.adafruit.com/adafruit-io-air-quality-monitor

## Parts List

- Feather Mx - $20
- LoRa Feather Wing - $20
- Small LoRa coil antenna - $2
- UV sensor - $6
- Air quality sensor - $10
- 2x 4.7k resistors - $2
- 6V charger - $10
- Large LiPo battery - $15
- Small photovoltaic cell - $10
- 2.1mm DC plug - $1
- Female header - $2
- Protoboard - $1
- Small enclosure - $10

Total cost: ~$100

** Creating a Raspberry Pi LoRa base station will cost another $25


## Assembly

- Layout the parts onto the protoboard, install header segments and wiring. I used the female header on the board and bottom pins on the components, and I soldered connections onto the underside of the protoboard.

- It should not be necessary b/c Adafruit includes pullups on their I2C sensors, but I found that I had to add 4.7k pullup resistors to the I2C bus to get the system to reliably start up headlessly.

- Assemble the charger.  Make sure to leave some slack on the big capacitor and bend it over slightly to lower the height profile.

- Mount the board on the back wall inside the enclosure using 2mm stand-offs.

- Change the photocell cord to use a 2.1mm jack, run it through the aperture, and seal the box up.

- Update the Feather to the latest bootloader and CircuitPython build.  Copy over the `hallicrafter.device` library and any required Adafruit libs (see `requirements.txt`).  

- Modify `code.py` from this project to use either the simple LoRa radio to forward JSON directly to an aggregator like `adafruit.io` or the LoRaWAN radio to forward encoded data to your own TTN app.

- To setup a single-channel Raspberry Pi forwarder and a TTN app, refer to this [Adafruit LoRaWAN tutorial][]

[Adafruit LoRaWAN tutorial]: https://learn.adafruit.com/raspberry-pi-single-channel-lorawan-gateway



Notes
--------------

Todo: Add button to force update
