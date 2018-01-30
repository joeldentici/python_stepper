import re

'''
stepper_lib
written by Joel Dentici
on 01/22/2018

The runtime library for the stepper. The
instrumented program calls the procedures in
this library, which report reduction steps of
the original program, block for input, and then
return the result of the reduction. Since Python is
strictly evaluated, every reduction step results in a value.
'''

class CommandlineReporter:
	def __init__(self):
		pass

	def report(self, val):
		BOLD = '\033[1m'
		ENDC = '\033[0m'
		YELLOW = '\033[93m'

		START = BOLD + YELLOW

		val = re.sub(
			r"(.*)\(\*\)(.*)\(\*\)(.*)",
			r"\1" + START + r"\2" + ENDC + r"\3",
			val,
			flags=re.DOTALL
		)

		print(val)
		input()

class ProgramContext:
	def __init__(self, reporter):
		self.reporter = reporter
		self.rootStmt = None
		self.knownFuncs = {}
		self.active = []
		self.lastReport = None
		self.stmts = []


	def nextStatement(self, stmt):
		root = False
		if self.rootStmt == None:
			root = True
			self.rootStmt = stmt

		if len(self.active):
			self.active[-1].addStatement(stmt)

		self.stmts.append(stmt)

		stmt.accept(self)
		result = stmt.reduce()

		self.stmts.pop()

		if root:
			self.rootStmt = None

		return result

	def visit(self, stmt):
		pass

	def visit_FunctionDef(self, stmt):
		self.knownFuncs[stmt.fn] = stmt


	def report(self):
		value = self.rootStmt.show(0)
		# don't report the same state more than once
		if value != self.lastReport and self.notEmpty(value):
			self.lastReport = value
			self.reporter.report(value)

	def activeStatement(self):
		if len(self.stmts):
			return self.stmts[-1]
		else:
			return None

	def notEmpty(self, value):
		return value != '(*)(*)' and value != ''


def visit(visitor, obj):
	mName = 'visit'
	sName = 'visit_' + obj.__class__.__name__
	if hasattr(visitor, sName):
		mName = sName

	method = getattr(visitor,mName)

	return method(obj)

def makeExpr(ctx, v):
	if isinstance(v, Expression):
		return v

	return Value(ctx, v)

def val_show(v):
	return repr(v)

def indent(depth, value):
	lines = value.split("\n")
	indentation = '\t' * depth
	return "\n".join(indentation + x for x in lines)

class Statement:
	def __init__(self, context):
		self.context = context

	def accept(self, visitor):
		return visit(visitor, self)

	def reduce(self):
		raise Exception('Virtual reduce called!')

	def show(self, depth):
		raise Exception('Virtual show called!')

	def active(self, val):
		if self.context.activeStatement() == self:
			return '(*)' + val + '(*)'
		else:
			return val

class Expression:
	def __init__(self, context):
		self.context = context

	def accept(self, visitor):
		return visit(visitor, self)

	def reduce(self):
		raise Exception('Virtual reduce called!')

	def show(self, depth):
		raise Exception('Virtual show called!')

class FunctionDef(Statement):
	def __init__(self, context, name, stmts, params, fn):
		Statement.__init__(self, context)
		self.name = name
		self.stmts = stmts
		self.params = params
		self.fn = fn

	def reduce(self):
		self.context.report()

	def show(self, depth):
		return self.active('')

class LambdaExpression(Expression):
	def __init__(self, context):
		Expression.__init__(self, context)

class AssignmentStatement(Statement):
	def __init__(self, context):
		Statement.__init__(self, context)

class FunctionCall(Expression):
	def __init__(self, context, fn, args):
		Expression.__init__(self, context)
		self.fn = fn
		self.args = [makeExpr(self.context, x) for x in args]
		self.result = None
		self.seenStatements = []
		self.step = 'show_call'
		self.called = self.fn.show(0)

	def addStatement(self, stmt):
		self.seenStatements.append(stmt)

	def reduce(self):
		# evaluate arguments
		fn = self.fn.reduce()
		args = []
		for arg in self.args:
			args.append(arg.reduce())

		# show evaluation of function if we know about it
		if fn in self.context.knownFuncs:
			info = self.context.knownFuncs[fn]
			self.params = info.params
			self.allStatements = info.stmts
			self.name = info.name
			self.step = 'user_function'
			self.context.report()

		# make function call
		self.context.active.append(self)
		self.result = fn(*args)
		self.context.active.pop()
		self.context.report()

		return self.result

	def show(self, depth):
		if self.result != None:
			if self.result in self.context.knownFuncs:
				return self.context.knownFuncs[self.result].name
			else:
				return val_show(self.result)

		if self.step == 'show_call':
			return self.fn.show(0) + '(' + ', '.join(a.show(0) for a in self.args) + ')'

		if self.step == 'user_function':
			header = 'def ' + self.name + '(' + ', '.join(self.showArg(p, a) for p, a in zip(self.params, self.args)) + '):'
			seen = '\n'.join(self.showStmt(x, i, depth) for i,x in enumerate(self.seenStatements))
			num = len(self.seenStatements)
			rest = '\n'.join(indent(depth + 1, x) for x in self.allStatements[num:])

			if len(seen):
				seen = '\n' + seen
			if len(rest):
				rest = '\n' + rest

			return '<@\n' + indent(depth, header) + seen + rest + '\n' + indent(depth, '@>')

	def showArg(self, p, a):
		return p + '=' + a.show(0)

	def showStmt(self, x, i, depth):
		val = x.show(depth + 1)
		default = indent(depth + 1, self.allStatements[i])
		if val == '(*)(*)':
			return '(*)' + default + '(*)'
		elif val == '':
			return default
		else:
			return val


class ReturnStatement(Statement):
	def __init__(self, context, value):
		Statement.__init__(self, context)
		self.value = makeExpr(context, value)

	def reduce(self):
		result = self.value.reduce()
		return result

	def show(self, depth):
		return self.active(indent(depth, 'return ' + self.value.show(depth)))


class BinaryOperation(Expression):
	def __init__(self, context, op, left, right):
		Expression.__init__(self, context)
		self.left = makeExpr(context, left)
		self.op = op
		self.right = makeExpr(context, right)
		self.value = None

	def reduce(self):
		ops = {
			'Add': lambda x,y: x + y,
			'Mult': lambda x,y: x * y
		}

		left = self.left.reduce()
		right = self.right.reduce()
		self.value = ops[self.op](left, right)
		self.context.report()

		return self.value

	def show(self, depth):
		ops = {
			'Add': ' + ',
			'Mult': ' * '
		}

		if self.value != None:
			return val_show(self.value)
		else:
			return self.left.show(depth) + ops[self.op] + self.right.show(depth)


class ExprStatement(Statement):
	def __init__(self, context, expr):
		Statement.__init__(self, context)
		self.expr = expr

	def reduce(self):
		return self.expr.reduce()

	def show(self, depth):
		return self.active(indent(depth, self.expr.show(depth)))

class Value(Expression):
	def __init__(self, context, value):
		Expression.__init__(self, context)
		self.value = value

	def reduce(self):
		return self.value

	def show(self, depth):
		return val_show(self.value)

class Reference(Expression):
	def __init__(self, context, id, value):
		Expression.__init__(self, context)
		self.id = id
		self.value = value
		self.reduced = False

	def reduce(self):
		self.reduced = True
		self.context.report()
		return self.value

	def show(self, depth):
		if self.reduced and not callable(self.value):
			return val_show(self.value)
		else:
			return self.id




context = None
def initialize(reporter):
	global context
	'''
	initialize :: Reporter -> ()

	Initialize the program context with a
	reporter, which is used to interact with
	the user.
	'''
	context = ProgramContext(reporter)

def function_def(name, initial_src, params, fn):
	'''
	function_def :: (string, [string], [string], Function) -> ()

	Occurs when a function definition is finished
	'''
	context.nextStatement(FunctionDef(context, name, initial_src, params, fn))

def assignment_statement(lval, value):
	'''
	assignment_statement :: (Ref, Expression a) -> a

	Occurs before an assignment happens (ie, this is the expression of an
	assignment)
	'''
	return context.nextStatement(AssignmentStatement(context, lval, value))

def return_statement(value):
	'''
	return_statement :: Expression a -> a

	Occurs before a return happens (ie, this is the expression of a return)
	'''
	return context.nextStatement(ReturnStatement(context, value))

def lambda_expression(initial_src, params, fn):
	'''
	lambda_expression :: Function a -> LambdaExpression a

	Wraps a lambda expression
	'''
	return LambdaExpression(context, initial_src, params, fn)

def function_call(fn, *args):
	'''
	function_call :: (Function a, [any]) -> FunctionCall a

	Wraps a function call
	'''
	return FunctionCall(context, fn, args)

def binary_operation(left, op, right):
	'''
	binary_operation :: (Expression a, string, Expression a) -> BinaryOperation a

	Wraps a binary operation
	'''
	return BinaryOperation(context, op, left, right)

def expr_stmt(expr):
	'''
	expr_statement :: Expression a -> ()

	Wraps an expression as statement
	'''
	context.nextStatement(ExprStatement(context, expr))

def ref(id, value):
	'''
	'''
	return Reference(context, id, value)

# This should be done by the instrumenter at a later time
# to allow specifying the reporter as cmd line argument
initialize(CommandlineReporter())

'''
known_funcs = {}
activated = []

def function_def(src, fn):
	known_funcs[fn] = src

def lambda_expression(src, fn):
	known_funcs[fn] = src
	return fn

def assignment_statement(lval, value):
	show(reduction(assign(lval, value)))
	return value

def function_call(src, fn, *args):
	if fn in known_funcs:
		activated.append(ActivationRecord(src, fn, args))

	result = fn(*args)

	activated.pop()

	return result

def return_statement(src, value):
	show(reduction('return ' + str(value)))
	return value

def binary_operation(src, left, op, right):
	operations = {
		'Add': lambda x, y: x + y,
		'Sub': lambda x, y: x - y,
		'Mult': lambda x, y: x * y,
	}

	display = {
		'Add': '+',
		'Sub': '-',
		'Mult': '*'
	}

	result = operations[op](left, right)

	reduction_part = reduction(str(left) + ' ' + display[op] + ' ' + str(right))
	reduction_full = reduction_part + ' -> ' + statement(str(result))

	show(reduction_full)

	return result

	

def reduction(stmt):
	active = activated[-1]

	red = statement(active.src) + ' -> ' + statement(stmt)

	return red

def statement(stmt):
	return '<@ ' + stmt + ' @>'

def assign(lval, value):
	return lval + ' = ' + str(value)

def show(val):
	print(val)
	input()


class ActivationRecord:
	def __init__(self, src, fn, args):
		self.src = src
		self.fn = fn
		self.args = args

'''