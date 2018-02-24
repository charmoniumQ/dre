from pyfirmata import Arduino, util
import time
board = Arduino('/dev/cu.usbmodem1421')

print (board.get_firmata_version())
servo1 = board.get_pin('d:3:s')
servo2 = board.get_pin('d:5:s')

while True:
    
    for i in range(0,181):
        servo1.write(i)
        time.sleep(.015)
        servo2.write(i)
        time.sleep(.015)
    for i in range(180,0,-1):
        servo1.write(i)
        time.sleep(.015)
        servo2.write(i)
        time.sleep(.015)