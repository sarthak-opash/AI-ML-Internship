try:
    n = 10
    res = 100/n

except ZeroDivisionError:
    print("Can not be divided by zero")

else:
    print(res)

finally:
    print("Your code executed successfully")

class ageerror(Exception):
    pass

def set(age):
    if age < 0:
        raise ageerror("Age can't Negative")
    print("Age set to f`{age}`",age)

try:
    set(10)
except ageerror as e:
     print(e)

try:
    with open("text.txt","w+") as file:
        try:
            file.write("Sarthak Is Amazing")
            print(file)
            file.seek(0)
            res = file.read()
            print(res)
        except:
            print("Something went Wrong")
        finally:
            print("Code Execution Done")
except:
    print("sOME THING GONE WRONG")

