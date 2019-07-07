import busio
import board

try:
    i2c_bus = busio.I2C(board.SCL, board.SDA)
except RuntimeError:
    print("I2C unavailable!")
    i2c_bus = None
