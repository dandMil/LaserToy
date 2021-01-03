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
servoPinB = 12
servoPinA = 22
laserPinB = 7
laserPin = 37
currentPosition = 7.5
neutralPosition = 7.5
negativePosition = 5
positivePosition = 10
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPinA, GPIO.OUT)
GPIO.setup(laserPin,GPIO.OUT)  
GPIO.setup(laserPinB, GPIO.OUT)
GPIO.setup(servoPinB, GPIO.OUT)
pwm=GPIO.PWM(servoPinA,50)
pwmB=GPIO.PWM(servoPinB,50)


     
def main(args):
    print ("Setting to neutral position")
    pwm.start(0)
    pwmB.start(0)
    moduleA = LaserModule()
    moduleB = LaserModule()
    compoundModule = CompoundLaserModule()
    init(moduleA,moduleB,compoundModule)
    startTime = time.time()
    randNumber = random.randint(0,1)
    while time.time()-startTime < 180:
        if randNumber == 0:
            laserGameChase(compoundModule)
        else:
            laserGamePounce(compoundModule)
    print("Time exceeded, ending game")
    compoundModule.turnOffLights()


#initates LaserMods
def init(moduleA, moduleB, compoundModule):
    moduleA.laser = laserPin
    moduleA.servo = servoPinA
    moduleA.name = 'LaserModule A'
    moduleB.laser = laserPinB
    moduleB.servo = servoPinB
    moduleB.name = 'LaserModule B'
    compoundModule.moduleA = moduleA
    compoundModule.moduleB = moduleB
    
    
   
#lasers move from left to right and sporatically turns
#the laser on and keeps in one spot for a set amount of time, then
#again turns off, changes angles and turns the light back on
def laserGameChase(compoundModule):
    print("Starting chase")
    module = selectModule(compoundModule)
    module.angle = random.randint(0,160)
    module.turnOnLight()
    module.isActive = True
    print("Setting angle to ",str(module.angle))
    setAngle(module)
    sleepTime = random.randint(3,10)
    print("Sleeping for ",str(sleepTime))
    sleep(sleepTime)
    module.turnOffLight()
    module.isActive = False


#angle of diode changes when off, turns back on and sleeps for sometime
def laserGamePounce(compoundModule):
    print("Starting pounce")
    module = selectModule(compoundModule)
    module.angle = random.randint(0,160)
    setAngle(module)
    module.turnOnLight()
    module.isActive = True
    module.moduleSummary()
    sleepTime= random.randint(5,15)
    sleep(sleepTime)
    module.turnOffLight()
    module.isActive = False
    
       

def selectModule(compoundModule):
    print ("Selecting module")
    randNum = random.randint(0,1)
    if randNum == 0:
        module = compoundModule.moduleA
    else:
        module = compoundModule.moduleB

    return module
        
def setAngle(module):
    print ('Moving module ',module.name)
    duty = module.angle/18 +3
    GPIO.output(module.servo,True)
    if module.name == 'LaserMoule A':
        pwm.ChangeDutyCycle(duty)
    else: 
        pwmB.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(module.servo,False)
    #pwm.ChangeDutyCycle(duty)

    
class LaserModule:

    servo = 0
    laser = 0
    name = ''
    angle = 0
    isActive = False
    
    def turnOnLight(self):
        print("Turning on laser ",self.laser)
        GPIO.output(self.laser,GPIO.HIGH)
        
    def turnOffLight(self):
        GPIO.output(self.laser,GPIO.LOW)
        
    def moduleSummary(self):
        print ("Module: ",self.name)
        print ("Laser: ",self.laser)
        print ("Servo: ",self.servo)
        print ("Active: ",self.isActive)

      
class CompoundLaserModule:
    moduleA = LaserModule()
    moduleB = LaserModule()

    def turnOffLights(self):
        print("Turning off laser diodes")
        if self.moduleA.isActive:
            GPIO.ouput(self.moduleA.laser,GPIO.LOW)
        if self.moduleB.isActive:
            GPIO.output(self.moduleB.laser,GPIO.LOW)
        

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
