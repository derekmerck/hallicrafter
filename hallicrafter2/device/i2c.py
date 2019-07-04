import busio
import board

i2c_bus = busio.I2C(board.SCL, board.SDA)