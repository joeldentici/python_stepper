from reducible import Reducible
from statement_group import StatementGroup

def block(what):
	return {
		"type": "block",
		"value": what
	}

class IfStatement(Reducible):
	def __init__(self, program, test, t, f):
		super().__init__(program, 1)
		self.test = self.program.wrap(test)
		self.true = IfBlock(self.program, t)
		self.false = IfBlock(self.program, f)
		self.state = 'initial'

	def do_reduce(self):
		self.report()

		value = self.test.reduce() 

		self.taken = self.true if value else self.false

		self.taken.reduce()

		return value

	def do_show(self):
		if self.state == 'initial':
			return ['if ', self.test.show(), ':\n', \
			  self.true.show()] + self.else_block()

	def else_block(self):
		if self.false.has_statements():
			return ['\nelse:\n', self.false.show()]
		else:
			return []

class IfBlock(StatementGroup):
	def __init__(self, program, stmts):
		super().__init__(program, stmts)
		self.state = 'initial'
		self.granularity = 1

	def reduce(self):
		self.program.report(1)

		self.enter()

	def show(self):
		if self.state == 'initial':
			return block(self.base_show())

	def cleanup(self):
		self.program.report(1)
		self.exit()
