def add(x):
	def f(y):
		nonlocal x
		val = x + y
		x = 5
		return val + x
	return f

result = add(1)(2)
