import numpy as np
import matplotlib.pyplot as plt

mean = 100
std = 15
size = 100000

data = np.random.normal(mean, std, size)
plt.hist(data, bins=50, density=True, alpha=0.6, color='skyblue') 
plt.title('Histogram of Normally Distributed Data')
plt.xlabel('Value')
plt.ylabel('Density')
plt.axvline(mean, color='k', linestyle='dashed', linewidth=2, label='Mean')
plt.legend()
plt.show()