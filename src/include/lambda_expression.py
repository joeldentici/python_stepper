from reducible import Reducible

class LambdaExpression(Reducible):
	def __init__(self, program, src, params, fn):
		super().__init__(program, 1)
		self.program.store_function(fn, self)
		self.src = src
		self.fn = fn

	def reduce(self):
		return self.fn

	def show(self):
		return self.src

	def display(self):
		return self.show()