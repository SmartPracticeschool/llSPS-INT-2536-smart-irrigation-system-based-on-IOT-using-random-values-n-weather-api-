import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import urllib.request
import json
import requests


#Provide your IBM Watson Device Credentials
organization = "pp2pfs"
deviceType = "windows"
deviceId = "12345678"
authMethod = "token"
authToken = "123456789"
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()
# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
while True:
        r=urllib.request.urlopen('https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=439d4b804bc8187953eb36d2a8c26a02')
        s=r.read()
        q=json.loads(s)
        temp=q['main']['temp']
        hum=q['main']['humidity']
        data = { 'Temperature' : temp, 'Humidity': hum }
        soil=random.randrange(0,1023)

        if (soil<=200):
            url = "https://www.fast2sms.com/dev/bulk"

            querystring = {"authorization":"ovKnyhewuJSIFWQZlji2zR8sm0qPDctOEg4rC73BLNA5d1HXVUHDfdjCprMFzxeoZakNn6O9uYW3LP54","sender_id":"FSTSMS","message":"turn on motor","language":"english","route":"p","numbers":"9963607462"}
  
            headers = {
               'cache-control': "no-cache"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            print(response.text)

        data = { 'Temperature' : temp, 'Humidity': hum,'Moisture':soil}

        
        
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s " % hum,"Moisture=%s %% "%soil, "to IBM Watson")
        success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        deviceCli.commandCallback = myCommandCallback
# Disconnect the device and application from the cloud
deviceCli.disconnect()
