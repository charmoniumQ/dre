import sys
from servo import Servo

board = Arduino('/dev/cu.usbmodem1421')
        self.fireServo = 

servos = {
    'f': Servo(Servo(self.board.get_pin('d:9:s'), 0)),
    'h': Servo(self.board.get_pin('d:5:s'), 90),
    'v': Servo(self.board.get_pin('d:3:s'), 90),
}

for line in sys.stdin:
    elems = line.split(' ')
    if len(elems) == 2:
        servo, val = elems
        if servo in servos:
            if val[0] in '+-':
                servos[servo].move_by(int(val))
            else:
                servos[servo].move_to(int(val))
