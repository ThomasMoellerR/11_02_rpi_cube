
import spidev
import numpy as np

def schreiben (m):

    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.mode = 2
    spi.cshigh = False
    spi.max_speed_hz = 40000000 # Max 40 MHz mit uC möglich

    r = m[:,:,:,0]
    g = m[:,:,:,1]
    b = m[:,:,:,2]
    r = r.flatten()
    g = g.flatten()
    b = b.flatten()

    spi.writebytes(r.tolist())
    spi.writebytes(g.tolist())
    spi.writebytes(b.tolist())
    spi.close()