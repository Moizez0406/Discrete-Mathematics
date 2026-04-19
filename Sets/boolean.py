# assumes p in the form ['p',[values]]
def my_and(p, q):
    result = [p[1][val]*q[1][val] for val in range(len(p[1]))]
    named_result = ['r', result]
    return result

def my_or(p, q):
    result = [p[1][val]+q[1][val] for val in range(len(p[1]))]
    named_result = ['r', result]
    for i in range(len(result)):
        if result[i] > 1:
            result[i] = 1
    return result

def my_not(p):
    result = [1-val for val in p[1]]
    named_result = ['r', result]
    return result

def eval(expression, list_sets):
    i = 0
    a = None
    result = ["r", []]
    list_sets.append(result)
    universal = None
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

    while i < len(expression):
        if expression[i] == "(":
            inner_expr = expression[i + 1 :]
            result[1] = eval(inner_expr, list_sets)
            if expression[i + 4] == ")" and expression[i + 5] == "E":
                return result[1]

        elif expression[i] == "^":
            if result[1]:
                b, _ = read(expression[i + 1])
            else:
                result[1], b = read(expression[i - 1], expression[i + 1])
            result[1] = my_and(result[1], b)
            if expression[i + 2] != "E":
                expression = result[0] + expression[i + 2 :]
                i = 0

        elif expression[i] == "v":
            if result[1]:
                b, _ = read(expression[i + 1])
            else:
                result[1], b = read(expression[i - 1], expression[i + 1])
            result[1] = inter(result[1], b)
            if expression[i + 2] != 'E':
                expression = result[0] + expression[i+2:]
                i = 0

        elif expression[i] == "~":
            if result[1]:
                result[1] = complement(result[1], universal)
            else:
                result[1], _ = read(expression[i - 1])
            result[1] = complement(result[1], universal)
            if expression[i + 1] != 'E':
                expression = result[0] + expression[i+1:]
                i = 0

        i += 1

    return result[1]
