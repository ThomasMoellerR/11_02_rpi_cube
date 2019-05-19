import spidev
import RPi.GPIO as GPIO
import time
import numpy as np
import itertools
import random
import math
import colorsys
from PIL import Image, ImageDraw, ImageFont
import paho.mqtt.client as mqtt
import threading
import colorsys
import math
import itertools
import argparse
import os



from animations.regen import regen
from animations.cube_random import cube_random

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, GPIO.LOW)
GPIO.output(23, GPIO.HIGH)


brightness = 1.0
mode = "random3"
mode_changed = False

actual_object_pointer = 0







def thread3():

    while True:
        time.sleep(0.1)

        




                

     



def thread2():
    global actual_object_pointer

    while True:
        if mode == "regen":
            obj = regen()
            obj.show()
        
        if mode == "random1":
            obj = cube_random()
            obj.random1()

        if mode == "random2":
            obj = cube_random()
            obj.random2()

        if mode == "random3":
            obj = cube_random()
            obj.random3()
                

     

 


def thread1():
    global client

    while True:

        client.on_connect = on_connect
        client.on_message = on_message

        try_to_connect = True

        while try_to_connect:
            try:
                client.connect(args.mqtt_server_ip, int(args.mqtt_server_port), 60)
                try_to_connect = False
                break
            except Exception as e:
                print(e)



        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(args.mqtt_topic_set_brightness)
    client.subscribe(args.mqtt_topic_set_mode)



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global brightness
    global mode
    global mode_changed

    print(msg.topic + " "+ msg.payload.decode("utf-8"))

    if msg.topic == args.mqtt_topic_set_brightness:
        brightness = float(msg.payload.decode("utf-8"))


    if msg.topic == args.mqtt_topic_set_mode:
        mode = msg.payload.decode("utf-8")
        mode_changed = True



################################################################################
#
# Hauptprogramm
#
################################################################################


# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mqtt_server_ip", help="")
parser.add_argument("--mqtt_server_port", help="")
parser.add_argument("--mqtt_topic_set_brightness", help="")
parser.add_argument("--mqtt_topic_set_mode", help="")
args = parser.parse_args()

client = mqtt.Client()

t1= threading.Thread(target=thread1)
t2= threading.Thread(target=thread2)
t3= threading.Thread(target=thread3)

t1.start()
time.sleep(1)
t2.start()
t3.start()
