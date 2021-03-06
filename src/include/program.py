from statement_group import RootStatementGroup
from reducible import Reducible
from value import Value
from report_state import state_to_string
from name_model import NameModel
import re

'''
Program
written by Joel Dentici
on 02/15/2018

Represents the state of the program as the
stepper sees it.
'''

class Program:
	'''
	Program class definition
	'''
	def __init__(self, reporter, granularity):
		'''
		__init__ :: (Program, Reporter, int) -> ()

		Initializes the Program. The specified reporter is
		used to report reduction steps to the user. The specified
		granularity is used to determine when to report reduction steps.
		'''
		self.reporter = reporter
		self.statement_group_stack = [RootStatementGroup(self)]
		self.bindings = {}
		self.functions = {}
		self.old_info = None
		self.granularity = granularity
		self.reducible_stack = []
		self.name_model = NameModel(self)
		self.ws_pattern = re.compile(r'\s+')


	def evaluate_statement(self, stmt):
		'''
		evaluate_statement :: (Program, Statement a) -> a

		Activates a statement in the current statement group, effectively
		replacing raw statement source with a statement that can be reduced.

		The statement is then reduced and the resulting value is returned.
		'''
		self.active_statement_group().activate_statement(stmt)

		self.old_info = None

		return stmt.reduce()

	def report(self, granularity, end = False):
		'''
		report :: Program -> ()

		Reports reductions when they have occurred.

		Walks the state tree of the Program to produce a description
		of the current state.

		The new state is diffed against the old state, and if it differs,
		this indicates a reduction has been performed.

		If a reduction has been performed, the old state is updated to be the
		new state, and the reduction is reported.

		The granularity specified is used to determine whether to even compute the
		program state.
		'''
		if granularity < self.granularity:
			return

		new_info = self.root_statement_group().show()
		old_info = self.old_info
		if old_info != None:
			new_str = state_to_string(new_info)
			old_str = state_to_string(old_info)

			if self.different(new_str, old_str):
				self.reporter.report(old_info, new_info, end)

		self.old_info = new_info

	def different(self, n, o):
		# astor module wraps lines, so because we use that to generate
		# initial statements, they don't match with the initial "show" result
		# from our Reducible for the statement. So just remove whitespace as a
		# hack...
		n = re.sub(self.ws_pattern, '', n)
		o = re.sub(self.ws_pattern, '', o)
		return n != o


	def report_clear(self, granularity):
		self.old_info = None
		self.report(granularity)

	def active_statement_group(self):
		'''
		active_statement_group :: Program -> StatementGroup

		Returns the currently active statement group.
		'''
		return self.statement_group_stack[-1]

	def push_statement_group(self, group):
		'''
		push_statement_group :: (Program, StatementGroup) -> ()

		Activates a new statement group.
		'''
		self.statement_group_stack.append(group)

	def pop_statement_group(self):
		'''
		pop_statement_group :: Program -> ()

		Pops a statement group.
		'''
		self.statement_group_stack.pop()

	def root_statement_group(self):
		'''
		root_statement_group :: Program -> StatementGroup

		Returns the root statement group of the Program.
		'''
		return self.statement_group_stack[0]

	def store_function(self, py_fn, stepper_fn):
		self.functions[py_fn] = stepper_fn

	def has_function(self, fn):
		return self.is_hashable(fn) and fn in self.functions

	def show_value(self, value, fallback, added = False):
		#if not added:
		value = self.name_model.resolve_memory(value)

		if self.has_function(value):
			return self.functions[value].display()
		elif callable(value):
			return fallback
		else:
			return repr(value)

	def is_hashable(self, value):
		try:
			hash(value)
			return True
		except TypeError:
			return False

	def wrap(self, val):
		added = self.name_model.maybe_add_to_memory(val)

		if isinstance(val, Reducible):
			return val
		else:
			return Value(self, val, added)

	def start_reducing(self, red):
		self.reducible_stack.append(red)

	def is_reducing(self, red):
		return len(self.reducible_stack)\
		 and self.reducible_stack[-1] == red

	def stop_reducing(self, red):
		# handle early returns!
		while (not self.is_reducing(red)):
			self.reducible_stack.pop()

		self.reducible_stack.pop()