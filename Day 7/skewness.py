from scipy.stats import skew
import numpy as np

data = np.array([10, 25, 14, 26, 35, 45, 67, 90, 40, 50, 60, 10, 16, 18, 20])
skewness_value = skew(data)
print(skewness_value)
