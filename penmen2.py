from PIL import Image
import math
import numpy as np
import scipy as sc

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

# generates h - off vertical shifts. h = w + off
def stagger (s, off, w, height):
    test = np.zeros((height - off, off, w))
    for i in range(len(s)):
        if i + off <= len(s):
            test[i] = s[i:i+off]
    return test

# generates h - off horizontal shifts
def off (s, num, n, off, w, height):
    test = np.zeros((height - off, off, w))
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
    height = len(row) + 1
    seg = np.hsplit(row, n)
    w = len(seg[0][0])
    off0 = [0 for i in range(n)]
    off1 = []
    for i in range(n):
        off0[i] = stagger(seg[i], h, w, height)
    for i in range(1, n):
        for j in range(1, w):
            off1.append(off(seg[i-1], j, seg[i], h, w, height))
    pieces = off0 + off1
    ans = [(i, piece[i]) for piece in pieces for i in range(height-h)]
    # filter by % whitespace
    ans = [(rownum, height, arr2int(i)) for (height, i) in ans if float(np.count_nonzero(i))/float(h*w) < 0.7]
    return ans

def arr2int (arr):
    ans = 2
    # left, right, up, down
    for j in range(len(arr)):
        for i in range(len(arr[j])):
            if arr[j][i] == 255.:
                ans = ans * 10 + 1
            else:
                ans *= 10
    return str(ans)

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

def splitws (img):
    ctr = 0
    rows = []
    for i in range(len(img)):
        if sum(img[i])/255. > 1335:
            if i - ctr > 10:
                rows.append(img[ctr:i])
                ctr = i
    return rows

def run (w, h):
    orig = Image.open("penmen2.png")
    orig = np.array(orig)
    if w == 10:
        orig = rem_borders(orig, 10, 12, 10, 20)
    elif w == 4:
        orig = rem_borders(orig, 10, 12, 10, 26)
    else:
        orig = rem_borders(orig, 10, 12, 10, 25)
    #sticks = np.vsplit(orig, 30)
    sticks = splitws(orig)
    test = Image.fromarray(sticks[6])
    test2 = Image.fromarray(sticks[25])
    test.show()
    test2.show()
    print "CHECKING", len(sticks)
    extract = [0 for i in range(30)]
    allex = []
    for i in range(30):
        print i
        print sticks[i].shape
        if w == 10:
            extract[i] = segments (sticks[i], 137, h, i)
        elif w == 4:
            extract[i] = segments (sticks[i], 1364/w, h, i)
        else:
            extract[i] = segments (sticks[i], 1365/w, h, i)
        print "How many passed?", len(extract[i])
        allex = allex + extract[i]
    allex = sorted(allex, key =lambda x:x[2])
    print "ALLEX LEN", len(allex)
    #checked = [(15, 0), (22, 7), (18, 15), (10, 3), (20, 13), (20, 2),
    #           (10, 1), (20, 23), (18, 8), (28, 4), (19, 18), (28, 18),
    #           (27, 13), (19, 13)]
    answers = []
    for i in range(len(allex)):
        print i
        for j in range(i, len(allex)):
            if offws(allex[i][2], allex[j][2]) < 50 and allex[i][0] != allex[j][0]:
                print "ROW", allex[i][0], allex[j][0]
                answers.append(allex[i])
                answers.append(allex[j])
        #if allex[i][2] == allex[i-1][2] and allex[i][0] != allex[i-1][0] and abs(allex[i][1] - allex[i-1][1]) <= 5: #and not((allex[i][0], allex[i-1][0]) in checked):
            #print "ROW", allex[i][0], allex[i-1][0]
            #answers.append(allex[i-1])
            #answers.append(allex[i])
    return answers

def offws (vec1, vec2):
    ans = 0
    for i in range(len(vec1)):
        if vec1[i] == vec2[i]:
            ans += 1
    return ans

def param (w, h):
    ans = run (w, h)
    print len(ans)
    if len(ans) <= 200:
        for i in range(len(ans)):
            if i%2 == 0:
                #print ans[i][1]
                j = Image.fromarray(int2arr(ans[i][2], h, w))
                j.show()
    else:
        for i in range(200):
            if i%2 == 0:
                test = Image.fromarray(int2arr(ans[i][2], h, w))
                test.show()
param (15, 52)
