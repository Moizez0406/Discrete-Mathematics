
def union(a, b):
    new_set = a.copy()
    for element in b:
        if element not in new_set:
            new_set.append(element)
    return new_set

def inter(a, b):
    new_set = []
    for element in a:
        if element in b:
                new_set.append(element)
    return new_set

def complement(set, universal):
    new_set = []
    for u in universal:
        if u not in set:
            new_set.append(u)
    return new_set 

def relative_cmplt(a, b, universal):
    # We assume a, b E U set
    new_set = complement(a, universal)
    return inter(new_set, b)

def cartesian_product(a, b, flattern = False):
    size = len(a) * len(b)
    groups = 2
    base = [[] for _ in range(size)]
    i = 0
    if flattern:
        i = 0
        base = [[] for _ in range(len(a)*len(b))]
        for element in a:
            for pair in b:
                base[i] = element + [pair]
                i+=1
    else:
        for element in a:
            for pair in b:
                base[i].append(element)
                base[i].append(pair)
                i+=1


    return base

def power(a):
    bin_set = [0,1]
    new_sets = []
    first = cartesian_product(bin_set, bin_set)

    if len(a) > 2:
        for _ in range(len(a)-1):
            new_sets = cartesian_product(first, bin_set, True)

        final_set = [[] for _ in range(len(new_sets))]
        index = 0
        for element in new_sets:
            for i in range(len(element)):
                if element[i]:
                    final_set[index].append(a[i])
            index += 1

        return final_set
    return new_sets

