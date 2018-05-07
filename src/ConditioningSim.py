import sys
import random as ran
import math
import decimal as dec

ef isValid(seq, target):
    sum = 0
    for i in xrange(len(seq)):
        sum += (i+1) * seq[i]
    # print '------ Checking if current sequence is valid -----'
    print 'Index-weighted sum of current sequence is {0}, target is {1}'.format(sum, target)
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
        # print seq
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

def partition(N, T, k):
    parts = list()
    i = 0

    minTarget = 0
    for i in xrange(N):
        minTarget += i * (N - i)
    print "The min target: %d" %minTarget

    # Need improvement: partitioning supports float-sized (i.e. N % k != 0) chunks
    # if T % k == 0:
    for val in xrange(0, T, T/k):
        if val > minTarget:
            parts.append(val)
    parts.append(T)

    return parts

def initMaxSeq(N):
    maxSeq = [0] * N
    i = 0
    for i in xrange(N):
        maxSeq[i] = i+1
    return maxSeq


def conditioning_simulator(N, steps, target, nIter):
    print "The HM conditional simulation with the given paramaters"
    print "Size: %d. Each stepsize: %d. Target: %d. Number of runs: %d" %(N, steps, target, nIter)
    maxSeq = initMaxSeq(N)

    parts = partition(N, target, k=steps)
    print parts
    curSeq = list(maxSeq)

    # '''
    prodRes = float(1.0) # result of multiples of probablities
    prodList = list()

    for i in xrange(len(parts) - 1):
        # print "Current target is %d" %parts[i]
        prodRes = float(1.0)
        cnt1 = 0
        cnt2 = 0

        j = 0
        for j in xrange(nIter):
            #DEBUG: force to generate the valid curSeq
            while (not isValid(curSeq, parts[i])):
                curSeq = genState(curSeq, parts[i])
            # print "Current valid sequence is as below: "
            # print curSeq

            cnt1 += 1
            potSeq = genState(maxSeq, parts[i])
            alpha = computeAlpha(curSeq, maxSeq, parts[i])
            U = ran.random()

            if alpha < U:
                nextSeq = potSeq
            else:
                nextSeq = curSeq
            curSeq = nextSeq

            if isValid(curSeq, parts[i+1]):
                cnt2 += 1

            estimate = float(cnt2)/float(cnt1)
            # print 'For the step of %d At the iteration %d The cnt1: %d, and the cnt2: %d' %(parts[i], j, cnt1, cnt2)
            # print estimate
            # prodRes = dec.Decimal(prodRes) * dec.Decimal(estimate)
            # probList.append(estimate)

        # prodRes = float(prodRes) * float(estimate)
        prodList.append(estimate)
        # if j == nIter - 1:
        print "For the step of %d, the estimate at the final iteration %d is %f" %(parts[i], j, estimate)

    # print prodList
    print '------ The end result of conditioning Gibb''s sampling algorithm -----'
    for i in xrange(0, len(prodList)):
        prodRes *= prodList[i]

    print 'The product result: %f' %prodRes
    print 'The long-term number of states is %d\n' %(1/prodRes)

if __name__ == "__main__":
    args = sys.argv
    print args
    dec.getcontext().prec = 2

    # conditioning_simulator()
    # First initial test: N = 7, steps = 10, target = 100, nIter = 1000
    conditioning_simulator(N=int(args[1]), steps=int(args[2]), target=int(args[3]), nIter=int(args[4]))
    # conditioning_simulator(N=10, steps=5, target=300, nIter=1000)
    # conditioning_simulator(N=10, steps=5, target=300, nIter=100000)
    # conditioning_simulator(N=10, steps=5, target=300, nIter=1000000)
    # conditioning_simulator(N=15, steps=5, target=300, nIter=100000)
