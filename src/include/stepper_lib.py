
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

