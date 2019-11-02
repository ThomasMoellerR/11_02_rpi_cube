
import util.utilcube as utilcube
import util.spicube as spicube
import numpy as np
import time
import itertools

class blocks:
    def __init__(self):
        self.ex = False

    def exit(self):
        self.ex = True



    def full_color_change(self):

        grad = utilcube.get_grad_array()

        while True:
            for g in grad:
                r,g,b = utilcube.grad_to_rgb(g)
                a = utilcube.alle(r,g,b)

                spicube.schreiben(a)
                time.sleep(1)

                if self.ex: return "exit"




