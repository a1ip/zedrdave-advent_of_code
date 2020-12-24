from ..utils import *

D = {'w':(-1,0), 'nw':(0,-1), 'ne':(1,-1), 'e':(1,0), 'se': (0,1), 'sw': (-1,1)}
𝓜 = lambda x,y,dx,dy: (x+dx,y+dy)

𝐓 = set()
for l in open(input_file()):
    P = (0,0)
    while len(l.strip()):
        n = 2 if l[:2] in D else 1
        P = 𝓜(*P, *D[l[:n]])
        l = l[n:]
    𝐓 ^= {P}

print(f"Part 1: {len(𝐓)}")

𝓝 = lambda *p: sum(𝓜(*p, *D[k]) in 𝐓 for k in D)
# 𝓑 = lambda n: range(min(X := [x[n] for x in 𝐓])-1, max(X)+2)
𝓑 = lambda n: range(min(x[n] for x in 𝐓)-1, max(x[n] for x in 𝐓)+2)

for d in range(100):
    𝐓 = {(x,y) for x in 𝓑(0) for y in 𝓑(1) if ((x,y) in 𝐓 and 𝓝(x,y) == 1) or 𝓝(x,y) == 2}
    ### Bonus Viz:
    import time
    w = 38
    print(f"\033\143Day {d+1}: {len(𝐓)}\n" + '\n'.join((' '* (y % 2) + ''.join('⬛️' if (x-w,y-w) in 𝐓 else '⬜️' for x in range(2*w))) for y in range(2*w)))
    time.sleep(.1)

print(f"Part 2: {len(𝐓)}")
