import statistics as s
import numpy as np

data = [2,5,6,8,9,7,5,1,4,8,5,2,3,6,9]
data_variance = s.variance(data)
print(data_variance)
data_population_variance = s.pvariance(data)
print(data_population_variance)

num = np.array([1,2,3,4,5])
num_variance = np.var(num)
print(num_variance)
num_sample_variance = np.var(num, ddof=1)
print(num_sample_variance)

