# coding:utf-8
import sys
import time
import signal
import RPi.GPIO as GPIO

def clean():
    GPIO.cleanup()
 
def sigint_handler(signum, instant):
    clean()
    sys.exit()

signal.signal(signal.SIGINT, sigint_handler)

class HCSR04(object):
    """
    This class is based on post
    https://dragaosemchama.com/2017/03/sonar-no-arduino-e-raspberry-pi/
    """

    sampling_rate = 20.0
    speed_of_sound = 349.10
    max_distance = 4.0
    max_delta_t = max_distance / speed_of_sound

    def __init__(self, trig=23, echo=18):
        self.trig = trig
        self.echo = echo
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, False)
        time.sleep(1)

    def clean(self):
        GPIO.cleanup()
 
    @property
    def value(self):
        GPIO.output(self.trig, True)
        time.sleep(0.00001)
        GPIO.output(self.trig, False)
 
        while GPIO.input(self.echo) == 0:
            start_t = time.time()
 
        while GPIO.input(self.echo) == 1 and time.time() - start_t < self.max_delta_t:
            end_t = time.time()
     
        if end_t - start_t < self.max_delta_t:
            delta_t = end_t - start_t
            distance = 100*(0.5 * delta_t * self.speed_of_sound)
        else:
            distance = -1
     
        distance = round(distance, 2)
        time.sleep(1/self.sampling_rate)
        return distance

if __name__ == "__main__":
    hcsr04 = HCSR04()

    for _ in range(1,50):
        time.sleep(1)
        print(hcsr04.value)

    hcsr04.clean()

