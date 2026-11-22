import board
import neopixel
import time
import digitalio
import utils

requests = utils.get_requests()
print("wifi test")
response = requests.get("https://api.github.com")
print("response status code:", response.status_code)
print("response text:", response.text)

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
