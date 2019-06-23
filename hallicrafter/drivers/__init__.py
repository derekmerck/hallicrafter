try:
    import board
    import busio
    import digitalio
except ModuleNotFoundError:
    from .mock import Mock as board
    from .mock import Mock as busio
    from .mock import Mock as digitalio

try:
    import adafruit_ssd1306
except ModuleNotFoundError:
    from .mock import Mock as adafruit_ssd1306

try:
    import neopixel
except ModuleNotFoundError:
    from .mock import Mock as neopixel

try:
    import adafruit_am2320
except ModuleNotFoundError:
    from .mock import Mock as adafruit_am2320

try:
    import adafruit_veml7700
except ModuleNotFoundError:
    from .mock import Mock as adafruit_veml7700

