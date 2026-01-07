import pandas as pd

data = {
    'Study_Hours': [1,2,3,4,5,6],
    'Exam_Score': [45,50,55,65,75,85]
}

df = pd.DataFrame(data)
res = df.corr()
print(res)
