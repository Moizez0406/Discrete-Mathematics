import random as rand

vertices = ['a1','a2','a3','a4','a8']
Edges = [(('a1','a4'),40), (('a4','a3'),30), (('a8','a3'),30)]

def random_iteration():
    rand.shuffle(vertices)
    S = []
    T = []
    # Split at the second place
    for i in range(5):
        if i < 3:
            S.append(vertices[i])
        else:
            T.append(vertices[i])
    # Check for Cuts on edges
    Sum = 0
    for (ai, aj), w in Edges:
        if (ai in S and aj in T) or (ai in T and aj in S):
            Sum  += w
    S.clear()
    T.clear()
    return Sum

highestSum = 0
for i in range(10):
    IterationSum = random_iteration()
    if highestSum < IterationSum:
        highestSum = IterationSum

print(f"{highestSum}")
