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

class WhileLoop(Reducible):
	def __init__(self, program, t, f):
		super().__init__(program, 1)
		self.true = t
		self.false = f

	def reduce(self):
		self.loop = WhileLoopGroup(self.program, self.true, self.false)
		self.loop.enter()

	def show(self):
		return self.loop.show()

class WhileLoopGroup(StatementGroup):
	def __init__(self, program, t, f):
		super().__init__(program, [])
		self.state = 'initial'
		self.true = t
		self.false = f

	def while_test(self, test):
		self.reset()
		self.state = 'initial'
		self.test = self.program.wrap(test)
		self.program.report(1)
		value = self.test.reduce()
		self.set_statements(self.true if value else self.false)
		self.state = 'taken'

		return value

	def loop_break(self):
		pass

	def loop_continue(self, explicit):
		# Todo: add handling of an explicit continue statement
		if explicit:
			pass
		self.finish_iteration()

	def finish_iteration(self):
		# Todo: determine whether we need to display anything at end of iteration
		pass


	def cleanup(self):
		self.state = 'done'
		self.program.report(1)
		self.exit()

	def show(self):
		if self.state == 'initial':
			return self.show_initial()
		elif self.state == "taken":
			return self.show_taken()
		elif self.state == "done":
			return '<while loop exited>'

	def show_initial(self):
		return ['while ', self.test.show(), ':\n', \
		  block(self.true)] + self.else_block()

	def show_taken(self):
		return {
			"type": "function_activation",
			"value": self.base_show()
		}

	def else_block(self):
		if len(self.false):
			return ['\nelse:\n', block(self.false)]
		else:
			return []