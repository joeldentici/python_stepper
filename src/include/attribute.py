from reducible import Reducible

class Attribute(Reducible):
	def __init__(self, program, left, ident):
		super().__init__(program, 1)
		self.left = self.program.wrap(left)
		self.ident = ident
		self.state = 'initial'

	def do_reduce(self):
		self.report()
		left = self.left.reduce()
		self.report()
		self.value = getattr(left, self.ident)
		self.state = 'reduced'
		self.report()
		return self.value

	def do_show(self):
		value = [self.left.show(), '.', self.ident]
		if self.state == 'initial':
			return value
		elif self.state == 'reduced':
			return self.program.show_value(self.value, value)