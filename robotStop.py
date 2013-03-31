#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C
from Adafruit_MCP230xx import Adafruit_MCP230XX
import smbus
import time



class MCP230XX_GPIO(object):
    OUT = 0
    IN = 1
    BCM = 0
    BOARD = 0
    def __init__(self, busnum, address, num_gpios):
        self.chip = Adafruit_MCP230XX(busnum, address, num_gpios)
    def setmode(self, mode):
        # do nothing
        pass
    def setup(self, pin, mode):
        self.chip.config(pin, mode)
    def input(self, pin):
        return self.chip.input(pin)
    def output(self, pin, value):
        self.chip.output(pin, value)
    def pullup(self, pin, value):
        self.chip.pullup(pin, value)
        

if __name__ == '__main__':
    mcp = Adafruit_MCP230XX(busnum = 1, address = 0x20, num_gpios = 16)

    # ***************************************************
	# Set num_gpios to 8 for MCP23008 or 16 for MCP23017!
	# If you have a new Pi you may also need to add:
	# busnum = 1
	# ***************************************************
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

    m1a=8
    m1b=9
    m1e=12
	
    m2a=10
    m2b=11
    m2e=13

    mcp.config(m1a, mcp.OUTPUT)
    mcp.config(m1b, mcp.OUTPUT)
    mcp.config(m1e, mcp.OUTPUT)
	
    mcp.config(m2a, mcp.OUTPUT)
    mcp.config(m2b, mcp.OUTPUT)
    mcp.config(m2e, mcp.OUTPUT)
    
    stopMotors(m1a,m1b,m1e,m2a,m2b,m2e)  
	  