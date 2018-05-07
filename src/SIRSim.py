import random as ran
import numpy as np
import math as ma
import sys

def isValid(seq, target):
    sum = 0
    for i in xrange(len(seq)):
        sum += i*seq[i]
    # print '------ Checking if current sequence is valid -----'
    # print 'Index-weighted sum of current sequence is {0}, target is {1}'.format(sum, target)
    return (sum > target)

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

def initSeq(N):
    maxSeq = [0] * N

    i = 0
    for i in xrange(N):
        maxSeq[i] = i+1
    return maxSeq

def SIRSimulator(N, target, nIter, m):
    curSeq = initSeq(N)

    watchSeq = genState(curSeq, target)
    watchCnt = 0

    for j in xrange(nIter):
        curSeq = list(genState(curSeq, target))

        # potSeqList = dict()
        potSeqList = {}
        idCnt = 0
        for i in xrange(m):
            nextSeq = genState(curSeq, target)
            if isValid(curSeq, target):
                idCnt += 1
                potSeqList.update({idCnt: nextSeq})
                # print "--- New sequence id %d is added---" %idCnt

        nextSeqId = ma.ceil(idCnt * ran.random())
        nextSeq = potSeqList.get(nextSeqId)

        curSeq = nextSeq #update the next state
        if np.array_equal(curSeq, watchSeq):
            watchCnt += 1

    print '------ The end result of SIR algorithm -----'
    print 'watchCnt is %d over nIter %d' %(watchCnt, nIter)
    lrProb = float(watchCnt) / float(nIter)
    print 'In the long run probablity, which is %f, the number of states is %d' %(lrProb, 1/lrProb)

if __name__ == '__main__':
    #small test: size = 10 with small iterations
    args = sys.argv
    print args
    # N = 7, target = 100, .. m = 50
    SIRSimulator(N=int(args[1]), target=int(args[2]), nIter=int(args[3]), m=int(args[4]))

    # SIRSimulator(N=10, target=300, nIter=1000, m= 100)
