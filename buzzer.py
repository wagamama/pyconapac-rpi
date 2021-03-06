import RPi.GPIO as GPIO
import time

buzzer_pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)

def buzz(pitch, duration) :
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles) :
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, False)
        time.sleep(delay)

try:
    pitch_s = 800
    duration_s = 0.1
    buzz(float(pitch_s), float(duration_s))

except KeyboardInterrupt:
    GPIO.cleanup()
finally:
    GPIO.cleanup()

