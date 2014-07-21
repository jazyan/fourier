from PIL import Image
import math
import numpy

orig = Image.open("am_goth.png")
new = Image.new( 'YCbCr', (orig.size[0], orig.size[1]), "black")
new2 = Image.new('YCbCr', (orig.size[0]/2, orig.size[1]/2), "black")

oldpix = orig.load()
print orig.size[0], orig.size[1]
newpix = new.load()
newpix2 = new2.load()

def ycbcr (rgb):
    (r, g, b) = rgb
    y = 0.299*float(r) + 0.587*float(g) + 0.114*float(b)
    cb = 128 - 0.168736*float(r) - 0.331264*float(g) + 0.5*float(b)
    cr = 128 + 0.5*float(r) - 0.418688*float(g) - 0.081312*float(b)
    return (int(y), int(cb), int(cr))

def replace (orig, new, l, w):
    for i in range(l):
        for j in range(w):
            new[i,j] = ycbcr(orig[i,j])

def downsample (old, new, l, w):
    for i in range(l):
        for j in range(w):
            if i%2 == 0 and j%2 == 0:
                new[i/2, j/2] = ycbcr(old[i,j])

downsample(oldpix, newpix2, orig.size[0], orig.size[1])
new2.show()
'''
newim = orig.convert('YCbCr')
newim.show()
print newim.getpixel((0,0))
orig.show()
print orig.getpixel((0,0))
test = Image.open("mona.png")
test = numpy.array(test)
test[:,:,0] *= 0
test[:,:,1] *= 0
test = Image.fromarray(test)
test.show()
'''
replace(oldpix, newpix, orig.size[0], orig.size[1])
orig.show()
new.show()
