import RPi.GPIO as GPIO
import time
import os

buzzer_pin = 12
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


class BuzzManager:
    def __init__(self, pin):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def buzz(self, pitch=800, duration=0.1):
        os.system('/home/pi/pyconapac-rpi/lib/buzzer.py')


if __name__ == "__main__":
    try:
        pitch_s = 800
        duration_s = 0.1
        buzz(float(pitch_s), float(duration_s))

    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()

