import numpy as np
# import matplotlib.pyplot as plt #later-
# import matplotlib.mlab as mlab
import math

class CombCounterObj():

    # def __init__(self):

    # # compute the degree of the given state X
    def nCr(n,r):
        f = math.factorial
        # NOTE: in python 3.x use '//' to avoid overflown
        nCr_result = f(n)// (f(r) * f(n-r))
        # print 'The combination of {0} over {1} is {2}'.format(n,r, nCr_result)
        return nCr_result

    def isValid(seq, target):
        sum = 0
        for i in xrange(len(seq)):
            sum += i*seq[i]
        # print '------ Checking if current sequence is valid -----'
        # print 'Index-weighted sum of current sequence is {0}, target is {1}'.format(sum, target)
        return (sum > target)

    def degree(seq, target):
        # print '------ Inside degree(seq) -----'
        cnt = 0
        n = len(seq)
        combNum = nCr(n, 2)

        i = 0
        # while i < combNum:
        #   potSeq = genState(seq)
        #   # print '------ Inside the combinatorics loop -----'
        #   print 'Current step is {0}'.format(i)
        #   if isValid(potSeq, target):
        #     cnt += 1
        #   i += 1
        #   continue

        testSeq = [0] * n
        for i in xrange(1, n-1):
          for j in xrange(i+1, n):
            testSeq = seq
            testSeq = list(swap(i, j, testSeq))

            if isValid(testSeq, target):
               cnt += 1

        return cnt

    def genState(seq, target):
        N = len(seq);

        while True:
            i = ran.randint(0, N-1)
            j = ran.randint(0, N-1)

            while (i == j):
                j = ran.randint(0, N-1)

            result = list(swap(i, j, seq))
            if isValid(result, target):
                break
        return result

    def computeAlpha(curSeq, potSeq, target):
        # print '------ Inside computeAlpha(curSeq, potSeq)  -----'
        deno = degree(curSeq, target)
        nume = degree(potSeq, target)
        ratio = 0.0
        if nume != 0:
            ratio = float(deno) / float(nume)
        else:
            print "ERROR: Something wrong with the potential sequence"
        # print 'Ratio is {0}'.format(ratio)
        return min(ratio, 1.0)

    def swap(i, j, seq):
        # temp = seq[i]
        # seq[i] = seq[j]
        # seq[j] = temp
        #print 'After the swap: seq[i] = {0}, seq[j] = {1}'.format(seq[i], seq[j])
        seq[i], seq[j] = seq[j], seq[i]
        return seq
