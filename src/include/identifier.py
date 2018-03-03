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

	def do_reduce(self):
		self.report()
		self.state = 'reduced'
		self.report()
		return self.value

	def do_show(self):
		ident = self.program.name_model.resolve_name(self.id)
		if self.state == 'initial':
			return ident
		elif self.state == 'reduced':
			return self.program.show_value(self.value, ident)



'''
	def __getattribute__(self, name):
		return super().__getattribute__(name)

	def __setitem__(self, key, value):
		self.value[key] = value



	def __setattr__(self, key, value):
		setattr(self.value, key, value)
'''