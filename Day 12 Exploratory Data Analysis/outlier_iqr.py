import numpy as np
import matplotlib.pyplot as plt

data = [10, 12, 14, 15, 18, 19, 20, 22, 23, 24, 100]
sort1 = np.sort(data)
print("Sorted Data: ", sort1)

q2 = np.median(sort1)
q1 = np.percentile(sort1, 25, method='midpoint')
q3 = np.percentile(sort1, 75, method='midpoint')

print("Q1: ", q1)
print("Q2: ", q2)
print("Q3: ", q3)

iqr = q3 - q1
print("IQR: ", iqr)

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
print("Lower Bound: ", lower_bound)
print("Upper Bound: ", upper_bound)

outlier = []
for x in sort1:
    if x < lower_bound or x > upper_bound:
        outlier.append(x)
print("Outliers: ", x)

plt.figure(figsize=(10,6))
plt.boxplot(sort1, vert=False)
plt.title("Box Plot to Detect Outliers using IQR")
plt.xlabel("Values")
plt.show()
