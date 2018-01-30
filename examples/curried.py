def add(x):
	def f(y):
		return x + y
	return f

add(1)(2)