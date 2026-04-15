import sets

x = ['a','b','c']
a = [0,1,2,3,8]
b = [2,3,4,5,9]
c = [2,3,6,7, 8, 9]
universal = [0,1,2,3,4,5,6,7,8,9]
union = sets.union(a,b)
intersection = sets.inter(a,b)
complement_a = sets.complement(a, universal)
cmp_b_respect_a = sets.relative_cmplt(a, b, universal)
cartesian_product = sets.cartesian_product(a, b)
#power_a = sets.power(a)
power_x = sets.power(x)
print(f"sets: ")
print(f"x: {x}")
print(f"a: {a}")
print(f"b: {b}")
print(f"c: {c}")
print(f"u: {universal}")
print("------"*7)
print("Syntax example")
print(f"a u b: {union} (Lower U)")
print(f"a n b: {intersection} (Lower N)")
print(f"a': {complement_a}")
print(f"b' respect to a (b-a): {cmp_b_respect_a}")
print(f"a x b: ")
print("P(x):")
for element in power_x:
    print("*********************")
    for component in element:
        for value in component:
            print(value)
print("------"*7)

#while True:
#    print("Enter q to exit")
#    print("Enter add to add a new set")
#    i = input("Enter expression: ")
#    if i == 'q':
#        break
