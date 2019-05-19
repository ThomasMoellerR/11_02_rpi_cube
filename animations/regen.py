
import util.utilcube as utilcube
import util.spicube as spicube
import numpy as np
import time
import itertools

class regen:
    def __init__(self):
        print("object regen constructor")

    def __del__(self):
        print("object regen destructor")



    def show(self):
        a = utilcube.alle(0,0,0)

        # Blauer Himmel
        for x, y in itertools.product(range(12), range(12)):
            a[x][y][11][0] = 255
            a[x][y][11][1] = 255
            a[x][y][11][2] = 255
        spicube.schreiben(a)

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

                spicube.schreiben(a)
                time.sleep(0.05) # 0.01




