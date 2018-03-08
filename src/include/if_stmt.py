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
		self.state = 'taken'

		self.taken.reduce()

		return value

	def do_show(self):
		if self.state == 'initial':
			return ['if ', self.test.show(), ':\n', \
			  block(self.true.show())] + self.else_block()
		elif self.state == 'taken':
			return self.show_block(self.taken)

	def show_block(self, block):
		if block.has_statements():
			return block.show()
		else:
			return []

	def else_block(self):
		if self.false.has_statements():
			return ['\nelse:\n', block(self.false.show())]
		else:
			return []

class IfBlock(StatementGroup):
	def __init__(self, program, stmts):
		super().__init__(program, stmts)
		self.state = 'initial'
		self.granularity = 1
		self.reset()

	def reduce(self):
		if self.has_statements():
			self.program.report(1)

		self.enter()

	def show(self):
		if self.state == 'initial':
			return self.base_show()

	def cleanup(self):
		if self.has_statements():
			self.program.report(1)
		self.exit()
