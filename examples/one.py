
def double(x):
	return x * 2

def apply(f, x):
	return f(x)

def double_add(a, b):
	print('in double_add', a)
	return double(a) + double(b)

double_add('h', 'e')
double_add(5, 10 + 2)
apply(double, 5)


