import ast
import sys
import astor
import copy

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

def get_source(node, marked = False):
	'''
	get_source :: ast -> string

	Mark the "name" nodes, such as "x" as "<@ x @>"

	This is used at runtime to rename variables before
	statements/expressions become "active". We could probably
	generate an expression tree from runtime calls like we do
	for the stepping itself, and reconstruct source at runtime,
	but this is the quick and dirty solution and it works.
	'''
	new_node = node
	if marked:
		orig_src = astor.to_source(node)
		new_node = MarkNames().visit(ast.parse(orig_src))

	new_src = ast.Str(astor.to_source(new_node, '   ').strip())
	return new_src

def find_bindings(node, first = True):
	recorder = RecordBindings(first)
	recorder.visit(node)

	return (recorder.found(), recorder.nlc, recorder.glb)

class RecordBindings(ast.NodeTransformer):
	def __init__(self, first):
		self.first = first
		self.names = set()
		self.nlc = set()
		self.glb = set()

	# ignore nested functions
	def visit_FunctionDef(self, node):
		if self.first:
			self.first = False
			self.generic_visit(node)

		return node

	def visit_Nonlocal(self, node):
		for ident in node.names:
			self.nlc.add(ident)
		return node

	def visit_Global(self, node):
		for ident in node.names:
			self.glb.add(ident)
		return node

	# assignments can introduce bindings
	def visit_Name(self, node):
		if (node.ctx.__class__.__name__ == 'Store'):
			self.names.add(node.id)
		return node

	def found(self):
		return self.names - (self.nlc | self.glb)

class MarkNames(ast.NodeTransformer):

	def visit_FunctionDef(self, node):
		return node

	def visit_LambdaExpression(self, node):
		return node

	def visit_Name(self, node):
		marking = {
			'Store': '@',
			'Load': '@'
		}

		ctx = node.ctx.__class__.__name__
		mark = marking[ctx]

		new_name = '<' + mark + ' ' + node.id + ' ' + mark + '>'
		return ast.Name(new_name, node.ctx)

class InstrumentSource(ast.NodeTransformer):
	def __init__(self, transformation):
		ast.NodeTransformer.__init__(self)

		self.used_transformation = transformation
		self.no_name = False

	def should_transform(self, transformation):
		return self.used_transformation == "" or \
		 self.used_transformation == transformation

	def visit_Module(self, node):
		initialStmts = self.initial(node.body, 'mark names')
		bindings,_,__ = find_bindings(node, False)

		self.generic_visit(node)
		if not self.should_transform("module"):
			return node

		import_runtime = ast.Import([ast.alias("stepper_lib", None)])

		set_initial = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.module_statements', ast.Load()),\
			[initialStmts, self.ast_list(sorted(bindings))],\
			[],\
		))

		end = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.end_program', ast.Load()),\
			[],\
			[],\
		))

		node.body = [import_runtime, set_initial] + node.body + [end]

		return node

	def visit_FunctionDef(self, node):
		initialStmts = self.initial(node.body)
		markedStmts = self.initial(node.body, 'mark names')
		assign_bindings, nonlocal_bindings, global_bindings = find_bindings(node)

		self.generic_visit(node)
		if not self.should_transform("function_def"):
			return node

		#names of parameters
		param_ids = [arg.arg for arg in node.args.args]

		params = self.ast_list(param_ids)
		nl_bindings = self.ast_list(sorted(nonlocal_bindings))
		gl_bindings = self.ast_list(sorted(global_bindings))
		as_bindings = self.ast_list(sorted(assign_bindings - set(param_ids)))

		#name of function
		name = ast.Str(node.name)

		instrumented = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.function_def', ast.Load()),\
			[name, initialStmts, params, ast.Name(node.name, ast.Load()),\
			 markedStmts, as_bindings, nl_bindings, gl_bindings],\
			[],\
		))

		return [node, instrumented]

	def ast_list(self, vals):
		return ast.List([ast.Str(x) for x in vals], ast.Load())

	def visit_Lambda(self, node):
		expr_src = get_source(node)
		expr_named = get_source(node.body, 'mark names')

		self.generic_visit(node)
		if not self.should_transform("lambda_expression"):
			return node


		params = [ast.Str(arg.arg) for arg in node.args.args]
		params = ast.List(params, ast.Load())

		return ast.Call(\
			ast.Name('stepper_lib.lambda_expression', ast.Load()),\
			[expr_src, params, node, expr_named],\
			[],\
		)

	def visit_Assign(self, node):
		assignment_str = get_source(node, 'mark names').s
		self.no_name = True
		node.targets = [self.visit(t) for t in node.targets]
		self.no_name = False
		node.value = self.visit(node.value)
		if not self.should_transform("assignment_statement"):
			return node

		# note, this should be done without string manipulation
		end = assignment_str.index(' =')
		target_str = assignment_str[0:end]

		targets = node.targets
		value = node.value

		node.value = ast.Call(\
			ast.Name('stepper_lib.assignment_statement', ast.Load()),\
			[ast.Str(target_str), value],\
			[],\
		)

		return self.make_assign(node)

	def make_assign(self, node):
		report = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.report', ast.Load()),\
			[ast.Num(1)],\
			[],\
		))

		return [node, report]

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
		if self.no_name:
			return node

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

	def initial(self, body, marked = False):
		return ast.List([get_source(x, marked) for x in body], ast.Load())

	def visit_If(self, node):
		initial_body = self.initial(node.body, 'mark names')
		initial_else = self.initial(node.orelse, 'mark names')
		self.generic_visit(node)
		if not self.should_transform('ifstmt'):
			return node

		new_test = ast.Call(\
			ast.Name('stepper_lib.begin_if', ast.Load()),\
			[node.test, initial_body, initial_else],\
			[]\
		)

		# to call after end of if statement (after taken branch's block runs)
		end = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.end_group', ast.Load()),\
			[],\
			[],\
		))

		new_node = ast.If(new_test, node.body, node.orelse)

		return [new_node, end]

	def visit_While(self, node):
		initial_body = self.initial(node.body, 'mark names')
		initial_else = self.initial(node.orelse, 'mark names')
		self.generic_visit(node)
		if not self.should_transform('whileloop'):
			return node

		initialize = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.begin_while', ast.Load()),\
			[initial_body, initial_else],\
			[]\
		))

		new_test = ast.Call(\
			ast.Name('stepper_lib.while_test', ast.Load()),\
			[node.test],\
			[]\
		)

		# to call after end of if statement (after taken branch's block runs)
		end = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.end_group', ast.Load()),\
			[],\
			[],\
		))

		# next iteration
		loop_continue = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.loop_continue', ast.Load()),\
			[],\
			[],\
		))

		# after each iteration of the body, we need to end.
		new_body = node.body

		new_node = ast.While(new_test, new_body, node.orelse)

		# we can put end here because the test will start the
		# block again!
		return [initialize, new_node, end]

	def ignore_stmt(self, t, node):
		if not self.should_transform(t):
			return node

		ignore = ast.Expr(ast.Call(\
			ast.Name('stepper_lib.ignore_stmt', ast.Load()),\
			[],\
			[],\
		))

		return [node, ignore]

	def visit_Attribute(self, node):
		if self.no_name:
			return node

		self.generic_visit(node)
		if not self.should_transform('attr'):
			return node

		if (node.ctx.__class__.__name__ == 'Load'):
			return ast.Call(\
				ast.Name('stepper_lib.attribute', ast.Load()),\
				[node.value, ast.Str(node.attr)],\
				[]\
			)
		else:
			return node

	def visit_Nonlocal(self, node):
		return self.ignore_stmt('nonlocal', node)

	def visit_Global(self, node):
		return self.ignore_stmt('global', node)

	def visit_Pass(self, node):
		return self.ignore_stmt('pass', node)

	def visit_Continue(self, node):
		return self.ignore_stmt('continue', node)

	def visit_Break(self, node):
		return self.ignore_stmt('break', node)

	def visit_AugAssign(self, node):
		return self.ignore_stmt('aug_assign', node)

	def visit_For(self, node):
		return self.ignore_stmt('for', node)

	def visit_ClassDef(self, node):
		return self.ignore_stmt('classdef', node)

	def visit_List(self, node):
		return node

	def visit_Dict(self, node):
		return node

	def visit_DictComp(self, node):
		return node

	def visit_SetComp(self, node):
		return node

	def visit_ListComp(self, node):
		return node

	def visit_Tuple(self, node):
		return node