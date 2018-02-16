from reducible import Reducible

class AssignmentStatement(Reducible):
	def __init__(self, program, lval, expr):
		super().__init__(program, 1)
		self.lval = lval
		self.expr = self.program.wrap(expr)

	def reduce(self):
		self.report()
		return self.expr.reduce()

	def show(self):
		return {
			"type": "statement",
			"value": [self.lval, ' = ', self.expr.show()]
		}
