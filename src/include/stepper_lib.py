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

from binary_operation import BinaryOperation
from program import Program
from function_def import FunctionDef
from function_call import FunctionCall
from lambda_expression import LambdaExpression
from return_statement import ReturnStatement
from expr_statement import ExprStatement
from identifier import Identifier
from commandline_reporter import CommandlineReporter
from if_expr import IfExpression
from if_stmt import IfStatement
from while_loop import WhileLoop
from assignment_statement import AssignmentStatement

context = None
def initialize(reporter):
	global context
	'''
	initialize :: Reporter -> ()

	Initialize the program context with a
	reporter, which is used to interact with
	the user.
	'''
	context = Program(reporter, 1)

def function_def(name, initial_src, params, fn, named_src, as_bindings, nl_bindings, gl_bindings):
	'''
	function_def :: (string, [string], [string], Function) -> ()

	Occurs when a function definition is finished
	'''
	context.evaluate_statement(FunctionDef(context, name, initial_src, params, fn,\
	 named_src, as_bindings, nl_bindings, gl_bindings))

def assignment_statement(lval, value):
	'''
	assignment_statement :: (Ref, Expression a) -> a

	Occurs before an assignment happens (ie, this is the expression of an
	assignment)
	'''
	#return context.evaluate_statement(AssignmentStatement(context, lval, value))
	return context.evaluate_statement(AssignmentStatement(context, lval, value))

def return_statement(value):
	'''
	return_statement :: Expression a -> a

	Occurs before a return happens (ie, this is the expression of a return)
	'''
	return context.evaluate_statement(ReturnStatement(context, value))

def lambda_expression(initial_src, params, fn, named_src):
	'''
	lambda_expression :: Function a -> LambdaExpression a

	Wraps a lambda expression
	'''
	return LambdaExpression(context, initial_src, params, fn, named_src)

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
	context.evaluate_statement(ExprStatement(context, expr))

def ref(id, value):
	'''
	'''
	return Identifier(context, id, value)

def if_expr(test, t, f):
	return IfExpression(context, test, t, f)

def begin_if(test, t, f):
	return context.evaluate_statement(IfStatement(context, test, t, f))

def end_group():
	context.active_statement_group().cleanup()

def loop_continue(explicit = False):
	context.active_statement_group().loop_continue(explicit)

def loop_break():
	context.active_statement_group().loop_break()

def begin_while(t, f):
	context.evaluate_statement(WhileLoop(context, t, f))

def while_test(test):
	return context.active_statement_group().while_test(test)

def ignore_stmt():
	context.active_statement_group().ignore_stmt()

def module_statements(stmts, bindings):
	context.active_statement_group().set_statements(stmts)
	for b in bindings:
		context.name_model.current_scope.create_binding(b)

def end_program():
	context.report_clear(1)
	context.active_statement_group().set_ended()
	context.report(1, True)

def report(granularity):
	context.report(granularity)
	context.reducible_stack.pop()

# This should be done by the instrumenter at a later time
# to allow specifying the reporter as cmd line argument
initialize(CommandlineReporter())