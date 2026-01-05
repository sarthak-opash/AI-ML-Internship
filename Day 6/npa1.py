import numpy as np

a = np.array(((1,2),(5,8)))
b = np.array(((2,4),(9,7)))


result = a @ b
res1 = a * b
res = np.dot(a,b)

print(result)
print(res1)
print(res)

print(np.ndim(a))
print(np.linspace(1,20,5))
print(np.logspace(a+b,a+b,2))