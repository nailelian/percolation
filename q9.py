#question 9
from percolation import *
from random import *

def rand_perc(n,p):
    P = Percolation(np.zeros((n,n)))
    for i in range(n):
        for j in range(n):
            P[i,j] = random()
            if P[i,j] < p:
