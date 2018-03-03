x = [4]
x[0] = 5

def change(y):
	y[0] = 7
	return 0

def add(x,y,z):
	return x + y + z

print(add(1, change(x), x[0]))