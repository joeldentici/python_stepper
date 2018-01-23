import ast
import sys
import astor

'''
instrumenter
written by Joel Dentici
on 01/22/2018

Instruments the user's Python script so that
when evaluated, it is stepped through by the
stepper. The 'stepper_lib' include module is
added to the top of the instrumented script as
an import.
'''


def instrument(src, transformation = ""):
	'''
	instrument :: string -> string

	Parses the user's source code, instruments
	it, and then generates and returns the instrumented
	source code. 
	'''
	# source code -> ast
	node = ast.parse(src)

	# original ast -> instrumented ast
	new_node = InstrumentSource(transformation).visit(node)

	# instrumented ast -> instrumented source code
	instrumented_src = astor.to_source(new_node, '\t')

	# add import of stepper_lib
	return instrumented_src


class InstrumentSource(ast.NodeTransformer):
	def __init__(self, transformation):
		ast.NodeTransformer.__init__(self)

		self.used_transformation = transformation

	def should_transform(self, transformation):
		return self.used_transformation == "" or \
		 self.used_transformation == transformation

	def visit_Module(self, node):
		self.generic_visit(node)
		if not self.should_transform("module"):
			return node

		import_runtime = ast.Import([ast.alias("stepper_lib", None)])

		node.body = [import_runtime] + node.body

		return node

	def visit_FunctionDef(self, node):
		expr_src = ast.Str(astor.to_source(node, '\t').strip())

		self.generic_visit(node)
		if not self.should_transform("function_def"):
			return node

		instrumented = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.function_def', ast.Load()),\
			[expr_src, ast.Name(node.name, ast.Load())],\
			[],\
		))

		return [node, instrumented]

	def visit_Lambda(self, node):
		expr_src = ast.Str(astor.to_source(node, '\t').strip())

		self.generic_visit(node)
		if not self.should_transform("lambda_expression"):
			return node

		return ast.Call(\
			ast.Name('stepper_lib.lambda_expression', ast.Load()),\
			[expr_src, node],\
			[],\
		)

	def visit_Assign(self, node):
		self.generic_visit(node)
		if not self.should_transform("assignment_statement"):
			return node

		# note, this should be done without string manipulation
		assignment_str = astor.to_source(node)
		end = assignment_str.index(' =')
		target_str = assignment_str[0:end]

		targets = node.targets
		value = node.value

		node.value = ast.Call(\
			ast.Name('stepper_lib.assignment_statement', ast.Load()),\
			[ast.Str(target_str), value],\
			[],\
		)

		return node

	def visit_Call(self, node):
		expr_src = ast.Str(astor.to_source(node, '\t').strip())

		self.generic_visit(node)
		if not self.should_transform("function_call"):
			return node

		func = node.func
		args = node.args

		return ast.Call(\
			ast.Name('stepper_lib.function_call', ast.Load()),\
			[expr_src, func] + args,\
			[],\
		)

	def visit_Return(self, node):
		expr_src = ast.Str(astor.to_source(node, '\t').strip())

		self.generic_visit(node)
		if not self.should_transform("return_statement"):
			return node

		node.value = ast.Call(\
			ast.Name('stepper_lib.return_statement', ast.Load()),\
			[expr_src, node.value],\
			[],\
		)

		return node