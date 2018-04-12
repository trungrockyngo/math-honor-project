import numpy as np
from itertools import permutations

'''
The brute force's idea is
    for each permulation of all N elements
        update the total counter
'''

def isValid(seq, t):
    sum = 0
    for i in xrange(len(seq)):
        sum += i*seq[i]
    print '------ Checking if current sequence is valid -----'
    print 'The current sequence is as followed'
    print (seq)
    print 'Index-weighted sum of current sequence is %d, target is %d' %(sum,t)
    return (sum > t)

# def genPer(n, tempArr):
#     if n == 1:
#         # result.append(tempArr)
#         yield tempArr
#     else:
#         i = 0
#         for i in xrange(0, n-1):
#             genPer(n-1, tempArr, result=result)
#
#             if n % 2 == 1:
#                 j = 1
#             else:
#                 j = i
#             # print '------- tempArr[%d] is %d, tempArr[%d] is %d -------' %(j, tempArr[j], n-1, tempArr[n-1])
#             tempArr[j], tempArr[n-1] = tempArr[n-1], tempArr[j]

def heap_perm(n, tempArr):
    if n == 1:
        yield tempArr
    else:
        for i in xrange(0, n-1):
            for hp in genPer(n-1, tempArr):
                yield hp
            j = 0 if n % 2 == 1 else i
            tempArr[j], tempArr[n-1] = tempArr[n-1], tempArr[j]
        for hp in genPer(n-1, tempArr):
            yield hp

def genPer(A):
    n = len(A)
    Alist = [el for el in A]
    for hp in _heap_perm_(n, Alist):
        yield hp

def bruteforce(N, target):
    maxSeq = [0] * (N+1)
    i = 0
    for i in xrange(len(maxSeq)):
        maxSeq[i] = i

    permList = []
    # permList = genPer(n=N, tempArr=maxSeq)
    # permList = genPer(A=maxSeq)
    print "The whole permulation list is as followed"
    # print (permList)
    # print genPer(A=maxSeq)


    # simple (import the permutation library) but insufficient perfomance permulation
    # print [list for list in permutations(maxSeq)]
    for list in permutations(maxSeq):
        # print list
        permList.append(list)


    cnt = 0 #total number of valid states
    for curSeq in permList:
        if isValid(curSeq, t=target):
            cnt += 1
    print 'The number of states as computed brute-forcely is %d' %cnt
    print 'The long-term prob is %f' %(cnt/ perm)


def calMaxSum(N):
    maxSeq = [0] * (N+1)
    i = 0
    for i in xrange(len(maxSeq)):
        maxSeq[i] = i
    sum = 0
    for i in maxSeq:
        # print "i: %d, value: %d" %(i, maxSeq[i])
        sum += (i) * maxSeq[i]
    return sum

if __name__ == "__main__":
    # bruteforce(N=10,target=300)
    sum = calMaxSum(N=10)
    print sum

    # bruteforce(N=15,target=1150)

    # bruteforce(N=30,target=9000)
