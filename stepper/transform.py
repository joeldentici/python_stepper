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
	* Inside of the function def
	* Inside of lambdas as well
	* Show args and return values

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
	def visit_FunctionDef(self, node):
		#simple POC right now
		#just print a function's name when it is called

		#extract info from function def
		fn = node.name 
		#this is only getting normal args, not keyword arguments
		args = node.args.args
		body = node.body

		#argNames = []
		argNames = [ast.Str(arg.id) for arg in args]
		argVals = args
		newEnv = ast.Dict(argNames, argVals)


		pushEnv = ast.Call(ast.Name('stepper_lib.push_env', ast.Load()), [ast.Str(fn), newEnv], [], None, None)

		retVal = ast.Assign([ast.Name('__step_ret', ast.Store())], body[-1].value)

		logRet = ast.Call(ast.Name('stepper_lib.pop_env', ast.Load()), [ast.Str(fn), ast.Name('__step_ret', ast.Load())], [], None, None)


		retStmt = ast.Return(ast.Name('__step_ret', ast.Load()))


		#print the function call line, then evaluate the body in resulting function
		stmts = [ast.Expr(pushEnv)] + body[0:-2] + [retVal, ast.Expr(logRet), retStmt]
		wrapped = ast.FunctionDef(fn, node.args, stmts, node.decorator_list)

		return wrapped

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

#transform stdin and print it to stdout.
print 'import stepper_lib'
print transform(sys.stdin.read())
print 'stepper_lib.print_state()'