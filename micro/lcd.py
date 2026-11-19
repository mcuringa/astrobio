import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time

print("testing lcd display")

lcd = characterlcd.Character_LCD_Mono(
    digitalio.DigitalInOut(board.A0),
    digitalio.DigitalInOut(board.A1),
    digitalio.DigitalInOut(board.A2),
    digitalio.DigitalInOut(board.A3),
    digitalio.DigitalInOut(board.SCL),
    digitalio.DigitalInOut(board.SDA),
    16, 2
)

while True:
    print("looping")
    lcd.clear()
    lcd.message = "Hello from\nQT Py!"
    time.sleep(1.0)
    lcd.clear()
    lcd.message = "This is a test\nof the LCD"
    time.sleep(1.0)
