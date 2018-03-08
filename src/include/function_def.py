from reducible import Reducible
from report_state import rename_statements
from function_app_scope import FunctionAppScope
from name_model import FunctionBinding

class FunctionDef(Reducible):
	def __init__(self, program, name, stmts, params, fn,\
	 named_stmts, as_bindings, nl_bindings, gl_bindings):
		super().__init__(program, 1)
		self.program.store_function(fn, self)
		self.name = name
		self.stmts = stmts
		self.params = params
		self.fn = fn
		self.named_stmts = named_stmts
		self.as_bindings = as_bindings
		self.nl_bindings = nl_bindings
		self.gl_bindings = gl_bindings
		self.parent_scope = program.name_model.current_scope
		self.parent_scope.bind(self.name, FunctionBinding(self))
		self.fake_scope = FunctionAppScope(program, self)
		self.renamed = rename_statements(self.fake_scope, named_stmts)

	def do_reduce(self):
		return self.fn

	def do_show(self):
		return self.show_with_name(self.name)

	def show_with_name(self, name):
		return ['def ', name, '(', self.show_params(), '):\n', self.show_body()]

	def show_params(self):
		return ", ".join(self.params)

	def show_body(self):
		return {
			"type": "block",
			"value": {
				"type": "statement_group",
				"statements": self.renamed
			}
		}

	def display(self):
		return self.parent_scope.show_name(self.name)