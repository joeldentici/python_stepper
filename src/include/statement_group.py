'''
StatementGroup
written by Joel Dentici
on 02/15/2018

Represents a group of statements that run in sequence.
'''

class StatementGroup:
	'''
	StatementGroup class definition
	'''
	def __init__(self, program, stmts):
		'''
		__init__ :: (StatementGroup, Program, [string]) -> ()

		Initializes the StatementGroup.
		'''
		self.program = program
		self.original = stmts
		self.active = []

	def activate_statement(self, stmt):
		'''
		activate_statement :: (StatementGroup a, Reducible b) -> ()

		Activates the next statement in the group.
		'''
		self.active.append(stmt)

	def show(self):
		'''
		show :: StatementGroup a -> ProgramState

		Gets the state of this group, which changes as its statements run.
		'''
		raise NotImplementedError("No show method implemented for this StatementGroup")

	def base_show(self):
		'''
		base_show :: StatementGroup a -> ProgramState

		Returns a list of ProgramState
		'''
		active = [x.show() for x in self.active]
		original = self.original[len(self.active):]
		return {
			"type": "statement_group",
			"statements": active + original
		}

	def enter(self):
		self.program.push_statement_group(self)

	def exit(self):
		# handle early returns!
		while (self.program.active_statement_group() != self):
			self.program.pop_statement_group()

		self.program.pop_statement_group()

	def reset(self):
		self.active = []

	def set_statements(self, stmts):
		self.original = stmts

	def has_statements(self):
		return len(self.original) > 0

	def ignore_stmt(self):
		cur_stmt = self.original[len(self.active)]
		self.activate_statement(StrStmt(cur_stmt))


class StrStmt:
	def __init__(self, stmt):
		self.stmt = stmt

	def show(self):
		return self.stmt


class RootStatementGroup(StatementGroup):
	'''
	RootStatementGroup class definition
	'''
	def __init__(self, program):
		'''
		__init__ :: (RootStatementGroup a, Program) -> ()

		Initializes the RootStatementGroup.
		'''
		super().__init__(program, [])

	def show(self):
		'''
		show :: RootStatementGroup a -> ProgramState

		Gets the state of the root statement group.
		'''
		return self.base_show()