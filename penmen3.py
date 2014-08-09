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

# splits the image into 30 rows
# splits at row if <25 black px in row and >10 rows since last valid row
def splitws (img):
    ctr = 0
    rows = []
    for i in range(len(img)):
        if sum(img[i])/255. > 1335:
            if i - ctr > 10:
                rows.append(img[ctr:i])
                ctr = i
    return rows

# converts the array of float64 to a string of char 0 and 1s
def arr2str (arr):
    # add 2 to avoid cutting off starting 0s
    ans = 2
    # left, right, up, down
    for j in range(len(arr)):
        for i in range(len(arr[j])):
            if arr[j][i] == 255.:
                ans = ans * 10 + 1
            else:
                ans *= 10
    return str(ans)

# converts the string back to array
def str2arr (i, w, h):
    ans = str(i)
    # remove first "2" in str
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

# generates vertical and horizontal shifts of window of size h by w
# in row s, storing the # white px, what row it came from, and array
def stagger (s, h, w, rownum):
    height = len(s) + 1
    ans = []
    for i in range(len(s[0]) - w):
        for j in range(height - h):
            x = s[j:(h + j), i:(i+w)]
            if float(np.count_nonzero(x))/float(h*w) < 0.67:
                ans.append((np.count_nonzero(x), rownum, x))
                #ans.append((np.count_nonzero(x), rownum, arr2str(x)))
    return ans

# distance function for XOR-ing the string "bits"
def dist (v1, v2):
    tally = 0
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            tally += 1
    return tally

# distance function for XOR-ing the "bits" in the array
def dist2 (v1, v2):
    tally = 0
    v2f = np.ravel(v2)
    v1f = np.ravel(v1)
    for i in range(len(v1f)):
        if v1f[i] != v2f[i]:
            tally += 1
    return tally

# meat of the program. puts together above functions
def run (w, h):
    orig = Image.open("penmen2.png")
    orig = np.array(orig)

    ## for clean cutting
    if w == 20:
        orig = rem_borders(orig, 10, 12, 10, 20)
    else:
        orig = rem_borders(orig, 10, 12, 10, 25)

    ## sticks contains the 30 rows
    sticks = splitws(orig)

    ## NOTE: converting to type bool makes it run slower?
    for i in range(30):
        sticks[i] = sticks[i].astype(int)

    ## allsamples stores w by h samples
    extract = [0 for i in range(30)]
    allsamples = []
    for i in range(30):
        print "ROW", i
        allsamples += stagger(sticks[i], h, w, i)

    ## sort by % whitespace
    allsamples = sorted(allsamples, key = lambda x:x[0])

    ## shorter pairwise comparison through sorted allsamples
    ## accept samples that have <120 px diff and are >3 rows apart
    answers = []
    for (i, ai) in enumerate(allsamples):
        print i
        ai0, ai1, ai2 = ai
        for j in range(i, min(i + 1000, allsamples_len)):
            aj0, aj1, aj2 = aj = allsamples[j]
            if dist2(ai2, aj2) < 120 and abs(ai1 - aj1) > 3:
                print "ROW", ai1, aj1
                print "AT SORT", ai0, aj0
                answers.append(ai)
                answers.append(aj)
    return answers

# below is for displaying the results
def display (w, h):
    ## for timing purposes
    timer = time.asctime(time.localtime(time.time()))
    start = int(timer[11:13])*3600 + int(timer[14:16])*60 + int(timer[17:19])

    ## find all the pairs for consideration
    ans = run (w, h)
    print len(ans)

    ## only show all if fewer than 100 matches, prevents overflow
    if len(ans) <= 200:
        rows = []
        for i in range(len(ans)):
            ## does not show matches in same rows as previous matches
            if i % 2 == 0 and not((ans[i][1], ans[i+1][1]) in rows or (ans[i+1][1], ans[i][1]) in rows):
                #img1 = ans[i][2]
                img1 = str2arr(ans[i][2], h, w)

                ## add whitespace between the two matches
                ws = np.ones((h, 1))*255
                print "ROWS", ans[i][1], ans[i+1][1]
                #img2 = ans[i+1][2]
                img2 = str2arr(ans[i+1][2], h, w)
                rows.append((ans[i][1], ans[i+1][1]))

                ## combine the two matches separated by whitespace
                view = np.concatenate((img1, ws, ws, ws, img2), axis = 1)
                view = Image.fromarray(view)
                view.show()
    else:
        for i in range(200):
            if i%2 == 0:
                test = Image.fromarray(str2arr(ans[i][2], h, w))
                test.show()
    timer2 = time.asctime(time.localtime(time.time()))
    finish = int(timer[11:13])*3600 + int(timer2[14:16])*60 + int(timer[17:19])
    print "TIME TAKEN IN SEC:", finish - start

display (15, 52)
