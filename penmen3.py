from PIL import Image
import math
import numpy as np
import scipy as sc
import scipy.spatial
import time

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

def splitws (img):
    ctr = 0
    rows = []
    for i in range(len(img)):
        if sum(img[i])/255. > 1335:
            if i - ctr > 10:
                rows.append(img[ctr:i])
                ctr = i
    return rows

'''
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
'''

# generates h - off vertical shifts. h = w + off
def stagger (s, h, w, rownum):
    height = len(s) + 1
    ans = []
    for i in range(len(s[0]) - w):
        for j in range(height - h):
            x = s[j:(h + j), i:(i+w)]
            if float(np.count_nonzero(x))/float(h*w) < 0.67:
                #ans.append((np.count_nonzero(x), rownum, arr2int(x)))
                ans.append((np.count_nonzero(x), rownum, x))
    return ans

# basically XOR bits
def dist (v1, v2):
    tally = 0
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            tally += 1
    return tally

def dist2 (v1, v2):
    tally = 0
    for i in range(len(v1)):
        for j in range(len(v1[i])):
            if v1[i, j] != v2[i, j]:
                tally += 1
    return tally

def run (w, h):
    orig = Image.open("penmen2.png")
    orig = np.array(orig)
    if w == 20:
        orig = rem_borders(orig, 10, 12, 10, 20)
    else:
        orig = rem_borders(orig, 10, 12, 10, 25)
    sticks = splitws(orig)
    extract = [0 for i in range(30)]
    allex = []
    for i in range(30):
        print "ROW", i
        extract[i] = stagger (sticks[i], h, w, i)
        print "How many passed?", len(extract[i])
        allex = allex + extract[i]
    allex = sorted(allex, key = lambda x:x[0])
    allex_len = len(allex)
    print "ALLEX", allex[allex_len - 700][0], allex[allex_len-1][0]
    print "ALLEX LEN", allex_len
    print "AVERAGE", allex_len/30.
    answers = []
    for (i, ai) in enumerate(allex):
        print i
        ai0, ai1, ai2 = ai
        for j in range(i, min(i + 1000, allex_len)):
            aj0, aj1, aj2 = aj = allex[j]

            if dist2(ai2, aj2) < 120 and abs(ai1 - aj1) > 3:
                print "ROW", ai1, aj1
                print "AT SORT", ai0, aj0
                answers.append(ai)
                answers.append(aj)

    return answers

def param (w, h):
    timer = time.asctime(time.localtime(time.time()))
    start = float(timer[14:16]) + float(timer[17:19])/60.
    ans = run (w, h)
    print len(ans)
    if len(ans) <= 200:
        rows = []
        for i in range(len(ans)):
            if i % 2 == 0 and not((ans[i][1], ans[i+1][1]) in rows or (ans[i+1][1], ans[i][1]) in rows):
                img1 = ans[i][2]
                #img1 = int2arr(ans[i][2], h, w)
                ws = np.ones((h, 1))*255
                print "ROWS", ans[i][1], ans[i+1][1]
                img2 = ans[i+1][2]
                #img2 = int2arr(ans[i+1][2], h, w)
                rows.append((ans[i][1], ans[i+1][1]))
                view = np.concatenate((img1, ws, ws, ws, img2), axis = 1)
                view = Image.fromarray(view)
                view.show()
    else:
        for i in range(200):
            if i%2 == 0:
                test = Image.fromarray(int2arr(ans[i][2], h, w))
                test.show()
    timer2 = time.asctime(time.localtime(time.time()))
    finish = float(timer2[14:16]) + float(timer[17:19])/60.
    print "TIME TAKEN IN MIN:", finish - start

param (15, 52)