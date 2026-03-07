import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = [10, 12, 14, 15, 18, 19, 20, 22, 23, 24, 100]

mean = np.mean(data)
print("Mean: ",mean)

std = np.std(data)
print("Standard Deviation: ",std)

lower_bound = mean - 2 * std
upper_bound = mean + 2 * std
print("Lower Bound: ", lower_bound)
print("Upper Bound: ", upper_bound)

outlier = []
for x in data:
    if x < lower_bound or x > upper_bound:
        outlier.append(x)   

print("Outliers: ", x)

sns.set_style("whitegrid")
plt.figure(figsize=(10,6))
sns.boxplot(x=data)
plt.title("Box Plot to Detect Outliers using Standard Deviation")
plt.xlabel("Values")
plt.show()