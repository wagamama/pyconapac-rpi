import RPi.GPIO as GPIO
import time

class BuzzManager:
    def __enter__(self):
        buzzer_pin = 11
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(buzzer_pin, GPIO.OUT)
        return self

    def buzz(pitch=800, duration=0.1):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles) :
            GPIO.output(buzzer_pin, True)
            time.sleep(delay)
            GPIO.output(buzzer_pin, False)
            time.sleep(delay)

    def __exit__(self, type, value, traceback):
        GPIO.cleanup()
