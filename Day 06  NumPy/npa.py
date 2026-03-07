import numpy as np

a = ([1,2,3],[4,5,6],[7,8,9])
a1 = np.array(a)
print(a1)

a0 = np.zeros((3,3))
print(a0)
a2 = np.ones((2,2))
print(a2)
a3 = np.arange(0,21,5)
print(a3)

a4 = np.array([10,20,30,40,50,60,70,80])
print(a4)
print(a4[-1])
print(a4[3])

a5 = np.array(
  [  [1,2,3],
    [4,5,6],
    [7,8,9]]
)
print(a5)
print(a5[2,2])

print(a5[1:2])
print(a5[:,1])

idx = ([1,3,5])
print(a4[idx])

a6 = np.array([1,2,3,4,5,6,7,8])
print(a4+a6)
print(a4-a6)
print(a4*a6)
print(a4/a6)

dtype = [("Name", "S10"),("Year", int), ("CGPA", float)]
data = [('Sarthak' , 2005, 7.9),
        ("Jolly", 2008,5.9),
        ("Josh",2002,8.9)]

x = np.array(data, dtype=dtype)
print(x)
print(np.sort(x,order='Name'))
print(np.sort(x,order='Year'))
print(np.sort(x,order=['Year','CGPA']))

unicode = [21,56,89,77]
array = np.fromiter(unicode, dtype='U1')
print(array)


mat1 = ('1,2;3,2')
matrix1 = np.matrix(mat1)
print(matrix1)

mat2 = ([1,2],[5,6])
matrix2 = np.matrix(mat2)
print(matrix2)