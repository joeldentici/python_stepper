from reducible import Reducible

class Value(Reducible):
	def __init__(self, program, value, added = False):
		super().__init__(program, 1)
		self.value = value
		self.added = added

	def do_reduce(self):
		return self.value

	def do_show(self):
		return self.program.show_value(self.value, '<unknown>', self.added)