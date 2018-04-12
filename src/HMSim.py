import random as ran
import numpy as np
import math
# from CombCounter import CombCounterObj

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

    i = 0
    testSeq = [0] * n
    for i in xrange(1, n-1):
      for j in xrange(i+1, n):
        testSeq = seq
        testSeq[i], testSeq[j] = testSeq[j], testSeq[i]
        # testSeq = list(swap(i, j, testSeq))

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

        seq[i], seq[j] = seq[j], seq[i]
        # result = list(swap(i, j, seq))
        if isValid(seq, target):
            break
    return seq
    # return res

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

def initSeq(N):
    maxSeq = [0] * N

    i = 0
    for i in xrange(N):
        maxSeq[i] = i+1
    return maxSeq

def HMSimulator(N, target, nIter):
    maxSeq = initSeq(N)

    watchSeq = genState(maxSeq, target)
    print 'The watch sequence is {0}'.format(watchSeq)

    watchTrans = 0
    totalTrans = 0
    curSeq = list(maxSeq)

    #--- simulation starts ---
    for i in xrange(nIter):
        # print '----------- Inside the simulation -------------'
        potSeq = genState(curSeq, target)

        # if (potSeq == watchSeq).all():
        if np.array_equal(potSeq, watchSeq):
          print '----------- Hit!!! -------------'
          watchTrans += 1

        alpha = computeAlpha(curSeq, potSeq, target)
        U = ran.random()

        if U < alpha:
          nextSeq = list(potSeq)
        else:
          nextSeq = list(curSeq)
        curSeq = list(nextSeq)
        totalTrans += 1

    #--- end of the main loop ---
    print '------ The end result of Hasting-Metropolis algorithm -----'
    lrProb = float(watchTrans) / float(totalTrans)
    print 'The number of times it hits on watch state is {0} over total of {1}'.format(watchTrans, totalTrans)
    if lrProb != 0:
        print 'The number of states in the long run is {0}'.format(1/lrProb)
    else:
        print 'ERROR: Something wrong in the long run probablity'

#Quick reminder of Python's 'docstring' syntax - https://www.python.org/dev/peps/pep-0257/
#------ Tests for running the HM algorithm for the permulation selection ---------
if __name__ == '__main__':
    #small test: size = 10 with small iterations
    # HMSimulator(N=10, target=300, nIter=10000)

    #small test: size = 10 with small iterations
    HMSimulator(N=10, target=300, nIter=10000000)

    #testing 2
    # HMSimulator(N=30, target=30000, nIter=10000)
