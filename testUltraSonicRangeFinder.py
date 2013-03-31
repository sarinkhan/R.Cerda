#!/usr/bin/env python
import time
import os
import RPi.GPIO as GPIO
 
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
 
#definition du ADC utilise (broche du MCP3008)
adcnum = 0
inch=3300.0/512.0
while True:
	# Lecture de la valeur brute du capteur
	read_adc0 = readadc(adcnum, SPICLK, SPIMOSI, SPIMISO, SPICS)

	# conversion de la valeur brute lue en milivolts = ADC * ( 3300 / 1024 )
	millivolts = read_adc0 * ( 3300.0 / 1024.0)
	
	dist0=millivolts/inch
	dist1=dist0 * 2.54

	print "valeurs lues : "
	print "\tvaleur brute : %s" % read_adc0
	print "\ttension : %s millivolts" % millivolts
	print "\tdistance : %s pouces" % dist0
	print "\tdistance : %s cm" % dist1
	time.sleep(0.05)

 
 

