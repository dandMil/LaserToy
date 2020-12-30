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
servoPinA = 12
servoPinB = 22
laserPin = 7
laserPinB = 37
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
    laserGameChase(compoundModule)


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
    startTime = time.time()
    while time.time()-startTime < 180:
        module = selectModule(compoundModule)
            
        module.angle = random.randint(0,160)
        lightOn(module)
        module.isActive = True
        print("Setting angle to ",str(module.angle))
        setAngle(module)
        sleepTime = random.randint(3,10)
        print("Sleeping for ",str(sleepTime))
        sleep(sleepTime)
        module.turnOffLight()
        module.isActive = False
    print ("Game time exceeded, turning off now")
    compoundModule.turnOffLights()


        


#angle of diode changes when off, turns back on and sleeps for sometime
def laserGamePounce(compoundModule):
    print("Starting pounce")
    selectModule(compoundModule)
    print("Pounce Game")
    print("Pounce Game")
       

def selectModule(compoundModule):
    print ("Selecting module")
    randNum = random.randint(0,1)
    if randNum = 0:
        module = compoundModule.moduleA
    else:
        module = compoundModule.moduleB
    print ("Selected module: ",module.name)
    return module
        
def setAngle(module):
    print ('Moving module ',module.name)
    duty = module.angle/18 +3
    GPIO.output(module.servo,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(module.servo,False)
    #pwm.ChangeDutyCycle(duty)

def lightOn(module):
    print ("Turning on laser diode")
    print (module.laser)
    GPIO.output(module.laser,GPIO.HIGH)
        
    
def lightOff(moduleA,moduleB):
    print ("Turning off laser diodes")
    GPIO.output(moduleA.laser,GPIO.LOW)
    GPIO.output(moduleB.laser,GPIO.LOW)
    
class LaserModule:
    def turnOffLight(self):
        GPIO.output(self.laser,GPIO.LOW)
    servo = 0
    laser = 0
    name = ''
    angle = 0
    isActive = False

      
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
