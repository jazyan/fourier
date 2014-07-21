from PIL import Image
import math
import numpy

orig = Image.open("am_goth.png")
new = Image.new( 'YCbCr', (orig.size[0], orig.size[1]), "black")

pixels1 = orig.load()
#pixels1 = Image.fromarray(pixels1)
#pixels1.show()
pixels2 = new.load()

def ycbcr (rgb):
    (r, g, b) = rgb
    y = 0.299*float(r) + 0.587*float(g) + 0.114*float(b)
    # print y
    cb = 128 - 0.168736*float(r) - 0.331264*float(g) + 0.5*float(b)
    # print cb
    cr = 128 + 0.5*float(r) - 0.418688*float(g) - 0.081312*float(b)
    return (int(y), int(cb), int(cr))

def replace (orig, new, l, w):
    for i in range(l):
        for j in range(w):
            new[i,j] = ycbcr(orig[i,j])

def upsample(mini_img):
    out = []
    for row in mini_img:
        doubled_row = sum([[i]*2 for i in row], [])
        out.append(doubled_row)
        out.append(doubled_row)

    return out

replace(pixels1, pixels2, orig.size[0], orig.size[1])
orig.show()
new.show()