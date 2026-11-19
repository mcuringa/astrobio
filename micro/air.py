import time
import math
import board
import analogio
import pwmio
from adafruit_motor import servo


pot = analogio.AnalogIn(board.A1)
needle_pwm = pwmio.PWMOut(board.A2, frequency=50, duty_cycle=0)
needle = servo.Servo(needle_pwm, actuation_range=180)

# calibration values for the potentiometer
MIN_ADC = 456
MAX_ADC = 50263
TAPER = 8.0


def sync_needle(gauge):
    """Move the gauge needle from 180 to 0 degrees for a gauge value of 0–10."""
    needle.angle = 180.0 - max(0.0, min(10.0, gauge)) * 18.0


def pot_to_10(raw):
    """Converts the raw potentiometer value to a 0–10 scale with logarithmic taper."""
    x = (raw - MIN_ADC) / (MAX_ADC - MIN_ADC)
    x = max(0.0, min(1.0, x))

    # Correct logarithmic taper
    linear = math.log(1 + (TAPER - 1) * x) / math.log(TAPER)

    # Convert to 0–10
    return round(linear * 10)

def init():
    raw = pot.value
    gauge = pot_to_10(raw)
    print(
        f"Startup: Servo angle: {needle.angle} degrees, Pot raw: {raw}, Gauge: {gauge}")
    sync_needle(gauge)

    time.sleep(1.0)

init()

while True:
    raw = pot.value
    gauge = pot_to_10(raw)
    sync_needle(gauge)

    print(f"Gauge: {gauge}")

    time.sleep(0.25)
