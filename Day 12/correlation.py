import pandas as pd
from sklearn.datasets import load_diabetes
import seaborn as sns
import matplotlib.pyplot as plt

df = load_diabetes(as_frame=True).frame

print(df.head())

corr = df.corr(method = 'pearson')
print(corr)

plt.figure(figsize=(10,6), dpi=100)
sns.heatmap(corr,annot=True,fmt=".2f", linewidth=.5)
plt.show()
