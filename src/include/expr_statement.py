from reducible import Reducible

class ExprStatement(Reducible):
	def __init__(self, program, expr):
		super().__init__(program, 1)
		self.expr = self.program.wrap(expr)
		self.state = 'initial'

	def do_reduce(self):
		self.report()
		result = self.expr.reduce()
		self.state = 'done'
		self.report()
		return result

	def do_show(self):
		if self.state == 'initial':
			return {
				"type": "statement",
				"value": self.expr.show()
			}
		elif self.state == 'done':
			return '<statement evaluated>'