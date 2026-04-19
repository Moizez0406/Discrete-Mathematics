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


def cartesian_product(a, b, flattern=False):
    size = len(a) * len(b)
    groups = 2
    base = [[] for _ in range(size)]
    i = 0
    if flattern:
        i = 0
        base = [[] for _ in range(len(a) * len(b))]
        for element in a:
            for pair in b:
                base[i] = element + [pair]
                i += 1
    else:
        for element in a:
            for pair in b:
                base[i].append(element)
                base[i].append(pair)
                i += 1

    return base


def power(a):
    bin_set = [0, 1]
    new_sets = []
    first = cartesian_product(bin_set, bin_set)

    if len(a) > 2:
        for _ in range(len(a) - 1):
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


def build_set(name, values):
    return [name, values]


def eval(expression, list_sets):
    i = 0
    a = None
    result = ["r", []]
    list_sets.append(result)
    universal = None
    expression = expression + "E"
    for this_set in list_sets:
        if this_set[0] == "universal":
            universal = this_set[1]

    def read(left, rigth=True):
        a = None
        b = None
        for this_set in list_sets:
            if this_set[0] == left:
                a = this_set[1]
            if this_set[0] == rigth:
                b = this_set[1]
            if a and b and rigth:
                return a, b
        return a, b

    while i < len(expression):
        if expression[i] == "(":
            inner_expr = expression[i + 1 :]
            result[1] = eval(inner_expr, list_sets)
            if expression[i + 4] == ")" and expression[i + 5] == "E":
                return result[1]

        elif expression[i] == "u":
            if result[1]:
                b, _ = read(expression[i + 1])
            else:
                result[1], b = read(expression[i - 1], expression[i + 1])
            result[1] = union(result[1], b)
            if expression[i + 2] != "E":
                expression = result[0] + expression[i + 2 :]
                i = 0

        elif expression[i] == "n":
            if a:
                b = read(expression[i + 1])
            else:
                a, b = read(expression[i - 1], expression[i + 1])
            return inter(a, b)

        elif expression[i] == "'":
            if a:
                return complement(a, universal)
            else:
                a = read(expression[i - 1])
                return complement(a, universal)

        elif expression[i] == "_":
            if a:
                b = read(expression[i + 1])
            else:
                a, b = read(expression[i - 1], expression[i + 1])
            return relative_cmplt(a, b, universal)

        elif expression[i] == "x":
            if a:
                b = read(expression[i + 1])
            else:
                a, b = read(expression[i - 1], expression[i + 1])
            return cartesian_product(a, b)

        elif expression[i] == "P":
            if a:
                return power(a)
            else:
                a = read(expression[i + 1])
            return power(a)
        i += 1

    return result[1]
