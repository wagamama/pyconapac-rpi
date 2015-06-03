import RPi.GPIO as GPIO
import time

class BuzzManager:
    def __init__(self, buzzer_pin = 12):
        self.buzzer_pin = buzzer_pin

    def __enter__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.buzzer_pin, GPIO.OUT)
        return self

    def buzz(self, pitch=800, duration=0.1):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles) :
            GPIO.output(self.buzzer_pin, True)
            time.sleep(delay)
            GPIO.output(self.buzzer_pin, False)
            time.sleep(delay)

        GPIO.cleanup()

    # def __exit__(self, type, value, traceback):
    #     GPIO.cleanup()


if __name__ == '__main__':
    with BuzzManager() as buzzer:
        buzzer.buzz()
