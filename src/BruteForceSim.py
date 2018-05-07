import sys
from itertools import permutations

'''
The brute force's idea is
    for each permulation of all N elements
        update the total counter
'''

def isValid(seq, t):
    sum = 0
    for i in xrange(len(seq)):
        sum += (i+1) * seq[i]
    # print '------ Checking if current sequence is valid -----'
    # print 'The current sequence is as followed'
    # print (seq)
    print 'Index-weighted sum of current sequence is %d, target is %d' %(sum,t)
    return (sum > t)

'''
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
'''

def genPer(seq):
    if len(seq) <=1:
        yield seq
    else:
        for perm in genPer(seq[1:]):
            for i in range(len(perm)+1):
                # str[0:1] works in both string and list contexts
                yield perm[:i] + seq[0:1] + perm[i:]


def bruteforce(N, target):
    maxSeq = [0] * (N+1)
    i = 0

    for i in xrange(len(maxSeq)):
        maxSeq[i] = i
    maxSeq = list(maxSeq[1:])

    permList = []
    # permList = genPer(n=N, tempArr=maxSeq)
    # permList = genPer(A=maxSeq)
    print "The whole permulation list is as followed"

    '''
    print (permList)
    print genPer(A=maxSeq)

    # simple (import the permutation library) but insufficient perfomance permulation
    # print [list for list in permutations(maxSeq)]
    for list in permutations(maxSeq):
        # print list
        permList.append(list)
    '''

    for item in genPer(maxSeq):
    # for item in permutations(maxSeq):
        # print item
        permList.append(item)

    print "-------------- Brute-force simulation!!! --------------"
    cnt = 0 #total number of valid states
    for curSeq in permList:
        print curSeq
        if isValid(curSeq, t=target):
            cnt += 1
    print 'The number of states as computed brute-forcely is %d\n' %cnt
    # print 'The long-term prob is %f' %(cnt/ len(permList))


def calMaxSum(N):
    maxSeq = [0] * (N+1)

    for i in xrange(len(maxSeq)):
        maxSeq[i] = i
    maxSeq = list(maxSeq[1:])
    print maxSeq

    sum = 0
    # i = 0 #reset loop index i
    for i in maxSeq:
        print "i: %d, value: %d" %(i, maxSeq[i-1])
        sum += (i) * maxSeq[i-1]
    return sum

if __name__ == "__main__":
    args = sys.argv
    print args

    sum = calMaxSum(N=int(args[1]))
    print '---- The maximal sum- used to parameterize the target: %d ----' %sum

    # bruteforce(N=7,target=100)
    bruteforce(N=int(args[1]),target=int(args[2]))

    # bruteforce(N=15,target=1150)

    # bruteforce(N=30,target=9000)
