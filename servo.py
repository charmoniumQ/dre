from pyfirmata import Arduino, util
import time
import math
import numpy as np


DEADBAND = 0
HORIZONTAL_SERVO_STEP = 0.04
HORIZONTAL_SERVO_DELAY = 0.3
FIRE_DELAY = 0.015
SHOOTER_VELOCITY = 1
TURN_TOLERANCE = 3
AIM_TOLERANCE = 4
class Servo(object):

    def __init__(self, pin, pos):
        self.pin  = pin
        
        if pos:
            self.pos = pos
            self.pin.write(round(pos))
    
    def move_to(self, new_pos):
        new_pos = round(min(max(new_pos, 0), 180))
        self.pin.write(new_pos)
        delta = abs(self.pos - new_pos)
        self.pos = new_pos
        return delta
    
    def move_by(self, requested_delta):
        new_pos = round(min(max(self.pos + requested_delta, 0), 180))
        self.pin.write(new_pos)
        delta = abs(self.pos - new_pos)
        self.pos = new_pos
        return delta

class ServoControl(object):
    def __init__(self):
        self.board = Arduino('/dev/cu.usbmodem1421')
        self.fireServo = Servo(self.board.get_pin('d:9:s'), 0)
        self.horizontalServo = Servo(self.board.get_pin('d:5:s'), 90)
        self.vertialServo = Servo(self.board.get_pin('d:3:s'), 90)

        time.sleep(.015)

        self.target_acquired = False
        self.turn_delta = 0
        self.aim_delta = 0
        self.cooldown_time = 0

    def turn(self, heading):
        if abs(heading) < DEADBAND:
            return True
        self.turn_delta = HORIZONTAL_SERVO_STEP * heading
        self.horizontalServo.move_by(self.turn_delta)

        time.sleep(HORIZONTAL_SERVO_DELAY)
        return False

    def aim(self, altitude, depth_inches):
        inches2meters = np.float64('2.54') / np.float64('100')
        depth = depth_inches * inches2meters
        x = depth * np.cos(np.radians(altitude)) * inches2meters
        y = depth * np.sin(np.radians(altitude)) * inches2meters
        g = 9.8
        v = SHOOTER_VELOCITY
        desc = v**4 - g*(g*x**2 + 2*y*v)
        
        if desc >= 0:
            # https://en.wikipedia.org/wiki/Projectile_motion#Angle_'"`UNIQ--postMath-0000003A-QINU`"'_required_to_hit_coordinate_(x,y)
            theta = np.degrees(np.arctan((v**2 - np.sqrt(desc))) / (g*x))
           
            self.aim_delta = self.vertialServo.pos - theta
           
            print(f'aiming {theta:.0f} deg up to hit {altitude:.0f} deg {depth:.2f} meters away')
           
            self.vertialServo.move_by(self.aim_delta)
        else:
            print('unhittable')

    def fire(self):
        print('fire in the hole')
        self.fireServo.move_to(180)
        time.sleep(FIRE_DELAY)
        self.fireServo.move_to(0)

    def maybe_fire(self):
        if time.time() - self.cooldown_time < 3:
            return
        
        print(f'{self.turn_delta:.0f} {self.aim_delta:.0f}')
        
        if np.fabs(self.turn_delta) < TURN_TOLERANCE and \
            np.fabs(self.aim_delta) < AIM_TOLERANCE:
            self.fire()
            self.cooldown()

    def got_target(self):
        if not self.target_acquired:
            self.target_acquired = True

    def cancel_target(self):
        self.target_acquired = False

    def cooldown(self):
        self.cooldown_time = time.time()