f = open("test.txt","r")
print(f.name)
print(f.mode)
print("Is Closed", f.closed)
f.close()
print("Is Closed", f.closed)


# By using with open we don't have to close filoe manually it will automatical close file after execution of the code
with open("test.txt", "w") as file:
    file.write("He is AiMl Intern \n")
print("Added")

with open("test.txt", "a") as file:
    file.write("He is 21 year old")

file = open("test.txt", "r")
content = file.read()
print(content)
file.close()

with open("3d_yellow_heart_shape_balloons.jpg","rb") as file:
    data = file.read()
    print(data)

