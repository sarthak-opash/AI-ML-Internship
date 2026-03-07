import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import zscore


data = [5, 2, 4.5, 4, 3, 2, 6, 20, 9, 2.5, 3.5, 4.75, 6.5, 2.5, 8, 1]
df = pd.DataFrame(data, columns=['Value'])
df['Z-score'] = zscore(df['Value'])
print(df)

outliers = df[df['Z-score'].abs() > 3]
print(outliers)

plt.figure(figsize=(10, 6))

plt.scatter(df['Value'].index, df['Z-score'], label='Data Points')
plt.scatter(outliers['Value'].index, outliers['Z-score'], color='red', label='Outlier')

plt.xlabel('Index Value')
plt.ylabel('Z-score')
plt.title('Scatter Plot of Value vs. Z-score')
plt.legend()
plt.grid(True)
plt.show()
