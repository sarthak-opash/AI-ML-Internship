import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

speed = [20,56,89,98,78,45,65,85]

df = pd.DataFrame(speed)

x=np.mean(speed)
print(x)

sns.kdeplot(
    data=df
)
plt.show()