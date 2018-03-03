from name_model import NameScope

class FunctionAppScope(NameScope):
	def __init__(self, program, info, args = []):
		super().__init__(program)
		self.info = info
		self.displays = {}
		self.parent_scope = info.parent_scope

		for b in self.info.as_bindings:
			self.create_binding(b)

		# set values for parameter bindings
		for i,b in enumerate(info.params):
			arg = args[i] if i < len(args) else None
			self.bind(b, arg)


	def resolve_scope(self, name):
		if name in self.info.gl_bindings:
			return self.program.name_model.scopes[0].resolve_scope(name)
		elif name in self.info.nl_bindings:
			return self.parent_scope.resolve_scope(name)
		elif name in self.info.as_bindings:
			return self
		elif name in self.info.params:
			return self
		else:
			return self.parent_scope.resolve_scope(name)