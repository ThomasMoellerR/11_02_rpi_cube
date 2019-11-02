import numpy as np
import itertools
import random
import colorsys

def alle(r,g,b):
    m = np.zeros((12,12,12,3), dtype=np.uint8)
    for x, y, z in itertools.product(range(12), range(12), range(12)):
        m[x][y][z][0] = r
        m[x][y][z][1] = g
        m[x][y][z][2] = b
    return m

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
    
def random_coordinates():
    x = random.randint(0, 11)
    y = random.randint(0, 11)
    z = random.randint(0, 11)
    return x,y,z

def random_color():
    grad = random.choice(get_grad_array())
    color = colorsys.hsv_to_rgb(grad/360, 1.0, 1.0)
    color = np.asarray(color)
    color *= 255
    r = color[0]
    g = color[1]
    b = color[2]
    return r,g,b