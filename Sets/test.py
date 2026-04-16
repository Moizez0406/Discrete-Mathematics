import random
a = [0, 1, 2]
b = [3, 4, 5]
c = [6, 7, 8] 

# Calculate the size
size = len(a) * len(b)
groups = 2
base = [[] for _ in range(size)]
# multiplicant
i = 0
for element in a:
    for pair in b:
        base[i].append(element)
        base[i].append(pair)
        i+=1


i = 0
new_base = [[] for _ in range(len(base)*len(c))]
for element in base:
    for pair in c:
        new_base[i] = element + [pair]
        i+=1



print(base)
print("---"*10)
print(new_base)
