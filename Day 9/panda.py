import pandas as pd
import numpy as np

data = np.array(['s','a','r','t','h','a','k'])

s = pd.Series()
#print("Panda Series :", s)

s = pd.Series(data)
#print(s)

s1 = pd.DataFrame()
#print("Panda Data Frame:",s1)

s1 = pd.DataFrame(data)
#print(s1)

s2 = pd.read_csv('sample.csv')
print(s2.head())

ages = s2[s2['Age'] >= 21]
print(ages)

total = s2['Age'] + s2['CGPA']
print(total)

second_row = s2.iloc[1]
print(second_row)

group = s2.groupby('Age')['CGPA'].sum()
print(group)