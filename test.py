import sys

def add(a,b):
	return a + b

def fact(n):
	return n * fact(n - 1) if n > 1 else n

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
print add(a, b)
print fact(c)