from reducible import Reducible

class FunctionDef(Reducible):
	def __init__(self, program, name, stmts, params, fn):
		super().__init__(program, 1)
		self.program.store_function(fn, self)
		self.name = name
		self.stmts = stmts
		self.params = params
		self.fn = fn

	def do_reduce(self):
		return self.fn

	def do_show(self):
		return ['def ', self.name, '(', self.show_params(), '):\n', self.show_body()]

	def show_params(self):
		return ", ".join(self.params)

	def show_body(self):
		return {
			"type": "block",
			"value": {
				"type": "statement_group",
				"statements": self.stmts
			}
		}

	def display(self):
		return self.name