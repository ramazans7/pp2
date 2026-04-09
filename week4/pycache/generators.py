#1
def square(N):
    for i in range(1,N + 1):
        yield i * i

N = int(input())
for i in square(N):
    print(i)

#2
def even(w):
    for i in range(w+1):
        if i % 2 == 0:
            yield i

w = int(input())
print(*even(w), sep=",")

#3
def div(n):
    for i in range(1, n + 1):
        x = i
        while x % 3 == 0:
            x //= 3
        while x % 4 == 0:
            x //= 4
        if x == 1:
            yield i
s = int(input())

for i in div(s):
    print(i)

#4
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i


a = int(input())
b = int(input())

for x in squares(a, b):
    print(x)

#5
def num(z):
    for i in range(z, -1,-1):
        yield i
z = int(input())
for i in num(z):
    print(i)