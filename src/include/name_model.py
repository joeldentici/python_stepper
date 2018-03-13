import re
from reducible import Reducible
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
		self.memory_lookup = {}
		self.memory = []

	def add_scope(self, scope):
		scope.set_number(len(self.scopes))
		self.scopes.append(scope)
		return scope

	def set_current_scope(self, scope):
		self.current_scope = scope

	def show(self):
		mem = []

		for i,x in enumerate(self.memory):
			mem.append(show_mem_name(str(i)) + ' = ' + self.program.show_value(self.mem_show(x), '<function>'))

		for x in self.scopes:
			mem += x.show()
		return mem

	def resolve_scope(self, name):
		return self.current_scope.resolve_scope(name)

	def resolve_name(self, name):
		return self.current_scope.resolve_name(name)

	def bind(self, name, val):
		self.current_scope.resolve_scope(name).bind(name, val)

	def is_class(self, value):
		return hasattr(value, '__dict__') and \
		not isinstance(value, Reducible) and \
		not callable(value)

	def maybe_add_to_memory(self, value):
		if isinstance(value, dict):
			for k in value:
				self.maybe_add_to_memory(value[k])
			res = self.store_value(value)
			return res
		if isinstance(value, list):
			for x in value:
				self.maybe_add_to_memory(x)
			res = self.store_value(value)
			return res
		if self.is_class(value):
			for k,v in vars(value).items():
				self.maybe_add_to_memory(v)
			res = self.store_value(value)
		return False

	def lookup_value(self, value):
		if id(value) in self.memory_lookup:
			return self.memory_lookup[id(value)]

	def store_value(self, value):
		if self.lookup_value(value) == None:
			self.memory_lookup[id(value)] = len(self.memory)
			self.memory.append(value)
			return True

	def resolve_memory(self, value):
		loc = self.lookup_value(value)
		if loc != None:
			return MemoryLocation(loc)
		else:
			return value

	def mem_show(self, value):
		if isinstance(value, dict):
			return {k:self.resolve_memory(v) for k,v in value.items()}
		if isinstance(value, list):
			return [self.resolve_memory(v) for v in value]
		if hasattr(value, '__dict__'):
			return ClassMemory(value, self)

def show_mem_name(loc):
	return 'mem_' + loc

class MemoryLocation:
	def __init__(self, loc):
		self.loc = loc

	def __repr__(self):
		return show_mem_name(str(self.loc))

class FunctionBinding:
	def __init__(self, fndef):
		self.fndef = fndef

	def show(self, name):
		return self.fndef.show_with_name(name) + ['\n']

class ClassMemory:
	def __init__(self, value, nm):
		self.value = value
		self.class_name = value.__class__.__name__
		self.nm = nm

	def __repr__(self):
		value = self.value
		nm = self.nm
		bindings = {k:nm.resolve_memory(v) for k,v in vars(value).items()}
		return repr(bindings)

class NameScope:
	def __init__(self, program):
		self.names = {}
		self.scope_number = 0
		self.program = program
		self.names_ordered = []

	def _bind(self, name, val):
		if name not in self.names:
			self.names_ordered.append(name)
		self.names[name] = val

	def create_binding(self, name):
		self._bind(name, Unbound)

	def bind(self, name, val):
		self._bind(name, self.program.name_model.resolve_memory(val))

	def set_number(self, num):
		self.scope_number = num

	def fix_conflicts(self, name):
		if re.match(r'.*_\d+', name):
			return '_' + name
		else:
			return name

	def show_name(self, name):
		name = self.fix_conflicts(name)

		if self.scope_number:
			return name + '_' + str(self.scope_number)
		else:
			return name

	def show_binding(self, name):
		value = self.names[name]
		if value is Unbound:
			return '# ' + self.show_name(name) + ' is unbound'
		elif isinstance(value, FunctionBinding):
			return value.show(self.show_name(name))
		else:
			return self.show_name(name) + ' = ' + self.show_val(name)

	def show_val(self, name):
		value = self.names[name]
		return self.program.show_value(value, '<function>')

	def show(self):
		names = self.names_ordered
		bindings = [self.show_binding(n) for n in names]
		return bindings

	def resolve_scope(self, name):
		return self

	def resolve_name(self, name):
		return self.resolve_scope(name).show_name(name)

class GlobalNameScope(NameScope):
	pass

class Unbound:
	pass