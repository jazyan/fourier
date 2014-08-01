from PIL import Image
import math
import numpy as np
import scipy as sc
import sys
import time
import datetime

fin = open(sys.argv[1], 'r')
SCRIPT = int(fin.read())
fout = open(sys.argv[2], 'w')

# there are 30 * 35 stick men

orig = Image.open("penmen2.png")
orig = np.array(orig)

def rem_borders (img, u, d, l, r):
    for i in range(u):
        img = sc.delete(img, 0, 0)
    img = np.flipud(img)
    for i in range(d):
        img = sc.delete(img, 0, 0)
    img = np.flipud(img)
    for i in range(l):
        img = sc.delete(img, 0, 1)
    img = np.fliplr(img)
    for i in range(r):
        img = sc.delete(img, 0, 1)
    img = np.fliplr(img)
    return img

def split (img, x, y):
    (w, l) = img.shape
    ans = np.zeros((w*l/(x*y), x, y))
    newRow = []
    for i in xrange(0, len(img)):
        k = i/x * (l/y)
        for j in xrange(0, len(img[i])):
            newRow.append(orig[i][j])
            if (j+1) % y == 0:
                ans[k][i%x] = newRow
                newRow = []
                k += 1
    return ans

def stagger (s, off, w, hshift):
    test = np.zeros((hshift, off, w))
    for i in range(len(s)):
        if i + off <= len(s):
            test[i] = s[i:i+off]
    return test

def off (s, num, n, off, w, hshift):
    test = np.zeros((hshift, off, w))
    for i in range(len(s)):
        if i + off <= len(s):
            test[i] = s[i:i+off]
            hold = n[i:i+off, 0:num]
            hold2 = test[i, :, 1:(w-num)]
            test[i, :, (w-num):w] = hold
            test[i, :, 0:(w-num-1)] = hold2
    return test

def segments (row, n, h):
    # split into n segments with height h
    seg = np.hsplit(row, n)
    w = len(seg[0][0])
    off0 = []
    off1 = []
    for i in range(n):
        off0.append(stagger(seg[i], h, w, 57-h))
    for i in range(1, n):
        for j in range(1, w):
            off1.append(off(seg[i-1], j, seg[i], h, w, 57-h))
    pieces = off0 + off1
    ans = [piece[i] for piece in pieces for i in range(57-h)]
    # filter by little whitespace
    ans = [i for i in ans if float(np.count_nonzero(i))/600. < 0.6]
    return ans

# change to 20 if div by 10
orig = rem_borders(orig, 15, 15, 10, 20)
sticks = np.vsplit(orig, 30)
#print sticks[0].shape

extract = [0 for i in range(30)]
for i in range(30):
    extract[i] = segments (sticks[i], 137, SCRIPT)
# NOTE 42 has no same elements
print len(sticks[0][0])

def comp_rows (row1, row2):
    ans = []
    #print "GOAL", len(row1)
    for r1 in range(len(row1)):
        for r2 in range(len(row2)):
            if int(np.count_nonzero(row1[r1])) == int(np.count_nonzero(row2[r2])):
                #print r1, r2
                if np.array_equal(row1[r1], row2[r2]):
                    #print "WAT"
                    ans.append(row1[r1])
                    ans.append(row2[r2])
    return ans

for i in range(30):
    for j in range(i+1, 30):
        print SCRIPT, ": comparing rows", i, j
        x = comp_rows (extract[i], extract[j])
        fout.write(str(x) + "\n")
    print "DONE", SCRIPT, datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
