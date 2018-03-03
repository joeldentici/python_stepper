def add(x):
	def f(y):
		val = x + y
		x = 5
		return val + x
	return f

add(1)(2)
