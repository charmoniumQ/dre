from pyfirmata import Arduino, util
import time
import math
import numpy as np


DEADBAND = 0
HORIZONTAL_SERVO_STEP = 0.04
HORIZONTAL_SERVO_DELAY = 0.3


class ServoControl(object):
    def __init__(self):
        self.board = Arduino('/dev/cu.usbmodem1421')
        self.horizontalServo = self.board.get_pin('d:5:s')
        self.vertialServo = self.board.get_pin('d:3:s')
        self.hp = 90
        self.vp = 90
        self.horizontalServo.write(self.hp)
        self.vertialServo.write(self.vp)
        time.sleep(.015)
        self.cancel_target()

        self.target_acquired = False
        self.turn_delta = 0
        self.aim_delta = 0
        self.cooldown_time = 0

    def turn(self, heading):
        if abs(heading) < DEADBAND:
            return True
        self.turn_delta = HORIZONTAL_SERVO_STEP * heading
        self.hp += round(self.turn_delta)
        self.hp = min(max(self.hp, 0), 180)
        self.horizontalServo.write(self.hp)

        time.sleep(HORIZONTAL_SERVO_DELAY)
        return False

    def aim(self, altitude, depth_inches):
        inches2meters = np.float64('2.54') / np.float64('100')
        depth = depth_inches * inches2meters
        x = depth * np.cos(np.radians(altitude)) * inches2meters
        y = depth * np.sin(np.radians(altitude)) * inches2meters
        g = 9.8
        v = 1
        desc = v**4 - g*(g*x**2 + 2*y*v)
        #desc = x**2 + 4*y*(y + (g/(2*v)*x**2))
        if desc >= 0:
            # https://en.wikipedia.org/wiki/Projectile_motion#Angle_'"`UNIQ--postMath-0000003A-QINU`"'_required_to_hit_coordinate_(x,y)
            theta = np.degrees(np.arctan((v**2 - np.sqrt(desc))) / (g*x))
            #theta = np.degrees(np.arcsin((x - np.sqrt(desc)) / (2*y)))
            self.aim_delta = self.vp - theta
            self.vp = round(theta)
            self.vp = min(max(self.vp, 0), 180)
            print(f'aiming {theta:.0f} deg up to hit {altitude:.0f} deg {depth:.2f} meters away')
            self.vertialServo.write(self.vp)
        else:
            print('unhittable')

    def maybe_fire(self):
        if time.time() - self.cooldown_time < 3:
            return
        print(f'{self.turn_delta:.0f} {self.aim_delta:.0f}')
        if np.fabs(self.turn_delta) < 3 and \
            np.fabs(self.aim_delta) < 4:
            print('fire in the hole')
            self.cooldown()

    def have_target(self):
        if not self.target_acquired: # already
            self.target_acquired = True

    def cancel_target(self):
        self.target_acquired = False

    def cooldown(self):
        self.cooldown_time = time.time()