from reducible import Reducible
from statement_group import StatementGroup
from function_def import FunctionDef


class FunctionCall(Reducible):
	def __init__(self, program, fn, args):
		super().__init__(program, 1)
		self.fn = fn
		self.args = [self.program.wrap(x) for x in args]
		self.state = 'initial'

	def reduce(self):
		self.report()
		fn = self.fn.reduce()
		args = [a.reduce() for a in self.args]

		self.create_reducer(fn, args)

		self.state = 'reducing'

		return self.reducer.reduce()

	def create_reducer(self, fn, args):
		if fn in self.program.functions:
			info = self.program.functions[fn]
			if isinstance(info, FunctionDef):
				self.reducer = FunctionAppGroup(self.program, fn, args, info)
			else:
				self.reducer = LambdaApp(self.program, fn, args, info)
		else:
			self.reducer = UnknownApp(self.program, fn, args)

	def show(self):
		if self.state == 'initial':
			return self.show_call()
		if self.state == 'reducing':
			return self.reducer.show()

	def show_call(self):
		return [self.fn.show(), '('] + self.show_args() + [')']

	def show_args(self):
		vals = []
		if len(self.args):
			vals.append(self.args[0].show())

		for arg in self.args[1:]:
			vals.append(', ')
			vals.append(arg.show())

		return vals

class FunctionAppGroup(StatementGroup):
	def __init__(self, program, fn, args, info):
		super().__init__(program, info.stmts)
		self.fn = fn
		self.args = args
		self.info = info
		self.state = 'initial'
		self.granularity = 1

	def reduce(self):
		self.program.report(1)

		self.enter()

		fn = self.fn
		args = self.args

		self.result = fn(*args)
		self.state = 'reduced'

		self.exit()

		self.program.report(self.granularity)

		return self.result

	def show(self):
		if self.state == 'initial':
			return {
				"type": "function_activation",
				"value": self.base_show()
			}
		elif self.state == 'reduced':
			return self.program.show_value(self.result, '<unknown>')

class LambdaApp(Reducible):
	def __init__(self, program, fn, args, info):
		super().__init__(program, 1)
		self.fn = fn
		self.args = args
		self.info = info
		self.state = 'initial'

	def reduce(self):
		fn = self.fn
		args = self.args

		self.expr = fn(*args)
		self.result = self.expr.reduce()
		self.state = 'reduced'

		self.report()

		return self.result

	def show(self):
		if self.state == 'initial':
			return self.expr.show()
		elif self.state == 'reduced':
			return self.program.show_value(self.result, '<unknown>')

class UnknownApp(Reducible):
	def __init__(self, program, fn, args):
		super().__init__(program, 1)
		self.fn = fn
		self.args = args
		self.state = 'initial'

	def reduce(self):
		fn = self.fn
		args = self.args

		self.result = fn(*args)
		self.state = 'reduced'

		self.report()

		return self.result

	def show(self):
		assert self.state != 'initial'
		if self.state == 'reduced':
			return self.program.show_value(self.result, '<unknown>')