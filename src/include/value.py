from reducible import Reducible

class Value(Reducible):
	def __init__(self, program, value):
		super().__init__(program, 1)
		self.value = value

	def reduce(self):
		return self.value

	def show(self):
		return self.program.show_value(self.value, '<unknown>')