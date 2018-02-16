from reducible import Reducible

class ReturnStatement(Reducible):
	def __init__(self, program, expr):
		super().__init__(program, 1)
		self.expr = self.program.wrap(expr)

	def reduce(self):
		return self.expr.reduce()

	def show(self):
		return {
			"type": "statement",
			"value": ['return ', self.expr.show()]
		}
