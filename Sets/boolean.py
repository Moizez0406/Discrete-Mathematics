def my_and(p, q):
    result = [p[val]*q[val] for val in range(len(p))]
    return result

def my_or(p, q):
    result = [p[val]+q[val] for val in range(len(p))]
    for i in range(len(result)):
        if result[i] > 1:
            result[i] = 1
    return result

def my_not(p):
    result = [1-val for val in p]
    return result

def eval(expression, list_sets):
    i = 0
    result = ["r", []]
    list_sets.append(result)
    expression = expression + "E"

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

    def get(name):
        for this_set in list_sets:
            if this_set[0] == name:
                return this_set[1]
        return None

    while i < len(expression):
        if expression[i] == "(":
            depth = 1
            j = i + 1
            while j < len(expression) and depth > 0:
                if expression[j] == "(":
                    depth += 1
                elif expression[j] == ")":
                    depth -= 1
                j += 1
            inner_expr = expression[i+1:j-1]
            result[1] = eval(inner_expr, list_sets)
            expression = expression[:i] + result[0] + expression[j:]
            i = 0
            continue

        elif expression[i] == "^":
            if expression[i+1] == '(':
                depth = 1
                j = i + 2
                while j < len(expression) and depth > 0:
                    if expression[j] == '(':
                        depth += 1
                    elif expression[j] == ')':
                        depth -= 1
                    j += 1
                inner = expression[i+2:j-1]
                b = eval(inner, list_sets)
                if result[1]:
                    p = result[1]
                else:
                    p, _ = read(expression[i-1])
                result[1] = my_and(p, b)
                expression = result[0] + expression[j:]
                i = 0
                continue
            elif result[1]:
                if expression[i+1] == '~':
                    b = my_not(get(expression[i+2]))
                    skip = 3
                else:
                    b = get(expression[i+1])
                    skip = 2
            else:
                if expression[i+1] == '~':
                    result[1], _ = read(expression[i-1])
                    b = my_not(get(expression[i+2]))
                    skip = 3
                else:
                    result[1], b = read(expression[i-1], expression[i+1])
                    skip = 2
            result[1] = my_and(result[1], b)
            expression = result[0] + expression[i + skip:]
            i = 0
            continue

        elif expression[i] == "v":
            if expression[i+1] == '(':
                depth = 1
                j = i + 2
                while j < len(expression) and depth > 0:
                    if expression[j] == '(':
                        depth += 1
                    elif expression[j] == ')':
                        depth -= 1
                    j += 1
                inner = expression[i+2:j-1]
                b = eval(inner, list_sets)
                if result[1]:
                    p = result[1]
                else:
                    p, _ = read(expression[i-1])
                result[1] = my_or(p, b)
                expression = result[0] + expression[j:]
                i = 0
                continue
            elif result[1]:
                if expression[i+1] == '~':
                    b = my_not(get(expression[i+2]))
                    skip = 3
                else:
                    b = get(expression[i+1])
                    skip = 2
            else:
                if expression[i+1] == '~':
                    result[1], _ = read(expression[i-1])
                    b = my_not(get(expression[i+2]))
                    skip = 3
                else:
                    result[1], b = read(expression[i-1], expression[i+1])
                    skip = 2
            result[1] = my_or(result[1], b)
            expression = result[0] + expression[i + skip:]
            i = 0
            continue

        elif expression[i] == "~":
            val = get(expression[i+1])
            result[1] = my_not(val)
            expression = result[0] + expression[i+2:]
            i = 0
            continue

        i += 1

    if not result[1]:
        result[1] = read(expression[0])[0]

    return result[1]
