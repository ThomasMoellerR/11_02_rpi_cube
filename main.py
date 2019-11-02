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
from mqtt import c_mqtt


from animations.regen import regen
from animations.cube_random import cube_random
from animations.snake import snake
from animations.blocks import blocks



GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, GPIO.LOW)
GPIO.output(23, GPIO.HIGH)


brightness = 1.0
mode = "regen"
obj = "objekt"




def Thread_Cube():
    global obj
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

        if mode == "full_color_change":
            obj = blocks()
            obj.full_color_change()


        if mode == "snakexxxxxxxxxxxxxxxxxxxxxxxxxxx":
         obj = snake(12)
         obj.show()




###############################################################################
#  Function Name  :  Thread_MqttLoop
#  Description    :  Mqtt Loop
#  Parameter(s)   :  None
#  Return Value   :  None
###############################################################################

def Thread_MqttLoop():
    while True:
        o.loop()
 

###############################################################################
#  Function Name  :  Thread_MqttRecQueue
#  Description    :  Receives Mqtt messages
#  Parameter(s)   :  None
#  Return Value   :  None
###############################################################################

def Thread_MqttRecQueue():
    global brightness
    global mode
    global mode_changed

    while True:
        if not o.empty():
            topic, message = o.get()
            print(topic, message)

            if topic == args.mqtt_topic_set_brightness:
                brightness = float(message)
                

            if topic == args.mqtt_topic_set_mode:
                mode = message
                obj.exit()




###############################################################################
#  Program Start Point
###############################################################################

# Argparse
parser = argparse.ArgumentParser()
parser.add_argument("--mqtt_server_ip", help="")
parser.add_argument("--mqtt_server_port", help="")
parser.add_argument("--mqtt_topic_set_brightness", help="")
parser.add_argument("--mqtt_topic_set_mode", help="")
args = parser.parse_args()

#  Init
sublist = []
sublist.append(args.mqtt_topic_set_brightness)
sublist.append(args.mqtt_topic_set_mode)
o = c_mqtt("192.168.178.52","1883",sublist)

#  Threads
t1= threading.Thread(target=Thread_MqttLoop)
t2= threading.Thread(target=Thread_MqttRecQueue)
t3= threading.Thread(target=Thread_Cube)

t1.start()
time.sleep(3)
t2.start()
time.sleep(1)
t3.start()