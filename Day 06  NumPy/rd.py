from numpy import random
import numpy as np

a = np.array([1,2,3,4])
x = random.randint(10,size=4)
print(x)
random.shuffle(a)
print(a)

