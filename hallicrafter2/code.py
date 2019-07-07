import time
import board
from device import Device, LEDStrip, SerialIO, Microprocessor
    # HDRLightSensor, \
    # TempHumSensor, Button, OLEDPanel, AnalogInput, SerialIO

LED_STRIP_CTRL_PIN = board.NEOPIXEL
LED_STRIP_NUM_LEDS = 1
LED_STRIP2_CTRL_PIN = board.A5
LED_STRIP2_NUM_LEDS = 24
OLED_RESET_PIN = board.D9  # D6 is A1 on cpx
OLED_DIMS = (128,64)
IR_DIODE_PIN = board.A0

UART_TX_LED = board.D10
UART_RX_LED = board.D11


# -------------------------------
# Create the led strip
# -------------------------------

led_strip  = LEDStrip(LED_STRIP_CTRL_PIN, LED_STRIP_NUM_LEDS, interval=0.01)

from utils.rgb import rgb_wheel_gen as gen
rgb_gen = gen(step=1)
def wheel_callback(self):
    self.fill(next(rgb_gen))
led_strip.callbacks.append(wheel_callback)

#
# led_strip2  = LEDStrip(LED_STRIP2_CTRL_PIN, LED_STRIP2_NUM_LEDS, interval=0.1)
#
# def wheel_callback2():
#     led_strip2.fill(next(rgb_gen))
# led_strip2.callback = wheel_callback2

# -------------------------------
# Create the button objects
# -------------------------------

# lf_button = Button(board.BUTTON_A)
#
# def lf_button_callback():
#     print("left button = {}".format(lf_button.button.value))
#
# lf_button.callback = lf_button_callback

# -------------------------------
# Create the sensor objects
# -------------------------------

# light_sensor = HDRLightSensor(interval=2)
# temp_hum_sensor = TempHumSensor(interval=2)
# ir_sensor = AnalogInput(IR_DIODE_PIN, name="ir diode", interval=0.001)
#
# last_hit_time = time.time()
# def detect_hit():
#
#     global last_hit_time
#     current_time = time.time()
#     if ir_sensor.input.value > 63000:
#         ir_sensor.data["hit"] = True
#         last_hit_time = current_time
#     elif current_time > last_hit_time + 2:
#         ir_sensor.data["hit"] = False
#
# ir_sensor.callback = detect_hit

# -------------------------------
# Create the OLED panel
# -------------------------------

# oled_panel = OLEDPanel(OLED_DIMS, OLED_RESET_PIN, interval=0.5)
#
# def read_sensors():
#     # oled_panel.data.update(light_sensor.data)
#     # oled_panel.data.update(temp_hum_sensor.data)
#     oled_panel.data.update(ir_sensor.data)
#     # print(oled_panel.data)
#
# oled_panel.callback = read_sensors

cpu = Microprocessor(name="cpu")

ser = SerialIO(interval=0.1)

# def handle_uart(self):
#
#     # rx_data will be a python instruction or script
#     # To create a return package, populate self.data and
#     # dump it to tx_data with self.dump_data()
#
#     if self.rx_data:
#         try:
#             eval(self.rx_data)
#         except SyntaxError:
#             print(self.rx_data)
#             print("Failed to eval serial input")

# ser.callbacks.append(handle_uart)

# -------------------------------
# Main loop
# -------------------------------

while True:
    for device in Device.registry.values():
        device.poll()
    time.sleep(0.001)
