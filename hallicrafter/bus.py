from .drivers import board, busio

i2c = busio.I2C(board.SCL, board.SDA)
