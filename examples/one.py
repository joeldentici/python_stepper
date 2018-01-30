
def double(x):
	return x * 2

def double_add(a, b):
	print('in double_add', a)
	return double(a) + double(b)

double_add('h', 'e')
double_add(5, 10 + 2)