sample_set = [1,1,2,2,3,5]
sample_set1 = set(sample_set)
print(sample_set1)

a = {1,2,3,4,5,6}
b = {2,3,5,6,7} 
print("Union", a|b)
print("Intersect",a&b)
print("Difference",a-b)

banned_set = {"Pistol", "Knife", "Sword"}
i = "Pistol"
if i in banned_set:
    print(f"{i} is Prohibited")

set1 = {"Sarthak","Nimbark"}
set2 = {"Sarthak","BLah"}
comma = set1 & set2
print(comma)