import sys
import time
from servo9g import Servo9g


if __name__ == "__main__":
    servo = Servo9g()

    while True:
        for angle in range(0, 180):
            servo.move_angle(angle)
            time.sleep(0.01)
     
        for angle in range(180, 0, -1):
            servo.move_angle(angle)
            time.sleep(0.01)
        
    servo.clean()


