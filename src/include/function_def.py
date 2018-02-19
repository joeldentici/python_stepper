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
		return '<TODO: Show FunctionDef>'

	def display(self):
		return self.name