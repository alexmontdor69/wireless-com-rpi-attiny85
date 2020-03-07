#!/usr/bin/env python


import time
import serial
import RPi.GPIO as GPIO

# Opening the serial Port for GT-38 configuration purposes
wirelessCommunication = serial.Serial(
    port='/dev/ttyS0',              # ttyS0 for Pi3 and 0W - ttyAMA0 for other
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# standard parameters
baudRate = 9600
setPin = 4
##########################################vv
def logging (message):
    print (message)
    timeStamp = time.ctime()
    logFile.write(timeStamp+" "+message+"\r\n")

def GT38Sending(message):
    answer = GT38Answer()
    time.sleep(.1) 
    wirelessCommunication.write(str("@ "+answer+" - "+message+"\n"))
    logging (time.ctime()+answer)

def GT38Communicating(message):
    time.sleep(.1) 
    wirelessCommunication.write(str(message))
    answer = GT38Answer()
    if (answer !="" or answer != "\n"):
        GPIO.output(LEDPin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LEDPin, GPIO.LOW)
    logging(time.ctime() +" "+answer)



def setCommunicationSpeed():
    global baudRate
    answer = GT38Answer()
    print answer
    if (answer[0:5] == ' OK+B'):
        baudRate=int(answer[5:])
        print ('Setting Baud Rate : ' + str(baudRate))


def GT38Mode(mode):
    # 2 modes
    # configuration : 'config'
    # operation : 'op'
    if (mode == "config"):
        logging("Switch Configuration Mode")
        GPIO.output(GT38SetPin, GPIO.LOW)
    if (mode == "op"):
        logging("Switch Operation Mode")
        GPIO.output(GT38SetPin, GPIO.HIGH)

def GT38Check ():
    print ("Checking configuration")
    request = "AT+RX\r\n"
    wirelessCommunication.write(request)
    setCommunicationSpeed()
    setCommunicationSpeed()
    setCommunicationSpeed()
    setCommunicationSpeed()
    # request = "AT+V\r\n"
    # wirelessCommunication.write(request)
    # print (GT38Answer())

def GT38ConfigChannel():
    channelNotValidated = True
    while (channelNotValidated):
        channelNumber = str(input("Put number (1-100)"))
        if (int(channelNumber)>0 and int(channelNumber)<=100):
            channelNotValidated = False
    request = "AT+C"+channelNumber+"\r\n"
    print ('Changing Channel' +  channelNumber)
    wirelessCommunication.write(request)
    print(GT38Answer())
###############################################


def GT38Answer():
    # get the answer from GT38
    #time.sleep(.1)
    # Waiting for a line to receive
    answer=""
    counter=0
    #time.sleep(1)
    while True:
        answer=wirelessCommunication.read_until('\n')
        
        if ((answer =="" or answer =='\r\n') and counter<10):
            if (counter>6):
                print ("attempt "+ str(counter))
            counter +=1
        else:
            break
        #answers.append(wirelessCommunication.readline())
        #answers.append(wirelessCommunication.readline())
        #c=answers
        #if len(c[1]) > 1:
        #        print (c)
        #        break
    #print ('answer:',answer, type(answer))
    return answer

def default_baud_rate ():
    # config fu
    global baudRate
    print ("Initialization Baud Rate "+ str(baudRate))
    request = "AT+B"+str(baudRate)+"\r\n"
    #request = "AT+RB\r\n"
    print ('sending', request)
    wirelessCommunication.write(request)
    answer = GT38Answer()
    if (answer == " OK+B"+str(baudRate)):
        logging("Changing Baud Rate"+str(baudRate))
    else:
        logging("Failed Baud Rate" + str(baudRate))

def set_FU (fu):
    # config fu
    print ("Initialization mode FU"+fu)
    request = "AT+FU"+fu+"\r\n"
    #request = "AT+RB\r\n"
    print ('sending', request)
    wirelessCommunication.write(request)
    answer = GT38Answer()
    if (answer == " OK+FU"+fu):
        logging("Changing FU"+fu)
    else:
        logging("Failed changing FU" + fu)
    
def set_baud (speed):
    GPIO.output(GT38SetPin, GPIO.LOW)
    time.sleep(.1) 
    request = "AT+B"+speed+"\r\n"
    GPIO.output(GT38SetPin, GPIO.HIGH)

def set_channel (channel):
    GPIO.output(GT38SetPin, GPIO.LOW)
    time.sleep(.1) 
    request = "AT+B"+channel+"\r\n"
    GPIO.output(GT38SetPin, GPIO.HIGH)


print "Serial Connection initialized"

GPIO.setup(GT38SetPin, GPIO.OUT) # Set pin set as output

# Configuration mode
GPIO.output(GT38SetPin, GPIO.LOW)
time.sleep(.1) 
default_baud_rate ()
time.sleep(.1) 
set_FU ('4')
time.sleep(.1)
GT38Check ()
time.sleep(.1)

#while 1:
#    readings=ser.readline()#

    #print readings

    #time.sleep(.5)
    

# Exchange data between GT-38 and Raspberry PI
# https://pinout.xyz/pinout/serial_pi_zero
# https://www.youtube.com/watch?v=Pwj4rHs9yQQ
# https://www.youtube.com/watch?v=JeUexihrKZQ
# https://www.youtube.com/watch?v=oiBi9RbNBUY



wirelessCommunication.baudrate = 9600

wirelessCommunication.baudrate = baudRate


print ('program ending')
GPIO.cleanup()
