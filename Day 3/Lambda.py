x = lambda a: a + 10
print(x(5))

x1 = lambda a,b: a + b
print(x1(1,5))

#map
number = [1,2,3,4,5]
num = map(lambda x2: x2*3,number)
print(list(num))

#filter
number1 = [2,4,5,6,8,9]
num1 = filter(lambda x3: x3%2==0,number1)
print(list(num1))

#sorted
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_list = sorted(students, key=lambda x:x[1])
print(list(sorted_list))

words = ["Apple", "Kiwi", "Mango", "Strawberry"]
sorted_words = sorted(words, key=lambda x:len(x))
print(list(sorted_words))


