def f(y):
	def g(x):
		def h(y):
			return x + y
		return h
	return g
f(5)(6)(7)
