#1
class myclass():
  def __len__(self):
    return 0

myobj = myclass()
print(bool(myobj))

#2
def myFunction() :
  return True

print(myFunction())

#3
def myFunction() :
  return True

if myFunction():
  print("YES!")
else:
  print("NO!")

#4
x = 200
print(isinstance(x, int))