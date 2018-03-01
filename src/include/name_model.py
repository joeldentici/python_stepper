
'''
NameModel
written by Joel Dentici
on 02/22/2018

Represents the name resolution model of Python. This is used
by various components of the stepper to track name bindings
the same way Python does.
'''

class NameModel:
	def __init__(self):
		self.scopes = []
		self.current_scope = self.add_scope(NameScope())

	def add_scope(self, scope):
		self.scopes.append(scope)
		scope.set_number(len(self.scopes))
		return scope

	def set_current_scope(self, scope):
		self.current_scope = scope

	def show(self):
		pass


class NameScope:
	def __init__(self):
		self.names = {}

	def create_binding(self, name):
		self.names[name] = unbound

	def bind(self, name, val):
		self.names[name] = val

	def set_number(self, num):
		self.scope_number = num


class Unbound:
	pass

unbound = Unbound()