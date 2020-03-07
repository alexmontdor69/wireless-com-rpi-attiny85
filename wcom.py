#!/usr/bin/env python


import time
import serial
import RPi.GPIO as GPIO

ser = serial.Serial(
        port='/dev/ttyS0', # ttyS0 for Pi3 and 0W - ttyAMA0 for other
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)

# standard parameters
baudRate = 9600
setPin = 4


def baud:
    
def baud:

def 

print "Serial Connection initialized"

GPIO.setup(GT38SetPin, GPIO.OUT) # Set pin set as output

while 1:
    readings=ser.readline()

    print readings

    time.sleep(.5)
    
    
#!/usr/bin/env python

# Exchange data between GT-38 and Raspberry PI
# https://pinout.xyz/pinout/serial_pi_zero
# https://www.youtube.com/watch?v=Pwj4rHs9yQQ
# https://www.youtube.com/watch?v=JeUexihrKZQ
# https://www.youtube.com/watch?v=oiBi9RbNBUY




import io
import time
import serial
import RPi.GPIO as GPIO

# Opening an existing logFile or creating it
print ("Opening log file")
logFile = open('log.txt','a')
logFile.write("new attempt\r\n")

# Opening the serial Port for GT-38 configuration purposes
wirelessCommunication = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# The Boss Role => Receiving the beacon signal
# The Slave Role => the Beacon
ImTheBoss= False
baudRate = 9600

# PIN configuration
# Raspberry zero BCM17 pin 11
# Raspberry 3 BCM17 pin 11
GT38SetPin = 17 # To set the GT-38
requestTempButtom = 27 # To use a button
LEDPin= 22  # Use a LED as a External Simple Communication Mean (if no screen)

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(GT38SetPin, GPIO.OUT) # Set pin set as output
GPIO.setup(requestTempButtom, GPIO.IN) # Button to request temp
GPIO.setup(LEDPin, GPIO.OUT)

def init ():
    GPIO.output(LEDPin, GPIO.HIGH)
    # Mode configuration
    GT38Mode("config")
    # Time to allow the GT38 to be ready
    time.sleep(.1) 
    # Use the
    GT38ConfigBaudRate ()
    GT38ConfigFU ('4')
    
    GT38Check ()

    # No Manual configuration allowed if a device is used without screen
   # GT38ConfigChannel()

    # Mode operation
    GT38Mode("op")
    GPIO.output(LEDPin, GPIO.LOW)

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

def GT38ConfigBaudRate ():
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

def GT38ConfigFU (fu):
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
# Write about 
# Import serial
# How to write on a GPIO 
# configuration of the GT38

def TemperatureRequested():
    #print(GPIO.input(requestTempButtom))
    return GPIO.input(requestTempButtom)

def beacon ():
    print ('BIP '+time.ctime())
    wirelessCommunication.write('BIP '+time.ctime())
    # LED Blinks
    GPIO.output(LEDPin, GPIO.HIGH)
    time.sleep(.2)
    GPIO.output(LEDPin, GPIO.LOW)


def readBeacon ():
    print('Check the beacon')
    answer = GT38Answer ()
    if (answer):
        print ('@ ' + time.ctime() + ' => '+ answer)
        GPIO.output(LEDPin, GPIO.HIGH)

    else:
        print ('beacon signal NOT received (' + time.ctime()+')')
        GPIO.output(LEDPin, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(LEDPin, GPIO.LOW)
        time.sleep(.2)
        GPIO.output(LEDPin, GPIO.HIGH)
        time.sleep(.2)
        GPIO.output(LEDPin, GPIO.LOW)


init()
# Air Communication Speed 
wirelessCommunication.baudrate = baudRate

if (ImTheBoss):
    while True:
        readBeacon ()
        time.sleep(1.5)
#        if (TemperatureRequested()==1):
#            GT38Communicating("Message from Alex "+ time.ctime())
else:
    while True:
        beacon()
        time.sleep(1.5)
#        GT38Sending ("Temperature is 20degC")

print ('program ending')
GPIO.cleanup()
