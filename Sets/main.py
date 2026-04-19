import sets

x = ['a', 'b', 'c']
y = [2, 3]
a = [0,1,2,3,8]
b = [2,3,4,5,9]
c = [4,5,6,7,8]
universal = [0,1,2,3,4,5,6,7,8,9]
union = sets.union(a,b)
intersection = sets.inter(a,b)
complement_a = sets.complement(a, universal)
cmp_b_respect_a = sets.relative_cmplt(b, a)
cartesian_product = sets.cartesian_product(x, y)
cartesian2 = sets.cartesian_product(cartesian_product, x, True)
#power_a = sets.power(a)
power_x = sets.power(x)
print(f"sets: ")
print(f"x: {x}")
print(f"y: {y}")
print(f"a: {a}")
print(f"b: {b}")
print(f"c: {c}")
print(f"u: {universal}\n")
print("------"*7)
print("Operators syntax:\n")
print("| Union                = u (lowercase U) |\n"+
    "| Intersection         = n (lowercase N) |"+
    "\n| Complement of x      = x'              |\n"+
    "| x' with respect of y = x_y             |"+
    "\n| Power of x           = Px              |\n")
print("Syntax examples:\n")
print(f"a u b: {union}")
print(f"a n b: {intersection}")
print(f"a': {complement_a}")
print(f"b' respect to a: {cmp_b_respect_a}")
print(f"x x y: {cartesian_product}")
print(f"P(x): {power_x}\n")
print("------"*7)

a = sets.build_set('a', [0,1,2,3,8])
b = sets.build_set('b', [2,3,4,5,9])
c = sets.build_set('c', [4,5,6,7,8])
universal = sets.build_set('universal', [0,1,2,3,4,5,6,7,8,9])
list_sets = [a,b,c,universal]

print("Enter q to exit")
print("Enter add to add a new set (NOT IMPLEMENTED)")
while True:
    expression = input("\nEnter expression: ")
    result = sets.eval(expression.replace(" ", ""), list_sets)
    print(f"result: {result}\n")
    if expression == 'q':
        break

