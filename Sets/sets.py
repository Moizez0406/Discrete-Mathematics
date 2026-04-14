
def union(sets):
    # assume we have more than 2 groups
    new_set = sets[0].copy()
    for i in range(1, len(sets)):
        for element in sets[i]:
            if element not in new_set:
                new_set.append(element)
    #new_set = sets[0]+sets[1]
    return new_set

def inter(sets):
    # assume we have more than 2 groups
    new_set = []
    for i in range(len(sets)-1):
        for element in sets[i]:
            if element in sets[i+1] and element not in new_set:
                new_set.append(element)
    return new_set

def complement(set, universal):
    new_set = []
    for u in universal:
        if u not in set:
            new_set.append(u)
    return new_set 

