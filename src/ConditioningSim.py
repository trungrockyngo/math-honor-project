import random as ran
import numpy as np
import math
'''
ideas:
    Partion orginal seq into k (simulator's paramater) equally divided chunks

    For each conditional prob at chunk a_i
        compute estimate[i] = P( s(x) > a_i | s(x) > a_(i - 1)) is done by calling

        if i == 0: a bit different yet simpler to calculate estimate[0]
        the HM-counting (OOP refactoring!!!) except
            - no watch state
            - a_i-1 becomes new target and just count cnt1 when s(x) > a_i-1
                if s(x) > a_i update cnt2
        -> estimate[i] = cnt2/ cnt1
    chunk = 1000

    for i = 1 -> nITer:
        for j = 0 -> N:
            if i mod chunk == 0:
                if S(X) > a[i-1]:
                    cnt2 ++
                    potSeq = genState(curSeq)

                    alpha = computeAlpha(degree(curSeq), degree(potSeq))
                    U = rand(0,1)

                    if alpha < U:
                        curSeq = potSeq
                    if alpha > U:
                        nextSeq = curSeq
                if S(X) > a[i]:
                    cnt1 ++
                estimate = cnt1/ cn2

    multiple all estimates


'''

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

    # minSeq = [0] * N
    minTarget = 0
    for i in xrange(N):
        minTarget += i * (N - i)
    # print "The min target: %d" %minTarget

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


def conditioning_simulator(N, k, target, nIter):
    maxSeq = initMaxSeq(N)

    parts = partition(N, target, k)
    print parts
    curSeq = list(maxSeq)

    # '''
    prodRes = 1.0 # result of multiples of probablities
    for i in xrange(len(parts) - 1):
        # print "Current target is %d" %parts[i]
        cnt1 = 0
        cnt2 = 0
        for j in xrange(nIter):
            if isValid(curSeq, parts[i]):
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
                # print 'Conditional counting is %f. Total counting is %f ' %(cnt2, cnt1)
                print 'The probablity between of consecutive conditioning is currently %f' %estimate
                prodRes = float(prodRes) * float(estimate)
                print 'The probablity is currently %f' %prodRes

    print '------ The end result of conditioning Gibb''s sampling algorithm -----'
    print 'The product result: %f' %prodRes
    print 'The long-term number of states is %d' %(1/prodRes)
    # '''
if __name__ == "__main__":
    # conditioning_simulator()
    conditioning_simulator(N=10, k=5, target=300, nIter=1000)
    # conditioning_simulator(N=10, k=30, target=300, nIter=100000)
