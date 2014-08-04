from PIL import Image
import math
import numpy as np

orig = Image.open("am_goth.png")
new = Image.new( 'YCbCr', (orig.size[0], orig.size[1]), "black")
new2 = Image.new('YCbCr', (orig.size[0]/2, orig.size[1]/2), "black")

orig = np.array(orig)
print orig.shape
print type(orig)
new = np.array(new)
new2 = np.array(new2)

def ycbcr (pixels):
    r = pixels[:,:,0]
    g = pixels[:,:,1]
    b = pixels[:,:,2]
    y = 0.299*r + 0.587*g + 0.114*b
    cb = 128 - 0.168736*r - 0.331264*g + 0.5*b
    cr = 128 + 0.5*r - 0.418688*g - 0.081312*b
    return np.dstack((y, cb, cr))

test = ycbcr(orig).astype(int)
print test.shape
test = Image.fromarray(test)
test.show()

def replace (old):
    for i in xrange(len(old)):
        for j in xrange(len(old[i])):
            new[i,j] = ycbcr(old[i,j])

def downsample (old, new):
    for i in xrange(len(old)):
        for j in xrange(len(old[i])):
            if i%2 == 0 and j%2 == 0:
                new[i/2, j/2] = ycbcr(old[i,j])

def upsample(mini_img):
    out = []
    for row in mini_img:
        doubled_row = sum([[i]*2 for i in row], [])
        out.append(doubled_row)
        out.append(doubled_row)

    return out

downsample(oldpix, newpix2, orig.size[0], orig.size[1])
new2.show()

replace(oldpix, newpix, orig.size[0], orig.size[1])
orig.show()
new.show()
