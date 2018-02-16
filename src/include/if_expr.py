from reducible import Reducible

class IfExpression(Reducible):
	def __init__(self, program, test, t, f):
		super().__init__(program, 1)
		self.test = self.program.wrap(test)
		self.true = self.program.wrap(t)
		self.false = self.program.wrap(f)
		self.state = 'initial'

	def reduce(self):
		self.report()
		truth = self.test.reduce()
		self.taken = self.true if truth else self.false # lol!
		self.state = 'taken'
		self.report()

		self.value = self.taken.reduce()
		self.state = 'reduced'
		self.report()

		return self.value

	def show(self):
		if self.state == 'initial':
			return [self.true.show(), ' if ', self.test.show(), ' else ', self.false.show()]
		elif self.state == 'taken':
			return self.taken.show()
		elif self.state == 'reduced':
			return self.program.show_value(self.value, '<unknown>')