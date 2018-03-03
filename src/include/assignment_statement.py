from reducible import Reducible
from report_state import rename_statement

class AssignmentStatement(Reducible):
	def __init__(self, program, lval, expr):
		super().__init__(program, 1)
		self.lval = lval
		self.expr = self.program.wrap(expr)

	def reduce(self):
		self.program.start_reducing(self)
		self.report()
		result = self.expr.reduce()
		self.program.report_clear(1)
		if "." not in self.lval and "[" not in self.lval:
			self.program.name_model.bind(self.clean_lval(), result)
		return result

	def do_show(self):
		return {
			"type": "statement",
			"value": [self.get_lval(), ' = ', self.expr.show()]
		}

	def get_lval(self):
		return rename_statement(self.program.name_model.current_scope, self.lval)

	def clean_lval(self):
		return self.lval.replace('<@ ', '').replace(' @>', '')