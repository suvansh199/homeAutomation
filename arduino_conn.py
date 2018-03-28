#Python script to establish a connection with pyrebase
import pyrebase
import serial
import time
arduino = serial.Serial('/dev/cu.usbmodem1421', 9600)
time.sleep(2)
config = {
    "apiKey" : "AIzaSyBmPHmzskGzHUjVPODyfWEWie5orDXlJjo",
    "authDomain" : "homeautomation-57822.firebaseapp.com",
    "databaseURL" : "https://homeautomation-57822.firebaseio.com",
    "storageBucket" : "homeautomation-57822.appspot.com",
    "messagingSenderId" : "521580658288"
  }
firebase = pyrebase.initialize_app(config)
db1 = firebase.database()
def waitForAr(LED):
    while True:
        temp = arduino.readline()
        if(temp.decode() == LED):
            return   
def readline():
    myData = arduino.readline()
    myData2 = myData.decode()
    if(myData2[0] == "D"):
        return "D"
    elif(myData2[0] == "T"):
        return "T"
    elif(myData2[0] != "L" and myData2[0] != " "):
        for index in range(11):
                if(myData2[index] == " "):
                    break
        x = float(myData2[0:index])
        for index1 in range(index+1,11):
                if(myData2[index1] == " "):
                    break
        y = float(myData2[index+1:index1])
        z = float(myData2[index1+1:len(myData2)])
        return (x,y,z)
#db.update({"Led1":"Off"});
#print(db.child("Led1").get().val())
#print(db.get().val()[1])
while True:
    db = firebase.database()
    Led1 = db.get().val()["Led1"]
    Led2 = db.get().val()["Led2"]
    Led3 = db.get().val()["Led3"]
    Led4 = db.get().val()["Led4"]
    if(Led1 == "On"):
        arduino.write('7'.encode())
        #waitForAr("Led1")
    else:
        arduino.write('3'.encode())
        #waitForAr("Led1")
    if(Led2 == "On"):
        arduino.write('6'.encode())
        #waitForAr("Led2")
    else:
        arduino.write('2'.encode())
        #waitForAr("Led2")
    if(Led3 == "On"):
        arduino.write('5'.encode())
        #waitForAr("Led3")
    else:
        arduino.write("1".encode())
        #waitForAr("Led3")
    if(Led4 == "On"):
        arduino.write('4'.encode())
        #waitForAr("Le4")
    else:
        arduino.write('0'.encode())
        #waitForAr("Led4")