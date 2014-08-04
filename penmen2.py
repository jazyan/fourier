from PIL import Image
import math
import numpy as np
import scipy as sc
import sys

#TODO: fix int2arr, play around with good size

#fin = open(sys.argv[1], 'r')
#SCRIPT = int(fin.read())
#fout = open(sys.argv[2], 'w')
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
    ans = [(rownum, arr2int(i)) for i in ans if float(np.count_nonzero(i))/float(h*w) < 0.9]
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

def int2arr (i, w, h):
    ans = str(i)
    # remove first 2
    ans = ans[1:]
    acc = []
    for i in ans:
        if i == "1":
            acc.append(255.)
        else:
            acc.append(0.)
    answer = np.array(acc)
    answer = np.reshape(answer, (w, h))
    return answer

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

def run (w, h):
    orig = Image.open("penmen2.png")
    orig = np.array(orig)
    if w == 10:
        orig = rem_borders(orig, 15, 15, 10, 20)
    else:
        orig = rem_borders(orig, 15, 15, 10, 25)
    sticks = np.vsplit(orig, 30)
    extract = [0 for i in range(30)]
    allex = []
    for i in range(30):
        print i
        if w == 10:
            extract[i] = segments (sticks[i], 137, h, i)
        else:
            extract[i] = segments (sticks[i], 1365/w, h, i)
        allex = allex + extract[i]
    allex = sorted(allex, key =lambda x:x[1])
    print "ALLEX LEN", len(allex)
    answers = []
    for i in range(1, len(allex)):
        if allex[i][1] == allex[i-1][1] and allex[i][0] != allex[i-1][0]:
            print "ROW", allex[i][0], allex[i-1][0]
            answers.append(allex[i-1])
            answers.append(allex[i])
    return answers

def param (w, h):
    ans = run (w, h)
    print len(ans)
    if len(ans) < 20:
        for i in ans:
            j = Image.fromarray(int2arr(i[1], h, w))
            j.show()
    else:
        for i in range(len(ans)):
            if ans[i][0] == 19:
                test = Image.fromarray(int2arr(ans[i][1], h, w))
                test2 = Image.fromarray(int2arr(ans[i+1][1], h, w))
                test.show()
                test2.show()

param (5, 41)
