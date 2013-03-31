#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C
import smbus
import time
import os
import RPi.GPIO as GPIO
from Adafruit_MCP230xx import Adafruit_MCP230XX
import smbus
import datetime
import subprocess as sub  
import urllib2, urllib
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#fonction lisant les donnees SPI de la puce MCP3008, parmi 8 entrees, de 0 a 7
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:   
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
		
        adcout /= 2       # first bit is 'null' so drop it
        return adcout
 
# ces numeros de pins GPIO doivent etre modifies pour correspondre aux broches utilisees.
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# definition de l'interface SPI
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
inch=3300.0/512.0

		
if __name__ == '__main__':
    mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)
	
	
    def readDistanceInch(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS):
      r = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)
      r = r * ( 3300.0 / 1024.0)
      r=r/inch
      return r
	  

    def moveForward(m1a,m1b,m1e,m2a,m2b,m2e):
      mcp.output(m1a, 1)  
      mcp.output(m1b, 0)
      mcp.output(m1e, 1)
	  
      mcp.output(m2a, 1)
      mcp.output(m2b, 0)
      mcp.output(m2e, 1)
		
		
    def moveBackward(m1a,m1b,m1e,m2a,m2b,m2e):
      mcp.output(m1a, 0)  
      mcp.output(m1b, 1)
      mcp.output(m1e, 1)
	  
      mcp.output(m2a, 0)
      mcp.output(m2b, 1)
      mcp.output(m2e, 1)
	  
    def stopMotors(m1a,m1b,m1e,m2a,m2b,m2e):
      mcp.output(m1e, 0)
      mcp.output(m2e, 0) 
	  
    def turnLeft(m1a,m1b,m1e,m2a,m2b,m2e):
      mcp.output(m1a, 0)  
      mcp.output(m1b, 1)
      mcp.output(m1e, 1)
	  
      mcp.output(m2a, 1)
      mcp.output(m2b, 0)
      mcp.output(m2e, 1)

    def turnRight(m1a,m1b,m1e,m2a,m2b,m2e):
      mcp.output(m1a, 1)  
      mcp.output(m1b, 0)
      mcp.output(m1e, 1)
	  
      mcp.output(m2a, 0)
      mcp.output(m2b, 1)
      mcp.output(m2e, 1)
	  
	  
	  
	#gestion des detecteurs de contact avant gauche et droit
    FLContactPin=7
    FRContactPin=6
    def readFLContact():
		return not(mcp.input(FLContactPin) >>FLContactPin)
		
    def readFRContact():
		return not(mcp.input(FRContactPin) >>FRContactPin)

		
	#definition des broches du moteur 1
    m1a=8
    m1b=9
    m1e=12
	
	#definition des broches du moteur 2
    m2a=10
    m2b=11
    m2e=13
	
	#On definit les broches A et B du moteur 1, ainsi que la broche d'activation en sortie
    mcp.config(m1a, mcp.OUTPUT)
    mcp.config(m1b, mcp.OUTPUT)
    mcp.config(m1e, mcp.OUTPUT)
	
	# On definit les broches A et B du moteur 2, ainsi que la broche d'activation en sortie
    mcp.config(m2a, mcp.OUTPUT)
    mcp.config(m2b, mcp.OUTPUT)
    mcp.config(m2e, mcp.OUTPUT)
	
	# les broches du detecteur de contact avant sont configurees en lecture
    mcp.pullup(FRContactPin, 1)
    mcp.pullup(FLContactPin, 1)

    dir1=1;
    #boucle principale et infinie du moteur
    while (True):
		if(readFLContact()==1 or readFRContact()==1):
			moveBackward(m1a,m1b,m1e,m2a,m2b,m2e)
			time.sleep(0.2)
		else :
			#lecture de la distance de l'obstacle le plus proche
			d=readDistanceInch(0, SPICLK, SPIMOSI, SPIMISO, SPICS)
			#en dessous de 8 pouces, le robot recule pendant au moins 0.2s
			if(d<8):
				moveBackward(m1a,m1b,m1e,m2a,m2b,m2e)
				#time.sleep(0.2)
			#entre 8 et 16 pouces, le robot tourne pendant au moins 0.2s
			elif(d<16) :
				turnLeft(m1a,m1b,m1e,m2a,m2b,m2e)
				time.sleep(0.2)	
			#le reste du temps le robot avance pendant 0.05s
			else :
				moveForward(m1a,m1b,m1e,m2a,m2b,m2e)
		time.sleep(0.05)	  
	  