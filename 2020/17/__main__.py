from ..utils import *

from itertools import product

rng = lambda X,b: range(b*(min(X)-1), max(X)+2)

Δ = [-1,0,1]

def neigh(i,P,d):
    Δs = Δ if max(i[2:]) != 0 else [1,0,1]
    moves = product(Δ, Δ, * [Δs]*(d-2) )
    return sum(tuple(a+b for a,b in zip(i,δ)) in P for δ in moves)

def GoL(dim, cycles = 6):
    P = {(x,y,*[0]*(dim-2))
              for y,X in enumerate(open(input_file()).read().split('\n'))
              for x,c in enumerate(X) if c == '#'}

    for _ in range(6):
        bounds = (rng([x[n] for x in P], n < 2) for n in range(dim))
        P = { i for i in product(*bounds)
                if ((i in P), neigh(i, P, dim)) in [(1,3), (1,4), (0,3)] }

    l = sum(max(i[2:]) == 0 for i in P)

    return (l + (len(P)-l)* 2**(dim-2))

print(GoL(3))
print(GoL(4))
# print(GoL(5))
