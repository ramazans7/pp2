import math
#1
d = float(input("Input degree: ")) 
r = math.radians(d)

print("Output radian:", r)  

#2
h = int(input("Height: "))
f = int(input("Base, first value: "))
s = int(input("Base, second value: "))

area = ((f+s)/2) *h
print("Expected Output: ", area)

#3
n = int(input("Input number of sides: "))
side = int(input("Input the length of a side: "))

area = (n * side**2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", area)

#4
length = int(input("Length of base: "))
height = int(input("Height of parallelogram: "))

area = length * height

print("Expected Output: ", area)