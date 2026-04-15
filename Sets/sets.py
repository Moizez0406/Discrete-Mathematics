
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

def cartesian_product(a, b):
    new_sets = []
    for element in a:
        new_sets.append([element, x] for x in b])
    return new_sets

def power(a):
    bin_set = [0,1]
    new_sets = []
    temp_sets = bin_set.copy()
    for _ in range(len(a)):
        new_sets = cartesian_product(temp_sets, bin_set)
        temp_sets = new_sets.copy()

    for value in temp_sets:
        if value:
           pass 

    return new_sets

