from reducible import Reducible

'''
Identifier
written by Joel Dentici
on 02/15/2018

Represents an identifier (name) in a program.
'''

class Identifier(Reducible):
	def __init__(self, program, ident, value):
		super().__init__(program, 1)
		self.id = ident
		self.value = value
		self.state = 'initial'

	def reduce(self):
		self.state = 'reduced'
		self.report()
		return self.value

	def show(self):
		if self.state == 'initial':
			return self.id
		elif self.state == 'reduced':
			return self.program.show_value(self.value, self.id)