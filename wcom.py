#!/usr/bin/env python

# Communication module
# Display the tension of the solar panel

import time
import serial 

ser = serial.Serial(
        port='/dev/ttyS0', # ttyS0 for Pi3 and 0W - ttyAMA0 for other
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

setPin = 4

def baud:
    
def baud:

def 

print "Serial Connection initialized"

while 1:
    readings=ser.readline()

    print readings

    time.sleep(.5)