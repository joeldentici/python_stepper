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

def stmtToStr(node):
	return ast.Str(astor.to_source(node, '\t').strip())

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
		initialStmts = [stmtToStr(x) for x in node.body]
		initialStmts = ast.List(initialStmts, ast.Load())

		self.generic_visit(node)
		if not self.should_transform("function_def"):
			return node

		#names of parameters
		params = [ast.Str(arg.arg) for arg in node.args.args]
		params = ast.List(params, ast.Load())

		#name of function
		name = ast.Str(node.name)

		instrumented = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.function_def', ast.Load()),\
			[name, initialStmts, params, ast.Name(node.name, ast.Load())],\
			[],\
		))

		return [node, instrumented]

	def visit_Lambda(self, node):
		expr_src = ast.Str(astor.to_source(node, '\t').strip())

		self.generic_visit(node)
		if not self.should_transform("lambda_expression"):
			return node


		params = [ast.Str(arg.arg) for arg in node.args.args]
		params = ast.List(params, ast.Load())

		return ast.Call(\
			ast.Name('stepper_lib.lambda_expression', ast.Load()),\
			[expr_src, params, node],\
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
		self.generic_visit(node)
		if not self.should_transform("function_call"):
			return node

		func = node.func
		args = node.args

		return ast.Call(\
			ast.Name('stepper_lib.function_call', ast.Load()),\
			[func] + args,\
			[],\
		)

	def visit_Return(self, node):
		self.generic_visit(node)
		if not self.should_transform("return_statement"):
			return node

		node.value = ast.Call(\
			ast.Name('stepper_lib.return_statement', ast.Load()),\
			[node.value],\
			[],\
		)

		return node

	def visit_BinOp(self, node):
		self.generic_visit(node)
		if not self.should_transform("binary_operation"):
			return node

		left = node.left
		right = node.right

		return self.makeBinOp(node.left, node.op, node.right)

	def visit_BoolOp(self, node):
		self.generic_visit(node)
		if not self.should_transform('bool_operation'):
			return node

		left,right = node.values
		return self.makeBinOp(left, node.op, right)

	def visit_Compare(self, node):
		self.generic_visit(node)
		if not self.should_transform('compare_operation'):
			return node

		left = node.left
		acc = None
		for op,right in zip(node.ops, node.comparators):
			comp = self.makeBinOp(left, op, right)
			if acc == None:
				acc = comp
			else:
				acc = self.makeBinOperator(acc, 'And', comp)
			left = right


		return acc

	def makeBinOperator(self, left, op, right):
		return ast.Call(\
			ast.Name('stepper_lib.binary_operation', ast.Load()),\
			[left, ast.Str(op), right],\
			[]\
		)	

	def makeBinOp(self, left, op, right):
		op = op.__class__.__name__
		return self.makeBinOperator(left, op, right)


	def visit_Expr(self, node):
		self.generic_visit(node)
		if not self.should_transform("expr_stmt"):
			return node

		return ast.Expr(ast.Call(\
			ast.Name('stepper_lib.expr_stmt', ast.Load()),\
			[node.value],\
			[]\
		))

	def visit_Name(self, node):
		self.generic_visit(node)
		if not self.should_transform('ref'):
			return node

		if (node.ctx.__class__.__name__ == 'Load'):
			return ast.Call(\
				ast.Name('stepper_lib.ref', ast.Load()),\
				[ast.Str(node.id), node],\
				[]\
			)
		else:
			return node

	def visit_IfExp(self, node):
		self.generic_visit(node)
		if not self.should_transform('ifexpr'):
			return node

		return ast.Call(\
			ast.Name('stepper_lib.if_expr', ast.Load()),\
			[node.test, node.body, node.orelse],\
			[]\
		)
