
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

def function_def(src, fn):
	pass

def lambda_expression(src, fn):
	return fn

def assignment_statement(src, value):
	return value

def function_call(src, fn, *args):
	return fn(*args)

def return_statement(src, value):
	return value