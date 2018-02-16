from reducible import Reducible
from statement_group import StatementGroup

def block(what):
	return {
		"type": "block",
		"value": {
			"type": "statement_group",
			"statements": what
		}
	}

class IfStatement(Reducible):
	def __init__(self, program, test, t, f):
		super().__init__(program, 1)
		self.test = self.program.wrap(test)
		self.true = t
		self.false = f
		self.state = 'initial'

	def reduce(self):
		self.report()

		value = self.test.reduce() 

		self.taken = IfBlock(self.program, self.true) \
		  if value else IfBlock(self.program, self.false)
		self.state = "taken"

		self.taken.reduce()

		return value

	def show(self):
		if self.state == 'initial':
			return ['if ', self.test.show(), ':\n', \
			  block(self.true)] + self.else_block()
		elif self.state == "taken":
			return self.taken.show()

	def else_block(self):
		if len(self.false):
			return ['\nelse:\n', block(self.false)]
		else:
			return []

class IfBlock(StatementGroup):
	def __init__(self, program, stmts):
		super().__init__(program, stmts)
		self.state = 'initial' if len(stmts) else 'done'
		self.granularity = 1

	def reduce(self):
		self.program.report(1)

		self.enter()

	def show(self):
		if self.state == 'initial':
			return {
				"type": "function_activation",
				"value": self.base_show()
			}
		elif self.state == 'done':
			return 'None'

	def cleanup(self):
		self.state = 'done'
		self.program.report(1)
		self.exit()