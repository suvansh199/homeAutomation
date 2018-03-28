#Python code for Raspberry Pi
import RPi.GPIO as GPIO
from threading import Thread
import time
import math
# Import the ADXL345 module.
import Adafruit_ADXL345
import pyrebase
config = {
    "apiKey": "AIzaSyBmPHmzskGzHUjVPODyfWEWie5orDXlJjo",
    "authDomain": "homeautomation-57822.firebaseapp.com",
    "databaseURL": "https://homeautomation-57822.firebaseio.com",
    "storageBucket": "homeautomation-57822.appspot.com",
    "messagingSenderId": "521580658288"
  }
firebase = pyrebase.initialize_app(config)
db = firebase.database()
led1 = 37
led2 = 35
led3 = 33
led4 = 31
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led4,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led1,GPIO.OUT)

def KeepUptoDate():
    global db
    Led1 = db.child("Leds").get().val()["Led1"]
    Led2 = db.child("Leds").get().val()["Led2"]
    Led3 = db.child("Leds").get().val()["Led3"]
    Led4 = db.child("Leds").get().val()["Led4"]
    if(Led1 == "On"):
        GPIO.output(led1,True)
    else:
        GPIO.output(led1,False)
    if(Led2 == "On"):
        GPIO.output(led2,True)
    else:
        GPIO.output(led2,False)
    if(Led3 == "On"):
        GPIO.output(led3,True)
    else:
        GPIO.output(led3,False)
    if(Led4 == "On"):
        GPIO.output(led4,True)
    else:
        GPIO.output(led4,False)

T = Thread(target = KeepUptoDate)
def UploadToFirebase(Led,Stat):
    global db
    global T
    if(Led == 1):
        db.child("Leds").update({"Led1": Stat})
    elif(Led == 2):
        db.child("Leds").update({"Led2": Stat})
    elif(Led == 3):
        db.child("Leds").update({"Led3": Stat})
    elif(Led == 4):
        db.child("Leds").update({"Led4": Stat})
# Create an ADXL345 instance.
accel = Adafruit_ADXL345.ADXL345()

# Alternatively you can specify the device address and I2C bus with parameters:
#accel = Adafruit_ADXL345.ADXL345(address=0x54, busnum=2)

# You can optionally change the range to one of:
#     ADXL345_RANGE_2_G   = +/-2G (default)
#  - ADXL345_RANGE_4_G   = +/-4G
#  - ADXL345_RANGE_8_G   = +/-8G
#  - ADXL345_RANGE_16_G  = +/-16G
# For example to set to +/- 16G:
accel.set_range(Adafruit_ADXL345.ADXL345_RANGE_16_G)

# Or change the data rate to one of:
#  - ADXL345_DATARATE_0_10_HZ = 0.1 hz
#  - ADXL345_DATARATE_0_20_HZ = 0.2 hz
#  - ADXL345_DATARATE_0_39_HZ = 0.39 hz
#  - ADXL345_DATARATE_0_78_HZ = 0.78 hz
#  - ADXL345_DATARATE_1_56_HZ = 1.56 hz
#  - ADXL345_DATARATE_3_13_HZ = 3.13 hz
#  - ADXL345_DATARATE_6_25HZ  = 6.25 hz
#  - ADXL345_DATARATE_12_5_HZ = 12.5 hz
#  - ADXL345_DATARATE_25_HZ   = 25 hz
#  - ADXL345_DATARATE_50_HZ   = 50 hz
#  - ADXL345_DATARATE_100_HZ  = 100 hz (default)
#  - ADXL345_DATARATE_200_HZ  = 200 hz
#  - ADXL345_DATARATE_400_HZ  = 400 hz
#  - ADXL345_DATARATE_800_HZ  = 800 hz
#  - ADXL345_DATARATE_1600_HZ = 1600 hz
#  - ADXL345_DATARATE_3200_HZ = 3200 hz
# For example to set to 6.25 hz:
#accel.set_data_rate(Adafruit_ADXL345.ADXL345_DATARATE_6_25HZ)
print("Starting intialisation....\n")
x,y,z = accel.read()
i = 0
KeepUptoDate()
while(i<5):
    print(5-i)
    print("\n")
    time.sleep(1)
    i+=1
print('Printing X, Y, Z axis values, press Ctrl-C to quit...')
while True:
    # Read the X, Y, Z axis acceleration values and print them.
    
    Thread(target = KeepUptoDate).start()
    x, y, z = accel.read()
    print('X={0}, Y={1}, Z={2}'.format(x, y, z))
    # Wait half a second and repeat.
    time.sleep(0.5)
    Pitch = math.degrees(math.atan(y/(math.hypot(z,x))))
    print(Pitch)
    Roll =math.degrees( math.atan(x/(math.hypot(z,y))))
    print(Roll)
    if(Pitch > 60):
        GPIO.output(led1,True)
        Thread(target = UploadToFirebase,args = (1,"On",)).start()    
    elif(Pitch< -60):
        GPIO.output(led1,False)
        Thread(target = UploadToFirebase,args = (1,"Off",)).start()
    if(Roll>60):
        Thread(target = UploadToFirebase,args = (2,"On",)).start()
        GPIO.output(led2,True)
    elif(Roll < -60):
        Thread(target = UploadToFirebase,args = (2,"Off",)).start()
        GPIO.output(led2,False)