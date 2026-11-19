import board
import digitalio
import time


print("testing hall sensor")

hall = digitalio.DigitalInOut(board.A1)
hall.switch_to_input(pull=digitalio.Pull.UP)

while True:
    print("Magnet detected:", not hall.value)
    time.sleep(0.2)


