from pyfirmata import Arduino, util
import sys

board = Arduino('/dev/cu.usbmodem1421')
vertialServo = self.board.get_pin('d:3:s')
vertialServo.write(int(sys.argv[1]))