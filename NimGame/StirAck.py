import numpy as np
import math
import matplotlib.pyplot as plt

def Stirling(n, Gosper=False, log=False):
    if Gosper:
        if log:
            value = 0.5 * np.log((2*n + 1/3) * np.pi) + n * np.log(n) - n
            return value
        value = np.sqrt((2*n+(1/3))*np.pi)*(n**n)*(np.e**(-n))
        return value
    if log:
        value = 0.5 * np.log(2 * np.pi * n) + n * np.log(n) - n
        return value

    log_value = n*np.log(n)-n+np.log(2*np.pi*n)
    value = np.sqrt(2*n*np.pi)*((n/np.e)**n)
    return value

def Ackerman(x,y):
    if x == 0:
        return y + 1
    elif y == 0:
        return Ackerman(x-1,1)
    else:
        return Ackerman(x-1,Ackerman(x,y-1))

n = 10
x,y = 3,5
base_value = math.factorial(n)
print(f"Exact value n!: {base_value}")
print(f"Stirling n! =~ {Stirling(n)}")
print(f"Gosper n! =~ {Stirling(n,True)}")


n_vals = np.linspace(0.1, 4.0, 100)
base = [math.gamma(n + 1) for n in n_vals]
stirlings = [Stirling(n, Gosper=False, log=False) for n in n_vals]
gospers = [Stirling(n, Gosper=True, log=False) for n in n_vals]

n_dots = np.arange(0.5, 4.0, 1.0) 
base_dots = [math.gamma(n + 1) for n in n_dots]

plt.figure(figsize=(10, 6))
plt.scatter(n_dots, base_dots, color='black', label='Exact (Gamma Function)', s=30, zorder=5)
plt.plot(n_vals, stirlings, color='red', label='Stirling', alpha=0.7)
plt.plot(n_vals, gospers, color='blue', label='Gosper version', alpha=0.9)

plt.xticks(np.arange(0,4.5,0.5))
plt.title('Comparison of Accuracy')
plt.xlabel('n')
plt.ylabel('n!')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

plt.show()

print("Accuracy Comparison:")
error_stirling = [abs(s_vals - b) / b for s_vals, b in zip(stirlings, base)]
error_gosper = [abs(g_vals - b) / b for g_vals, b in zip(gospers, base)]
print(f"Stirling Relative Error: {np.mean(error_stirling):.5%}")
print(f"Gosper Relative Error:   {np.mean(error_gosper):.5%}")


n_vals = np.arange(1,50)
base = [math.log(math.factorial(int(n))) for n in n_vals]
stirlings = [Stirling(n,False,True) for n in n_vals]
gospers = [Stirling(n,True,True) for n in n_vals]

plt.figure(figsize=(10,6))
plt.scatter(n_vals, base, color='black',label='Exact',s=10,zorder=5)
plt.plot(n_vals, stirlings, 'r--',label='Stirling',alpha=0.8)
plt.plot(n_vals, gospers, 'b:',label='Gosper version',linewidth=2)

steps = [1] + list(range(5,50,5))
plt.xticks(steps)
plt.title("Comparison")
plt.xlabel("n")
plt.ylabel("log(n!)")
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)

plt.show()

print(f"Ackerman({x},{y}) = {Ackerman(x,y)}")

for m in range(4):
    values = [Ackerman(m, n) for n in range(7)]
    plt.plot(range(7), values, marker='o', label=f"m={m}")

plt.yscale("log")
plt.xlabel("n")
plt.ylabel("Ackermann(m, n)")
plt.title("Ackermann Function Growth")
plt.legend()
plt.grid()
plt.show()

