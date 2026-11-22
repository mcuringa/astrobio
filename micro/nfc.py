import board
import time
import digitalio
from adafruit_pn532.i2c import PN532_I2C

print("starting nfc reader")
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)
pixels[0] = (255, 0, 0) 
i2c = board.I2C()
pn532 = PN532_I2C(i2c, debug=False)
pn532.SAM_configuration()

hall = digitalio.DigitalInOut(board.A0)
hall.switch_to_input(pull=digitalio.Pull.UP)

last_uid = None
last_nav = None

pixels[0] = (0, 255, 0)
while True:
    uid = pn532.read_passive_target(timeout=0.5)
    nav = hall.value
    data = not nav
    print("Planet ID:", uid)
    print("Navigation:", nav)
    print("Data:", data)
    if last_nav != nav:
        last_nav = nav
    
    if uid is not None:
        uid_hex = uid.hex().upper()
        planet_id = uid_hex
        data = not nav

        if uid_hex != last_uid:
            print("Planet ID:", planet_id)
            print("Navigation:", nav)
            last_uid = uid_hex

    else:
        if last_uid is not None:
            print("Tag removed")
            last_uid = None

    time.sleep(0.1)
