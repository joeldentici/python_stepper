from reducible import Reducible
from statement_group import StatementGroup

def block(what):
	return {
		"type": "block",
		"value": what
	}

class WhileLoop(Reducible):
	def __init__(self, program, t, f):
		super().__init__(program, 1)
		self.true = WhileBlock(program, t, self)
		self.false = WhileBlock(program, f, self)
		self.t = WhileBlock(program, t, self)
		self.f = WhileBlock(program, f, self)
		self.state = 'initial'

	def do_reduce(self):
		self.true.enter()

	def do_show(self):
		if self.state == 'initial':
			return self.show_loop(self.test.show())
		elif self.state == 'taken':
			return self.show_block(self.taken, '\n') + self.show_loop(self.test_start)
		elif self.state == 'done':
			return self.show_block(self.taken)

	def show_loop(self, test):
		return ['while ', test, ':\n',\
		block(self.t.show())] + self.else_block()

	def show_block(self, block, after = ''):
		if block.has_statements():
			return [block.show(), after]
		else:
			return []

	def else_block(self):
		if self.f.has_statements():
			return ['\nelse:\n', block(self.f.show())]
		else:
			return []

	def while_test(self, test):
		self.true.reset()
		self.false.reset()
		self.t.reset()
		self.f.reset()
		self.state = 'initial'
		self.test = self.program.wrap(test)
		self.test_start = self.test.show()
		self.program.report_clear(1)
		value = self.test.reduce()
		taken = self.true if value else self.false
		self.state = 'taken' if value else 'done'
		self.taken = taken
		taken.enter()
		return value

class WhileBlock(StatementGroup):
	def __init__(self, program, stmts, loop):
		super().__init__(program, stmts)
		self.loop = loop

	def while_test(self, test):
		self.exit()
		return self.loop.while_test(test)

	def show(self):
		return self.base_show()

	def cleanup(self):
		if self.has_statements():
			self.program.report(1)
		self.exit()



'''
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

'''