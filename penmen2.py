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
    ans = [(i, piece[i]) for piece in pieces for i in range(57-h)]
    # filter by % whitespace
    ans = [(rownum, height, arr2int(i)) for (height, i) in ans if float(np.count_nonzero(i))/float(h*w) < 0.75]
    return ans

def arr2int (arr):
    ans = 2
    # left, right, up, down
    bbor = [1, 1, 1, 1]
    for j in range(len(arr)):
        for i in range(len(arr[j])):
            if arr[j][i] == 255.:
                ans = ans * 10 + 1
            else:
                ans *= 10
                '''
                if j == 0:
                    if bbor[2] == 0:
                        bbor[2] = 1
                if j == (len(arr) - 1):
                    if bbor[3] == 0:
                        bbor[3] == 1
                if i == 0:
                    if bbor[0] == 0:
                        bbor[0] = 1
                if i == (len(arr[j]) - 1):
                    if bbor[1] == 0:
                        bbor[1] = 1
                '''
    bb = (bbor[0] or bbor[1]) or (bbor[2] or bbor[3])
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

def run (w, h):
    orig = Image.open("penmen2.png")
    orig = np.array(orig)
    if w == 10:
        orig = rem_borders(orig, 15, 15, 10, 20)
    elif w == 4:
        orig = rem_borders(orig, 15, 15, 10, 26)
    else:
        orig = rem_borders(orig, 15, 15, 10, 25)
    sticks = np.vsplit(orig, 30)
    extract = [0 for i in range(30)]
    allex = []
    for i in range(30):
        print i
        if w == 10:
            extract[i] = segments (sticks[i], 137, h, i)
        elif w == 4:
            extract[i] = segments (sticks[i], 1364/w, h, i)
        else:
            extract[i] = segments (sticks[i], 1365/w, h, i)
        print "How many passed?", len(extract[i])
        allex = allex + extract[i]
        #for i in range(20, 40):
            #(a, b, ans) = allex[i]
            #check = Image.fromarray(int2arr(ans, h, w))
            #check.show()
    allex = sorted(allex, key =lambda x:x[2])
    print "ALLEX LEN", len(allex)
    #(a, b, test) = allex[0]
    #(a1, b1, test2) = allex[1]
    #view = Image.fromarray(int2arr(test, 40, 15))
    #view2 = Image.fromarray(int2arr(test, 40, 15))
    #view.show()
    #view2.show()
    answers = []
    #checked = [(15, 0), (22, 7), (18, 15), (10, 3), (20, 13), (20, 2),
    #           (10, 1), (20, 23), (18, 8), (28, 4), (19, 18), (28, 18),
    #           (27, 13), (19, 13)]
    for i in range(1, len(allex)):
        if allex[i][2] == allex[i-1][2] and allex[i][0] != allex[i-1][0]: #and not((allex[i][0], allex[i-1][0]) in checked) and abs(allex[i][1] - allex[i-1][1]) <= 10:
            print "ROW", allex[i][0], allex[i-1][0]
            answers.append(allex[i-1])
            answers.append(allex[i])
    return answers

def param (w, h):
    ans = run (w, h)
    print len(ans)
    if len(ans) <= 200:
        for i in range(len(ans)):
            if i%2 == 0:
                j = Image.fromarray(int2arr(ans[i][2], h, w))
                j.show()
    else:
        for i in range(len(ans)):
            if ans[i][0] == 19 and ans[i-1][0] == 16:
                test = Image.fromarray(int2arr(ans[i][2], h, w))
                test2 = Image.fromarray(int2arr(ans[i-1][2], h, w))
                test.show()
                test2.show()

param (15, 40)
