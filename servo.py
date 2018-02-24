from pyfirmata import Arduino, util
import time


DEADBAND = 0
HORIZONTAL_SERVO_STEP = 0.05
HORIZONTAL_SERVO_DELAY = 0.3


class ServoControl(object):
    def __init__(self):
        self.board = Arduino('/dev/cu.usbmodem1421')
        self.horizontalServo = self.board.get_pin('d:5:s')
        self.vertialServo = self.board.get_pin('d:3:s')
        self.horizontalServo.write(90)
        self.vertialServo.write(90)
        time.sleep(.015)
        self.hp = 90
        self.vp = 90
    def turn(self, heading):
        if abs(heading) < DEADBAND:
            return True
        print ("Updating heading by: ", int(HORIZONTAL_SERVO_STEP * heading), self.hp)
        self.hp += round(HORIZONTAL_SERVO_STEP * heading)
        self.hp = min(max(self.hp, 0), 180)
        self.horizontalServo.write(self.hp)

        time.sleep(HORIZONTAL_SERVO_DELAY)
        return False
