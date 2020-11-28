#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  LaserToy.py
#  
#  Copyright 2020  <pi@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import RPi.GPIO as GPIO
import time as time
from time import sleep
import random
servoPin = 12
laserPin = 7
currentPosition = 7.5
neutralPosition = 7.5
negativePosition = 5
positivePosition = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(laserPin,GPIO.OUT)  
pwm=GPIO.PWM(servoPin,50)


     
def main(args):
    print ("Setting to neutral position")
    pwm.start(0)
    laserGameA()


#lasers move from left to right and sporatically turns
#the laser on and keeps in one spot for a set amount of time, then
#again turns off, changes angles and turns the light back on
def laserGameA():
    while True: 
        angle = random.randint(0,160)
        sleepTime = random.randint(3,15)
        print("Sleeping for ",str(sleepTime))
        sleep(sleepTime)
        print("Setting angle to ",str(angle))
        setAngle(angle)
    

    
def setAngle(angle):
    duty = angle/18 +3
    GPIO.output(servoPin,True)
    pwm.ChangeDutyCycle(duty)
    lightOn()
    sleep(1)
    GPIO.output(servoPin,False)
    pwm.ChangeDutyCycle(duty)

def lightOn():
    print ("Turning on laser")
    GPIO.output(laserPin,GPIO.HIGH)
    
def lightOff():
    print ("Turning off laser")
    GPIO.output(laserPin,GPIO.LOW)
        
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
