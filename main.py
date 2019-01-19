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

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)

GPIO.output(23, GPIO.LOW)
GPIO.output(23, GPIO.HIGH)


brightness = 1.0
mode = "regen"
mode_changed = False

def schreiben (m):

    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.mode = 2
    spi.cshigh = False
    spi.max_speed_hz = 40000000 # Max 40 MHz mit uC möglich

    global brightness

    if brightness == 0:
        m = np.zeros((12,12,12,3), dtype=np.uint8)


    #wait = 0.000
    r = m[:,:,:,0]
    g = m[:,:,:,1]
    b = m[:,:,:,2]
    r = r.flatten()
    g = g.flatten()
    b = b.flatten()

    #time.sleep(wait)
    spi.writebytes(r.tolist())
    #time.sleep(wait)
    spi.writebytes(g.tolist())
    #time.sleep(wait)
    spi.writebytes(b.tolist())
    #time.sleep(wait)
    spi.close()



def alle(r,g,b):
    m = np.zeros((12,12,12,3), dtype=np.uint8)
    for x, y, z in itertools.product(range(12), range(12), range(12)):
        m[x][y][z][0] = r
        m[x][y][z][1] = g
        m[x][y][z][2] = b
    return m

def x_to_pi(x):
    return (x / 11.0) * (2.0*math.pi)

def calculate_sin(x):
    y = x_to_pi(x)
    sin = math.sin(y)
    sin_half= sin / 2
    sin_half_plus_offset = sin_half + 0.5
    mal11= sin_half_plus_offset * 11
    gerundet = round(mal11 + 0.001)
    return int(gerundet)

def conv (m):
    a = np.zeros((12,12,12,3), dtype=np.uint8)
    for x, y, z in itertools.product(range(12), range(12), range(12)):
        a[11-y][11-x][z][0] = m[x][y][z][0]
        a[11-y][11-x][z][1] = m[x][y][z][1]
        a[11-y][11-x][z][2] = m[x][y][z][2]
    return a
"""
def display_image(img):

    len = img.shape[1]
    m = np.zeros((12,len+24,3), dtype=np.uint8)

    print(m.shape)
    print(img.shape)
    #m[0:len, 0:len] = img[0:len, 0:len]
    #m[0:0, len:len+12] = img[0:0, 0:len]

    save_image(image,"/home/pi/your_file.jpeg")

    print(m.shape)
    print(img.shape)

    #width = np.arange(0,50,1)


    for w in width:
        s = img[0:0+12, w:w+12]
        #s = s / 255
        #s = s * 10

        a = alle(0,0,0)

        suchbereich = range(12)
        for x, y in itertools.product(suchbereich, suchbereich):
            for depth in range(3):
                a[11-y][depth][x][0] = s[11-x][11-y][0]


        schreiben(a)
        time.sleep(0.05)
"""

def create_image(text):
    img = Image.new('RGB', (200, 12), color = (0, 0, 0))
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 12, encoding="unic")
    d = ImageDraw.Draw(img)
    ret = d.text((0,0), text, font=font, fill=(255,0,0))
    img = np.array(img)
    len = font.getsize(text)[0]
    img = img[0:len, 0:len]
    return img

def save_image(image, path):
    im = Image.fromarray(image)
    im.save(path)

def get_grad_array():
    return np.arange(0,360,60)

def grad_to_rgb(grad):
    color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
    color = np.asarray(color)
    color *= 255
    r = color[0]
    g = color[1]
    b = color[2]
    return r,g,b

def random_color():
    grad = random.choice(get_grad_array())
    color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
    color = np.asarray(color)
    color *= 255
    r = color[0]
    g = color[1]
    b = color[2]
    return r,g,b

def cube_random_color():
    a = alle (0, 0, 0)
    for x, y, z in itertools.product(range(12), range(12), range(12)):
        r,g.b = random_color()
        a[x][y][z][0] = r
        a[x][y][z][1] = g
        a[x][y][z][2] = b
    return a

def random_coordinates():
    x = random.randint(0, 11)
    y = random.randint(0, 11)
    z = random.randint(0, 11)
    return x,y,z

def create_lookUpTable():
    lookUpTable = {}
    counter = 0
    for x in range(12):
        for y in range(12):
            for z in range(12):
                lookUpTable[counter] = x,y,z
                counter += 1
    return lookUpTable


"""
a = alle(0,0,0)
a[0][0][0][0] = 255
schreiben(a)
"""


"""
a = alle(0,0,0)
schreiben(a)

while True:
    for grad in get_grad_array():
        r,g,b = grad_to_rgb(grad)
        elements = np.arange(1728)
        np.random.shuffle(elements)
        lookUpTable = create_lookUpTable()
        for i in elements:
            x,y,z = lookUpTable[i]
            del lookUpTable[i]
            a[x][y][z][0] = r
            a[x][y][z][1] = g
            a[x][y][z][2] = b
            schreiben(a)
            time.sleep(0.0)
"""











"""
a = alle(0,0,0)
schreiben(a)
"""

def zeit():

    while True:
        actual_time = time.strftime("%H:%M")


        img = Image.new('RGB', (200, 12), color = (0, 0, 0))
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 12, encoding="unic") #font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 12, encoding="unic")
        d = ImageDraw.Draw(img)
        d.text((0,0), "    " + actual_time, font=font, fill=(0,0,255)) # d.text((0,0), "   Hello World", font=font, fill=(255,0,0))
        t = np.array(img)



        width = np.arange(0,50,1)

        for w in width:
            s = t[0:0+12, w:w+12]
            #s = s / 255
            #s = s * 10

            a = alle(0,0,0)

            suchbereich = range(12)
            for x, y in itertools.product(suchbereich, suchbereich):
                for depth in range(1):
                    a[11-y][depth][x][0] = s[11-x][11-y][0]
                    a[11-y][depth][x][1] = s[11-x][11-y][1]
                    a[11-y][depth][x][2] = s[11-x][11-y][2]


            schreiben(a)
            time.sleep(0.05)


def regen():
    a = alle(0,0,0)

    # Blauer Himmel
    for x, y in itertools.product(range(12), range(12)):
        a[x][y][11][0] = 255
        a[x][y][11][1] = 255
        a[x][y][11][2] = 255
    schreiben(a)

    # Liste mit Himmels-Koordinaten
    himmel_koor = []
    for x, y in itertools.product(range(12), range(12)): himmel_koor.append((x,y))

    np.random.shuffle(himmel_koor)

    for x, y in himmel_koor:
        time.sleep(0.5)
        for i in reversed(range(11)):
            a[x][y][i+1][0] = 0
            a[x][y][i+1][1] = 0
            a[x][y][i+1][2] = 0

            a[x][y][i][0] = 255
            a[x][y][i][1] = 255
            a[x][y][i][2] = 255

            if i == 0:
                a[x][y][i][0] = 255
                a[x][y][i][1] = 255
                a[x][y][i][2] = 255

            global mode_changed
            if mode_changed == True:
                mode_changed = False
                return True
            schreiben(a)
            time.sleep(0.01)

    return False


def prog_random():
    a = alle(0,0,0)
    while True:
        coordinates = random_coordinates()
        color = random_color()
        a[coordinates[0]][coordinates[1]][coordinates[2]][0] = color[0]
        a[coordinates[0]][coordinates[1]][coordinates[2]][1] = color[1]
        a[coordinates[0]][coordinates[1]][coordinates[2]][2] = color[2]
        global mode_changed
        if mode_changed == True:
            mode_changed = False
            return True
        schreiben(a)
        time.sleep(0.1)

    return False


def prog_random2():
    farben = np.arange(0,360,60)
    a = alle (0, 0, 0)
    while True:
        suchbereich = range(12)
        for x, y, z in itertools.product(range(12), range(12), range(12)):
            grad = random.choice(farben)
            color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
            color = np.asarray(color)
            color *= 255

            a[x][y][z][0] = color[0]
            a[x][y][z][1] = color[1]
            a[x][y][z][2] = color[2]

        global mode_changed
        if mode_changed == True:
            mode_changed = False
            return True
        schreiben(a)
        time.sleep(0.0)

    return False

def grid_sin(x):
    a = np.array([0,1,2,3,4,5,6,7,8,9,10,11,10,9,8,7,6,5,4,3,2,1])
    return a[x]

def sinus():
    list_t = np.arange(0,22,1)
    list_a = np.array([])

    a = alle (0, 0, 0)

    for t in list_t:
        list_a = np.append(list_a, grid_sin(t))

    color = (255,0,0)

    for x in range(12):
        z = int(list_a[x])
        a[x][0][z][0] = 255
        schreiben(a)
        time.sleep(1)



def distance(x,y):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))


def kreis():
    a = alle(0,0,0)



    startpunkt = (0, 0, 0)
    list = []

    for x, y, z in itertools.product(range(12), range(12), range(12)):
        b = (x, y, z)
        list.append((x,y,z,distance(startpunkt,b)))




    np_array = np.asarray(list)
    np_array = np.array(sorted(np_array, key=lambda x: x[3]))
    #print(np_array.shape)


    koor = np_array[:,:3]
    koor = koor.squeeze()

    dist = np_array[:,3:]
    dist = dist.squeeze()
    #print(np.unique(dist))


    for t in np.arange(0.0, 12.0, 0.5):

        list_kreis = []
        for i in range(dist.size):
            if dist[i] <= t:
                list_kreis.append(koor[i])

        for i in list_kreis:

            x, y, z = i
            x = int (x)
            y = int (y)
            z = int (z)

            a[x][y][z][0] = 255




        schreiben(a)

        time.sleep(1)

    print("fertig")

    while True:
        pass

def thread1():

    while True:
        if mode == "regen":
            ret = regen()

        elif mode == "prog_random":
            prog_random()

        elif mode == "prog_random2":
            prog_random2()

        elif mode == "kreis":
            kreis()

        else:
            pass




def thread2():
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

t1.start()
t2.start()



#regen()
"""
counter = 0
while True:
    a = alle(255,0,0)
    schreiben(a)
    #print(counter)
    #counter += 1
"""


"""
counter = 0
while True:
    a = alle(255,0,255)
    schreiben(a)
    print(str(counter))
    counter += 1
"""


#a = cube_random_color()
#schreiben(a)











#image = create_image("hallo thomas")

#display_image(image)

#save_image(image,"/home/pi/your_file.jpeg")

"""
while True:

    for i in range(12):
        a = alle(0,0,0)
        a[i][i][i][0] = 255
        schreiben(a)
"""


"""
a = np.zeros((12,120,3), dtype=np.uint8)
for x in range(12):
        a[x][calculate_sin(x)+ 12][0] = 255


im = Image.fromarray(a)
im.save("/home/pi/your_file.jpeg")




im = Image.open("/home/pi/your_file.jpeg")
t = np.array(im)



while True:
    width = np.arange(0,50,1)

    for w in width:
        s = t[0:0+12, w:w+12]
        #s = s / 255
        s = s * 10

        a = alle(0,0,0)

        suchbereich = range(12)
        for x, y in itertools.product(suchbereich, suchbereich):
            for depth in range(3):
                a[11-y][depth][x][0] = s[11-x][11-y][0]


        schreiben(a)
        time.sleep(0.05)


"""



"""
while True:
    for i in np.arange(0,360,60):
        #print(i)

        grad = i
        color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
        color = np.asarray(color)
        color *= 255

        suchbereich = range(12)
        for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
            matrix[x][y][z][0] = color[0]
            matrix[x][y][z][1] = color[1]
            matrix[x][y][z][2] = color[2]

        #matrix[0][0][0][0] = 255
        #matrix[0][0][0][1] = 255
        #matrix[0][0][0][2] = 255

        schreiben(matrix)
        #time.sleep(0.5)
"""


"""
while True:
    ra = range(12)
    for x, y, z in itertools.product(ra, ra, ra):
        a = alle(0,0,0)
        a[x][y][z][2] = 255
        schreiben(a)
        #time.sleep(0.5)


    #matrix[0][0][0][0] = 255
    #matrix[0][0][0][1] = 255
    #matrix[0][0][0][2] = 255


    #time.sleep(0.5)
"""

"""
while True:
    for c in range(3):
        for z in range(12):
            a = alle(0,0,0)
            for x, y in itertools.product(range(12), range(12)):
                a[x][y][z][c] = 30
            schreiben(a)
"""



#random.randint(0, 5)


"""
farben = np.arange(0,360,60)
a = alle (0, 0, 0)
while True:
    suchbereich = range(12)
    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        grad = random.choice(farben)
        color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
        color = np.asarray(color)
        color *= 100

        a[x][y][z][0] = color[0]
        a[x][y][z][1] = color[1]
        a[x][y][z][2] = color[2]

    schreiben(a)
"""




"""
for i in np.arange(0,255,1):
    print(i)
    suchbereich = range(12)
    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        matrix[x][y][z][0] = i
        matrix[x][y][z][1] = 0
        matrix[x][y][z][2] = 0


    schreiben(matrix)
    time.sleep(0.1)
"""


"""
for i in np.arange(0,255,1):
    print(i)
    suchbereich = range(12)
    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        matrix[x][y][z][0] = i
        matrix[x][y][z][1] = 0
        matrix[x][y][z][2] = 0


    schreiben(matrix)
    time.sleep(0.1)
"""

"""
while True:
    suchbereich = range(12)
    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        matrix[x][y][z][0] = 255
        matrix[x][y][z][1] = 0
        matrix[x][y][z][2] = 0


    schreiben(matrix)


    time.sleep(0.1)

    #while True:
        #pass
"""

"""
suchbereich = range(12)

while True:
    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        matrix[x][y][z][0] = 255
        matrix[x][y][z][1] = 0
        matrix[x][y][z][2] = 0
    schreiben(matrix)
    #time.sleep(0.1)

    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        matrix[x][y][z][0] = 0
        matrix[x][y][z][1] = 255
        matrix[x][y][z][2] = 0
    schreiben(matrix)
    #time.sleep(0.1)

    for x, y, z in itertools.product(suchbereich, suchbereich, suchbereich):
        matrix[x][y][z][0] = 0
        matrix[x][y][z][1] = 0
        matrix[x][y][z][2] = 255
    schreiben(matrix)
    #time.sleep(0.1)
"""
