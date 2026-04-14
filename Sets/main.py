import sets

a = [0,1,2,3]
b = [2,3,4,5]
c = [2,3,6,7]
union = sets.union([a,b,c])
intersection = sets.inter([a,b,c])
universal = union.copy()
complement_a = sets.complement(a, universal)

print(f"sets: ")
print(f"a: {a}")
print(f"b: {b}")
print(f"c: {c}")
print(f"Union? {union}")
print(f"Intersection? {intersection}")
print(f"Complement_a? {complement_a}")
