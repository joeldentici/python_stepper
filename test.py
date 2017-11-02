import sys

def add(a,b):
	return a + b

def fact(n):
	return n * fact(n - 1) if n > 1 else n

def add2(a):
	def finish_add(b):
		return a + b

	return finish_add

def mymax(a, b):
	if (a > b):
		return a
	else:
		return b

a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
print add(a, b)
print fact(c)
print add2(a)(b)
print mymax(a, b)