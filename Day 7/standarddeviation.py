import statistics as s
import numpy as np

num = np.array([1,2,3,4,5])
num_standard_deviation = np.std(num)
print(num_standard_deviation)
num_standard_deviation_standard = np.std(num,ddof=1)
print(num_standard_deviation)