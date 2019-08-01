uWeather Perpetual Station
=======================

Merck, Summer 2019

A Feather Mx based air quality monitor suitable for "off-grid" sensing.  Uses a battery-backed photovoltaic cell for power and a LoRa radio to submit measurement data.  Assembly roughly follows this [Adafruit air-quality sensor tutorial][].

[Adafruit air-quality sensor tutorial]: https://learn.adafruit.com/adafruit-io-air-quality-monitor

Sample output from a prototype system can often be viewed at [Dweet][].

[Dweet]: https://dweet.io/get/dweets/for/uweather


Parts List
-----------------------

- [Feather M4][] - $23
- [LoRa Feather Wing][] - $20
- [Spring antenna][] - $1
- [UV sensor][] - $6
- [Air quality sensor][] - $23
- [2x 4.7k resistors][] - $1
- [Solar charger][] - $18
- [1200mAh LiPo battery][] - $10
- [6V/1W solar panel][] - $20
- [2.1mm DC plug][] - $1
- [Female header][] - $3
- [Perfboard][] - $11
- [Small enclosure][] - $10

Total cost: ~$150

[Feather M4]: https://www.adafruit.com/product/3857
[LoRa Feather Wing]: https://www.adafruit.com/product/3231
[Spring antenna]: https://www.adafruit.com/product/4269
[UV sensor]: https://www.adafruit.com/product/3964
[Air quality sensor]: https://www.adafruit.com/product/3660
[2x 4.7k resistors]: https://www.adafruit.com/product/2783
[Solar charger]: https://www.adafruit.com/product/390
[1200mAh LiPo battery]: https://www.adafruit.com/product/258
[6V/1W solar panel]: https://www.adafruit.com/product/3809
[2.1mm DC plug]: https://www.adafruit.com/product/3310
[Female header]: https://www.adafruit.com/product/598
[Perfboard]: https://www.amazon.com/AUSTOR-Prototype-Universal-Protoboard-Electronic/dp/B074X2GDH2
[Small enclosure]: https://www.adafruit.com/product/903

** Creating a LoRa base station will cost another $14 for a [Raspberry Pi Zero][] and $32 for a [LoRa Bonnet][].

[Raspberry Pi Zero]: https://www.adafruit.com/product/3708
[LoRa Bonnet]: https://www.adafruit.com/product/4074

Assembly
----------------------

- Layout the parts onto the protoboard, install header segments and wiring. I used the female header on the board and bottom pins on the components, and I soldered connections onto the underside of the protoboard.

- Although Adafruit includes SCL and SDA pullups on their I2C sensors, I found that I had to add 4.7k pullup resistors to the I2C bus to get the system to reliably start up headlessly.

- Assemble the charger.  Make sure to leave some slack on the big capacitor and bend it over slightly to lower the height profile.

- Mount the board on the back wall inside the enclosure using 2mm stand-offs.

- Change the photocell cord to use a 2.1mm jack, run it through the aperture, and seal the box up.

- Update the Feather to the latest bootloader and CircuitPython build.  Copy over the `hallicrafter.device` library and any required Adafruit libs (see `requirements.txt`).  

- Copy `code.py` from this project to the Feather and modify it either to use the simple LoRa radio to forward JSON directly to an aggregator like `io.adafruit.com`, or to use the LoRaWAN radio to forward encoded data to your own TTN app.


LoRaWAN
----------------------

To setup a single-channel Raspberry Pi forwarder and a TTN app, refer to this [Adafruit LoRaWAN tutorial][].

[Adafruit LoRaWAN tutorial]: https://learn.adafruit.com/raspberry-pi-single-channel-lorawan-gateway

1. There is a bug in the single channel forwarder helper script.  When a packet is received, the subprocess emits both the packet data and a "gateway status update" message, which confuses the json parser.

Fix:

```python
# read incoming packet info
pkt_json = proc.stdout.readline().decode('utf-8')

if pkt_json.endswith("gateway status update\n"):
   pkt_json = pkt_json[:-len("gateway status update\n")]
```

### Decoding

For packet creation, I use python's `struct` class.  There is an equivalent JavaScript port of the class available as [JSPack](https://github.com/birchroad/node-jspack).

As an example:

Encoded: `b'9CBC5F46FC877840BC077E445C5A823CEDB10D00F0AC5342A4A8C141'`

Decoded:
```json
{
    "gas": 897517,
    "humidity": 52.91888427734375,
    "pressure": 1016.120849609375,
    "temperature": 24.20734405517578,
    "uptime": 14319.15234375,
    "uv": 0.01591222733259201,
    "voltage": 3.8832998275756836
}
```

Decoding with JSPack on TTN:

```javascript
// include functions from https://raw.githubusercontent.com/birchroad/node-jspack/master/jspack.js
function Decoder(bytes, port) {
  var p = new JSPack();
  var result = p.Unpack(">ffffiff", bytes);
  return {uptime: result[0],
          voltage: result[1],
          pressure: result[2],
          uv: result[3],
          gas: result[4],
          humidity: result[5],
          temperature: result[6]
  };
}
```


Notes
--------------

Todo: Add button to force on demand update
