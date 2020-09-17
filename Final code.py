import time
import sys
import ibmiotf.application
import ibmiotf.device
import random #for sensor values
import requests # for sending sms
#Provide your IBM Watson Device Credentials
organization = "blavqr"
deviceType = "raspberrypi"
deviceId = "123456"
authMethod = "token"
authToken = "12345678"

# Initialize GPIO

def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='lighton':
                print("light is on")
        elif i=='lightoff':
                print("light is off")

try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)#.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        pulse=random.randint (58, 102)#normal pulse rate of human body is btw (60- 100)
        #print(pulse)
        temp = random.randint (30, 40)
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Pulse': pulse }
        print (data)
        
            
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Pulse = %s %%" % pulse, "to IBM Watson")

        success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
        if (pulse>100 or pulse<60): #setting the if condition for sending sms through fast2sms
            print(f"Document successfully created.")
            r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=CT8hIwZG0p7ROvsZ1xg9KH9SwOfAVjswzoEx0vugk6axVZbI9Tyk7bVao0Gv&sender_id=FSTSMS&message=Pulse%20is%20not%20normal&language=english&route=p&numbers=9810768394')
            print(r.status_code)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
