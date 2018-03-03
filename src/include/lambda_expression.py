from reducible import Reducible
from report_state import rename_statement
from function_app_scope import FunctionAppScope

class LambdaExpression(Reducible):
	def __init__(self, program, src, params, fn, named_src):
		super().__init__(program, 1)
		self.program.store_function(fn, self)
		self.src = src
		self.fn = fn
		self.params = params
		self.named_src = named_src
		self.as_bindings = []
		self.gl_bindings = []
		self.nl_bindings = []
		self.parent_scope = program.name_model.current_scope
		self.fake_scope = FunctionAppScope(program, self)
		self.renamed = rename_statement(self.fake_scope, named_src)

	def do_reduce(self):
		return self.fn

	def do_show(self):
		return ['(', 'lambda ', self.show_params(), self.show_body(), ')']

	def show_params(self):
		return ", ".join(self.params) + ': '

	def show_body(self):
		return self.renamed

	def display(self):
		return "".join(self.show())