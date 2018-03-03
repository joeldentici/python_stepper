
'''
NameModel
written by Joel Dentici
on 02/22/2018

Represents the name resolution model of Python. This is used
by various components of the stepper to track name bindings
the same way Python does.
'''

class NameModel:
	def __init__(self, program):
		self.program = program
		self.scopes = []
		self.current_scope = self.add_scope(GlobalNameScope(program))

	def add_scope(self, scope):
		scope.set_number(len(self.scopes))
		self.scopes.append(scope)
		return scope

	def set_current_scope(self, scope):
		self.current_scope = scope

	def show(self):
		mem = []
		for x in self.scopes:
			mem += x.show()
		return mem

	def resolve_scope(self, name):
		return self.current_scope.resolve_scope(name)

	def resolve_name(self, name):
		return self.current_scope.resolve_name(name)

	def bind(self, name, val):
		self.current_scope.resolve_scope(name).bind(name, val)


class NameScope:
	def __init__(self, program):
		self.names = {}
		self.scope_number = 0
		self.program = program

	def create_binding(self, name):
		self.names[name] = None

	def bind(self, name, val):
		self.names[name] = val

	def set_number(self, num):
		self.scope_number = num

	def show_name(self, name):
		if self.scope_number:
			return name + '_' + str(self.scope_number)
		else:
			return name

	def show_val(self, name):
		value = self.names[name]
		return self.program.show_value(value, '<function>')

	def show(self):
		names = sorted(self.names)
		bindings = [self.show_name(n) + ' = ' + self.show_val(n) for n in names]
		return bindings

	def resolve_scope(self, name):
		return self

	def resolve_name(self, name):
		return self.resolve_scope(name).show_name(name)

class GlobalNameScope(NameScope):
	pass
