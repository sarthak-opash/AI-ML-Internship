import numpy as np
from scipy import stats

speed = [20,56,89,98,78,45,65,85,85,20,65,20]

x=stats.mode(speed)
print(x)

