
import util.utilcube as utilcube
import util.spicube as spicube
import numpy as np
import time
import itertools
import random
import colorsys

class cube_random:
    def __init__(self):
        print("cube_random constructor")
        self.ex = False

    def __del__(self):
        print("cube_random destructor")

    def __str__(self):
        return "cube_random"

    def exit(self):
        self.ex = True

    def random1(self):
        a = utilcube.alle(0,0,0)
        while True:
            coordinates = utilcube.random_coordinates()
            color = utilcube.random_color()
            a[coordinates[0]][coordinates[1]][coordinates[2]][0] = color[0]
            a[coordinates[0]][coordinates[1]][coordinates[2]][1] = color[1]
            a[coordinates[0]][coordinates[1]][coordinates[2]][2] = color[2]
            spicube.schreiben(a)
            time.sleep(0.1)
            if self.ex: return "exit"


    def random2(self):
        farben = np.arange(0,360,60)
        a = utilcube.alle (0, 0, 0)
        while True:
            for x, y, z in itertools.product(range(12), range(12), range(12)):
                grad = random.choice(farben)
                color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
                color = np.asarray(color)
                color *= 255

                a[x][y][z][0] = color[0]
                a[x][y][z][1] = color[1]
                a[x][y][z][2] = color[2]

            spicube.schreiben(a)
            time.sleep(0.0)
            if self.ex: return "exit"

 
    def random3(self):
        a = utilcube.alle(0,0,0)
        list_coordinates = []

        number = 200

        for i in range(number):
            coordinates = utilcube.random_coordinates()
            color = utilcube.random_color()

            list_coordinates.append(coordinates)
                      
            a[coordinates[0]][coordinates[1]][coordinates[2]][0] = color[0]
            a[coordinates[0]][coordinates[1]][coordinates[2]][1] = color[1]
            a[coordinates[0]][coordinates[1]][coordinates[2]][2] = color[2]

            spicube.schreiben(a)


        while True:

            for i in range(number):
                

                # alte koordinate holen und löschen, led aus
                coordinate = list_coordinates[i]

                a[coordinate[0]][coordinate[1]][coordinate[2]][0] = 0
                a[coordinate[0]][coordinate[1]][coordinate[2]][1] = 0
                a[coordinate[0]][coordinate[1]][coordinate[2]][2] = 0
    
                # neue koordinate holen, in liste speichern, led setzen
                coordinate = utilcube.random_coordinates()
                list_coordinates[i] = coordinate

                color = utilcube.random_color()

                a[coordinate[0]][coordinate[1]][coordinate[2]][0] = color[0]
                a[coordinate[0]][coordinate[1]][coordinate[2]][1] = color[1]
                a[coordinate[0]][coordinate[1]][coordinate[2]][2] = color[2]

                spicube.schreiben(a)
                time.sleep(1)
                if self.ex: return "exit"
    