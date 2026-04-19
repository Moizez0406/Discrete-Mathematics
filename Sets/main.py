import sets
import boolean

p = [1, 0, 1, 0]
q = [1, 1, 0, 0]
a = [0,1,2,3,8]
b = [2,3,4,5,9]
c = [4,5,6,7,8]
x = ['a','b','c']
y = ['e','f','g']
universal = [0,1,2,3,4,5,6,7,8,9]
union = sets.union(a,b)
intersection = sets.inter(a,b)
complement_a = sets.complement(a, universal)
cmp_b_respect_a = sets.relative_cmplt(b, a)
cartesian_product = sets.cartesian_product(x, y)
power_p = sets.power(x)
print("------"*7)
print(f"| sets: "+" "*33+"|")
print("|"+"-----"*8+"|")
print(f"| p: {p}"+" "*24+"|")
print(f"| q: {q}"+" "*24+"|")
print(f"| x: {x}"+" "*21+"|")
print(f"| y: {y}"+" "*21+"|")
print(f"| a: {a}"+" "*21+"|")
print(f"| b: {b}"+" "*21+"|")
print(f"| c: {c}"+" "*21+"|")
print(f"| u: {universal}"+" "*6+"|")
print("------"*7)
print("------"*7)
print("| Operators syntax:"+" "*22+"|")
print("|"+"-----"*8+"|")
print("| Union                = u (lowercase U) |\n"+
    "| Intersection         = n (lowercase N) |"+
    "\n| Complement of x      = x'              |\n"+
    "| x' with respect of y = x_y             |"+
    "\n| Power of x           = Px              |"+
    "\n| And, Or, Not         = v,^,~           |")
print("------"*7)
print("------"*7)
print("Syntax examples:\n")
print(f"a u b: {union}")
print(f"a n b: {intersection}")
print(f"a': {complement_a}")
print(f"b' respect to a: {cmp_b_respect_a}")
print(f"X x Y: {cartesian_product}")
print(f"P(x): {power_p}")
print(f"Inclusion for |aubuc| {sets.in_ex([a, b, c])}")
print("------"*7)
print("------"*7)

a = sets.build_set('a', [0,1,2,3,8])
b = sets.build_set('b', [2,3,4,5,9])
c = sets.build_set('c', [4,5,6,7,8])
universal = sets.build_set('universal', [0,1,2,3,4,5,6,7,8,9])
list_sets = [a,b,c,universal]
list_bool = [['p',p],['q',q]]

print(f"characteristic function for a from u {sets.characteristic(a[1], universal[1])}")
print("Enter 'q' to exit")
print("Enter add to add a new set (NOT IMPLEMENTED)")
print("Enter 'bool' to enter boolean mode and write like: ~pv(p^q)")
print("Enter 'exit' to quite bool mode")
mode = 'normal'
while True:
    expression = input(f"\nEnter expression ({mode} mode): ")
    if expression == 'bool':
        mode = 'bool'
    elif expression == 'exit':
        mode = 'normal'

    if mode == 'bool' and expression != 'bool':
        if expression == 'exit':
            mode = 'normal'
        else:
            result = boolean.eval(expression.replace(" ", ""), list_bool)
            print(f"result: {result}\n")
    elif mode == 'normal' and expression != 'exit':
        result = sets.eval(expression.replace(" ", ""), list_sets)
        print(f"result: {result}\n")

    if expression == 'q':
        break

