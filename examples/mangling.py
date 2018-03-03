def f(x):
	def g(x):
		return x + x
	return g
f(5)(5)
