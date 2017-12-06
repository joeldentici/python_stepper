import ast
import sys
import astor

'''
Python stepper AST transformation POC

Proof of concept modifying a Python AST to change program
semantics. We will be doing this to augment programs with an
algebraic stepper later.

Next Steps:

1. Add data structure to store history of stack calls.
	* Inside of lambdas as well (not done)
		* Abstract out the transformation so it returns
		the items needed to construct the modified AST node
		and then create two visitors, one for function def,
		one for lambdas

'''

'''
AddEnv :: NodeTransformer

A node transformer. Transforms Python functions
to record the environment they were called in and
the value that they return with the stepper library.

This involves extending the environment in an immutable
way at each call site (actually inside the function) so
that we can see the state of all variables on the 'stack'
at each function application.
'''
class AddEnv(ast.NodeTransformer):
	def __init__(self):
		ast.NodeTransformer.__init__(self)
		#stack of function definition names being transformed
		self.fns = []

	def visit_FunctionDef(self, node):
		#store name while we are transforming this definition
		self.fns.append(node.name)

		#visit children too!
		self.generic_visit(node)

		#extract info from function def
		fn = node.name 
		#this is only getting normal args, not keyword arguments
		args = node.args.args
		body = node.body

		#construct the environment of the application
		argNames = [ast.Str(arg.arg) for arg in args]
		argVals = args
		newEnv = ast.Dict(argNames, argVals)

		#push a function call onto stepper's call stack, this will record the *lexical* environment of
		#the application (so arguments and the closure environment will be in the reported environment)
		pushEnv = ast.Call(ast.Name('stepper_lib.push_call', ast.Load()), [ast.Name(fn, ast.Load()), newEnv], [], None, None)

		#create the new function definition
		stmts = [ast.Expr(pushEnv)] + body
		wrapped = ast.FunctionDef(fn, node.args, stmts, node.decorator_list, None)

		#store the environment this function was defined in
		close = ast.Call(ast.Name('stepper_lib.store_env', ast.Load()), [ast.Name(fn, ast.Load())], [], None, None)

		#replace the definition with the new definition and the call to store the env
		newNode = [wrapped, ast.Expr(close)]

		#no longer transforming this definition
		self.fns.pop()

		return newNode

	def visit_Return(self, node):
		#visit children
		self.generic_visit(node)

		#get name of function this statement is in
		fn = self.fns[-1]

		#record the return value with the stepper library, then return it.
		#we are careful to assign it to a temporary variable so we don't
		#evaluate the return expression more than once (which would be bad
		#if it had side effects)
		val = ast.Assign([ast.Name('__step_ret', ast.Store())], node.value)
		logRet = ast.Call(ast.Name('stepper_lib.pop_call', ast.Load()), [ast.Name(fn, ast.Load()), ast.Name('__step_ret', ast.Load())], [], None, None)
		retStmt = ast.Return(ast.Name('__step_ret', ast.Load()))

		return [val, ast.Expr(logRet), retStmt]


'''
transform :: string -> string

Parses an input Python program, runs it through the
transformer defined above, generates the resulting Python code, and
outputs it as a string.
'''
def transform(src):
	#parse source code to ast, transform ast
	node = ast.parse(src)
	new_node = AddEnv().visit(node)

	#generate output source code
	return astor.to_source(new_node)

#output the transformed program to stdout
print('import stepper_lib')
print(transform(sys.stdin.read()))
print('stepper_lib.print_call_history()')