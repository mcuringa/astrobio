import board
import neopixel
import time
import digitalio
import util


import time
import math
import board
import analogio
import pwmio
from adafruit_motor import servo


# tesing the servo motor
needle_pwm = pwmio.PWMOut(board.A2, frequency=50, duty_cycle=0)
needle = servo.Servo(needle_pwm, actuation_range=180)
pot = analogio.AnalogIn(board.A1)

while True:

    needle.angle = 0
    time.sleep(0.1)
    needle.angle = 45
    time.sleep(0.1)
    needle.angle = 90
    time.sleep(0.1)
    needle.angle = 135
    time.sleep(0.1)
    needle.angle = 180
    # print the pots
    print("pot value:", pot.value)



# requests = util.get_requests()
# print("wifi test")
# response = requests.get("https://api.github.com")
# print("response status code:", response.status_code)
# print("response text:", response.text)

# print("running basic qtpy test")

# pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
# # flash the pixel red, green, blue, then off
# x = 0
# while True:
#     pixels.fill((255, 0, 0))
#     time.sleep(0.25)
#     pixels.fill((0, 255, 0))
#     time.sleep(0.25)
#     pixels.fill((0, 0, 255))
#     time.sleep(0.25)
#     pixels.fill((0, 0, 0))
#     time.sleep(0.25)
#     print("loop count:", x)
#     x += 1
