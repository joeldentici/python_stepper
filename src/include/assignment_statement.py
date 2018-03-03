from reducible import Reducible

class AssignmentStatement(Reducible):
	def __init__(self, program, lval, expr):
		super().__init__(program, 1)
		self.lval = lval
		self.expr = self.program.wrap(expr)

	def do_reduce(self):
		self.report()
		result = self.expr.reduce()
		self.program.report_clear(1)
		self.program.name_model.bind(self.lval, result)
		self.report()
		return result

	def do_show(self):
		lval = self.program.name_model.resolve_name(self.lval)
		return {
			"type": "statement",
			"value": [lval, ' = ', self.expr.show()]
		}
