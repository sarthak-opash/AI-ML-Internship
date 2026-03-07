list = [1,2,5,33]
list.append(222)
list.remove(2)
print(list)

list1 = []
list1.append(2)
list1.append(3)
list1.remove(2)
print(list1)

dynamic_list = []
for i in range(11):
    dynamic_list.append(i*i)
print(dynamic_list)

string_slicing = "Here it begins now"
slice=string_slicing.split()
for i in slice:
    print(i.upper(), end = " ") 