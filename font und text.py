from PIL import Image, ImageDraw, ImageFont
import numpy as np


img = Image.new('RGB', (200, 12), color = (0, 0, 0))

font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", 28, encoding="unic")

d = ImageDraw.Draw(img)
d.text((0,0), "Hello World", fill=(255,0,0))


 

a = np.array(img)
b = a[0:12,0:12,:]


im = Image.fromarray(b)
im.save("your_file.jpeg")
 

