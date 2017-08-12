import sys
import signal
import RPi.GPIO as GPIO
from time import sleep

def clean():
    GPIO.cleanup()
 
def sigint_handler(signum, instant):
    clean()
    sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

class Servo9g(object):

    def __init__(self, pin=2):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        self.servo = GPIO.PWM(pin, 50)
        self.servo.start(0)

    def clean(self):
        GPIO.cleanup()

    def move_angle(self, angle):
        duty_cycle = 1/18 * (angle) + 2
        self.servo.ChangeDutyCycle(duty_cycle)


if __name__ == "__main__":
    servo = Servo9g()

    for angle in range(0, 180):
        servo.move_angle(angle)
        sleep(0.05)
 
    for angle in range(180, 0, -1):
        servo.move_angle(angle)
        sleep(0.05)
    
    servo.clean()

