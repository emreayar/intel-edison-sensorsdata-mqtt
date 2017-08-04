# This Python file uses the following encoding: utf-8
#Importing The Client Class
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os,sys
import mraa
import time
import sys
import math


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#Creating a Client Instance	

client = mqtt.Client()
client.on_connect = on_connect   #configures callback for new connection established


#Before you can publish messages or subscribe to topics you need to establish a connection to a broker.
#Connecting To a Broker or Server
client.connect("iot.eclipse.org",60)  #connects to broker (the '60' parameter means keepalive time). If no messages are exchanged in 60 seconds, This program automatically sends ping to broker (for keeping connection on)
client.loop_start()	 #start the loop

temptPin=0
tempt=mraa.Aio(temptPin)
temptValue=0

soundPin=1
sound=mraa.Aio(soundPin)
soundSensorValue=0

lightPin=2
light=mraa.Aio(lightPin)
lightValue=0

buttonPin=mraa.Gpio(2)
buttonPin.dir(mraa.DIR_IN)



while True:
    lightValue=float(light.read())
    client.publish("/homeoffice/sensors/lightSensor", payload=lightValue, qos=0, retain=False)
	
    B=3975
    temptValue = float(tempt.read())
    resistance = (float)(1023 - temptValue) * 10000 / temptValue
    temperature = 1 / (math.log(resistance / 10000) / B + 1 / 298.15) - 273.15
    client.publish("/homeoffice/sensors/temptSensor", payload=temperature, qos=0, retain=False)

    soundSensorValue = float(sound.read())
    client.publish("/homeoffice/sensors/soundSensor", payload=soundSensorValue, qos=0, retain=False)
    time.sleep(5)

client.loop_stop()   #stop loop
client.disconnect()  #disconnect        
    
