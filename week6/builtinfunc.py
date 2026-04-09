#1
nums = [1, 2, 3, 4]

squares = list(map(lambda x: x**2, nums))
print(squares)

#2
nums = [1, 2, 3, 4, 5, 6]

even = list(filter(lambda x: x % 2 == 0, nums))
print(even)

#3
from functools import reduce

nums = [1, 2, 3, 4]

total = reduce(lambda x, y: x + y, nums)
print(total)

#4
names = ["Ali", "John", "Sara"]

for i, name in enumerate(names):
    print(i, name)

#5
names = ["Ali", "John"]
scores = [90, 85]

for name, score in zip(names, scores):
    print(name, score)