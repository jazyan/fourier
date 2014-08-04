from PIL import Image
import math
import numpy as np
import scipy as sc
import sys

#fin = open(sys.argv[1], 'r')
#SCRIPT = int(fin.read())
#fout = open(sys.argv[2], 'w')
SCRIPT = 40

orig = Image.open("penmen2.png")
orig = np.array(orig)

# removes whitespace from the sides of the image
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

# generates h - off vertical shifts. h = w + off
def stagger (s, off, w):
    test = np.zeros((57 - off, off, w))
    for i in range(len(s)):
        if i + off <= len(s):
            test[i] = s[i:i+off]
    return test

# generates h - off horizontal shifts
def off (s, num, n, off, w):
    test = np.zeros((57 - off, off, w))
    for i in range(len(s)):
        if i + off <= len(s):
            test[i] = s[i:i+off]
            hold = n[i:i+off, 0:num]
            hold2 = test[i, :, 1:(w-num)]
            test[i, :, (w-num):w] = hold
            test[i, :, 0:(w-num-1)] = hold2
    return test

# create n segments of height h
def segments (row, n, h, rownum):
    seg = np.hsplit(row, n)
    w = len(seg[0][0])
    off0 = [0 for i in range(n)]
    off1 = []
    for i in range(n):
        off0[i] = stagger(seg[i], h, w)
    for i in range(1, n):
        for j in range(1, w):
            off1.append(off(seg[i-1], j, seg[i], h, w))
    pieces = off0 + off1
    ans = [piece[i] for piece in pieces for i in range(57-h)]
    # filter by % whitespace
    ans = [arr2int(i) for i in ans if float(np.count_nonzero(i))/float(h*w) < 0.8]
    #ans = [(rownum, arr2int(i)) for i in ans if float(np.count_nonzero(i))/float(h*w) < 0.9]
    return ans

def arr2int (arr):
    ans = 2
    for row in arr:
        for i in row:
            if i == 255.:
                ans = ans * 10 + 1
            else:
                ans *= 10
    return ans
    #ans = np.array_str(arr)
    #ans = ans.replace("[", "").replace("]", "").replace("\n", "")
    #ans = ans.replace("255", "1").replace(" ", "").replace(".", "2")
    # add 2 in beginning so converting to int doesn't lose first 0
    #ans = '2' + ans
    #return int(ans)

def int2arr (i, w, h):
    ans = str(i)
    # remove first 2
    ans = ans[1:]
    ans = ans.replace("2", " ").replace("1", "255.").replace("0", "0.")
    ans = np.fromstring(ans, dtype=float, sep=' ')
    ans = np.reshape(ans, (w, h))
    return ans

def comp_rows (row1, row2):
    ans = []
    for r1 in row1:
        for r2 in row2:
            if int(np.count_nonzero(r1)) == int(np.count_nonzero(r2)):
                #print r1, r2
                if np.array_equal(r1, r2):
                    ans.append(r1)
                    ans.append(r2)
    return ans

# change to 20 if div by 10
orig = rem_borders(orig, 15, 15, 10, 20)
sticks = np.vsplit(orig, 30)

extract = [0 for i in range(30)]
allex = []
for i in range(30):
    print i
    extract[i] = segments (sticks[i], 137, 40, i)
    allex = allex + extract[i]


allex = sorted(allex, key =lambda x:x[1])
print "ALLEX LEN", len(allex)
answers = []
for i in range(1, len(allex)):
    if allex[i][1] == allex[i-1][1] and allex[i][0] != allex[i-1][0]:
        answers.append(allex[i-1])
        answers.append(allex[i])

print "ANSWERS", len(answers)
'''
for i in answers:
    print i[0]
    j = Image.fromarray(int2arr(i[1], 40, 10))
    j.show()
'''
