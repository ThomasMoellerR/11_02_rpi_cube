
import util.utilcube as utilcube
import util.spicube as spicube
import numpy as np
import time
import itertools

class snake:
    def __init__(self, dim):
        self.dim = dim # dimension
        self.m = np.zeros((dim,dim,dim,1), dtype=np.uint8) # belegte felder
        self.ex = False

    def __del__(self):
        pass

    def __str__(self):
        return "cube_random"

    def exit(self):
        self.ex = True

    def gueltiges_feld(self, x ,y, z):
        if x < self.dim and y < self.dim and z < self.dim:
            if self.m[x][y][z] == 0:
                return 1
            else:
                return 0
        else:
            return 0

    def belege_feld(self, x ,y, z):
        if x < self.dim and y < self.dim and z < self.dim:
            self.m[x][y][z] = 1

    def show(self):
        a = utilcube.alle(0,0,0)

        # start position
        x = 0
        y = 0
        z = 0

        state = "rechts"

        delay = 0.05

        count = 0


        while True:
            if self.ex: return "exit"

            #print(count, x,y,z, state)

            while True:
                if self.ex: return "exit"

                if state == "rechts":
                    if (self.gueltiges_feld(x,y,z)):
                        self.belege_feld(x,y,z)
                        a[x][y][z][0] = 255

                        spicube.schreiben(a)
                        time.sleep(delay)
                        if self.ex: return "exit"

                        x += 1
                        break
                    else:
                        x -= 1
                        y += 1
                        state = "hoch"
                        break


                if state == "hoch":
                    if (self.gueltiges_feld(x,y,z)):
                        self.belege_feld(x,y,z)
                        a[x][y][z][0] = 255

                        spicube.schreiben(a)
                        time.sleep(delay)
                        if self.ex: return "exit"

                        y += 1
                        break
                    else:
                        state = "links"
                        y -= 1
                        x -= 1
                        break


                if state == "links":
                    if (self.gueltiges_feld(x,y,z)):
                        self.belege_feld(x,y,z)
                        a[x][y][z][0] = 255

                        spicube.schreiben(a)
                        time.sleep(delay)
                        if self.ex: return "exit"

                        x -= 1
                        break
                    else:
                        state = "runter"
                        x += 1
                        y -= 1
                        break



                if state == "runter":
                    if (self.gueltiges_feld(x,y,z)):
                        self.belege_feld(x,y,z)
                        a[x][y][z][0] = 255

                        spicube.schreiben(a)
                        time.sleep(delay)
                        if self.ex: return "exit"

                        y -= 1
                        break
                    else:
                        state = "rechts"
                        y += 1
                        x += 1
                        break



            count = np.count_nonzero(a)

            if count % 144 == 0:
                z += 1
                x = 0
                y = 0
                state = "rechts"
