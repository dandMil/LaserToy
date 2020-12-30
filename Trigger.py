#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import subprocess
import os 


pwrButton= 33
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
GPIO.setup(pwrButton,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def main (args):
    count = 0

    while True:
        if GPIO.input(pwrButton) == GPIO.HIGH:
            print ("Calling LaserToy.py")
            os.system('python LaserToy.py')
            
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
