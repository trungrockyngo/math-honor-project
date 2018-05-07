import sys
import random as ran
import math
# import numpy as np

def compare(A, B):
    if len(A) == 0 or len(B) == 0:
        return False
    if len(A) != len(B):
        return False
    else:
        for i in xrange(len(A)):
            if A[i] != B[i]:
                return False
    return True

def isValid(seq, target):
    sum = 0
    for i in xrange(len(seq)):
        sum += (i+1) * seq[i]
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
    N = len(seq)

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
    maxSeq = [0] * (N+1)
    for i in xrange(len(maxSeq)):
        maxSeq[i] = i
    maxSeq = list(maxSeq[1:])

    minTarget = 0
    for i in xrange(N):
        minTarget += i * (N - i)
    print "The min target: %d" %minTarget

    '''
    # Unnecessary to generate minSeq!!!
    minSeq = [0] * N
    for val in reversed(maxSeq):
        minSeq.append(val)
    print "The minimum sequence is: "
    print minSeq

    minValidSeq = genState(maxSeq, minTarget)
    '''
    # return maxSeq, minTarget, minValidSeq
    return maxSeq, minTarget

# def genWatchSeqList(maxSeq, minTarget, W, T): #NOTE: no longer need watch size or target
def genWatchSeqList(maxSeq, minTarget):
    print '--------- Generating the list of watch sequences ---------'
    watchList = []
    # watchList.append(minValidSeq)
    # print 'Initially, the min valid sequence is {0}'.format(minValidSeq)

    '''
    j = len(minValidSeq) - 1 #initially the last index
    pivotIndex = j - W - 1 #the pivot index to be swapped with

    # generate other W-1 sequences in the watch list. Need to also check against the target???
    for i in (0, W):
        print '--- Generating the element %d-th' %(i+1)
        tempSeq = minValidSeq
        # x = tempSeq[pivotIndex]
        # y = tempSeq[j]
        print 'Two elements to be swapped are %d, %d' %(tempSeq[pivotIndex], tempSeq[j])
        tempSeq[pivotIndex], tempSeq[j] = tempSeq[j], tempSeq[pivotIndex]
        watchList.append(tempSeq)
        print '--- Current distinct sequences in the watchState''s list'
        print tempSeq
        j = j - 1
    #end-for
    # assert len(watchList) == W
    '''

    # Optimization #3:
    currID = len(maxSeq) - 1
    prevID = currID - 1
    curSeq = maxSeq
    while (prevID < currID and prevID >= 0):
        tempSeq = curSeq
        tempSeq[prevID], tempSeq[currID] = tempSeq[currID], tempSeq[prevID]

        if isValid(tempSeq, minTarget) is False:
            break
        curSeq = list(tempSeq)
        # print 'Valid sequence for the watch list is {0}'.format(curSeq)
        watchList.append(curSeq)

        currID = prevID
        prevID = prevID - 1
    #end-while
    print '--------- The watch list of size {0} contains -------- \n{1}'.format(len(watchList), watchList)

    return watchList

def HMSimulator(N, target, nIter):
    maxSeq, minTarget = initSeq(N)

    # watchSeq = genState(maxSeq, target)
    # print 'The watch sequence is {0}'.format(watchSeq)
    watchList = genWatchSeqList(maxSeq, minTarget)

    watchTotalTrans = 0
    totalTrans = 0
    curSeq = list(maxSeq)

    for i in xrange(nIter):

        # print '----------- Inside the simulation -------------'
        #prune all values doesn't pass the minimum for this and other methods -> already passed by the check inside here
        potSeq = genState(curSeq, target)

        for wSeq in watchList:
            if compare(potSeq, wSeq):
              print '----------- Hit!!! -------------'
              watchTotalTrans += 1
        #end-for loop

        alpha = computeAlpha(curSeq, potSeq, target)
        U = ran.random()

        if U < alpha:
          nextSeq = list(potSeq)
        else:
          nextSeq = list(curSeq)
        curSeq = list(nextSeq)
        totalTrans += 1

    watchSize = len(watchList)
    #--- end of the main loop ---
    print '------ The end result of Hasting-Metropolis algorithm -----'
    lrProb = float(watchTotalTrans)/ (watchSize * float(totalTrans))
    print 'The number of times it hits on watch state is {0} over total of {1}'.format(watchTotalTrans, totalTrans)
    if lrProb != 0:
        print 'The number of states in the long run is {0}'.format(int(1/lrProb))
    else:
        print 'MISS: No hit for the watch list. The long-run probablity is 0!!!'

#Quick reminder of Python's 'docstring' syntax - https://www.python.org/dev/peps/pep-0257/
#------ Tests for running the HM algorithm for the permulation selection ---------
if __name__ == '__main__':
    args = sys.argv
    print args
    # First initial test: N = 7, target = 100, watchSize = 7 (usually parameterize it to the same as watchSize), nIter = 10000
    # HMSimulator(N=int(args[1]), target=int(args[2]), watchSize=int(args[3]), nIter=int(args[4]))
    HMSimulator(N=int(args[1]), target=int(args[2]), nIter=int(args[3]))

    #small test: size = 10 with small iterations
    # HMSimulator(N=10, target=300, nIter=10000)

    #small test: size = 10 with small iterations
    # HMSimulator(N=10, target=300, nIter=10000000)

    #testing 2
    # HMSimulator(N=30, target=30000, nIter=10000)
