from report_state import rename_statements
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
		self.set_statements(stmts)
		self.active = []

	def activate_statement(self, stmt):
		'''
		activate_statement :: (StatementGroup a, Reducible b) -> ()

		Activates the next statement in the group.
		'''
		self.freeze_last()

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
		active = self.show_active()
		original = self.show_original()
		return {
			"type": "statement_group",
			"statements": active + original
		}

	def enter(self):
		self.program.push_statement_group(self)

	def exit(self):
		self.freeze_last()

		# handle early returns!
		while (self.program.active_statement_group() != self):
			self.program.pop_statement_group()

		self.program.pop_statement_group()

	def reset(self):
		self.active = []
		self.rename_statements()

	def freeze_last(self):
		if len(self.active):
			self.active[-1] = StrStmt(self.active[-1].show())

	def set_statements(self, stmts):
		self.original = stmts
		self.renamed = self.original

	def has_statements(self):
		return len(self.original) > 0

	def ignore_stmt(self):
		cur_stmt = self.renamed[len(self.active)]
		self.activate_statement(StrStmt(cur_stmt))

	def show_active(self):
		return [x.show() for x in self.active[-1:]]

	def show_original(self):
		return self.renamed[len(self.active):]

	def rename_statements(self):
		self.renamed = rename_statements(self.program.name_model.current_scope, self.original)

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
		self.ended = False

	def show(self):
		'''
		show :: RootStatementGroup a -> ProgramState

		Gets the state of the root statement group.
		'''
		active = self.show_active()
		original = self.show_original()

		bindings = self.program.name_model.show()

		#ran_stmts = active[0:-1] if not self.ended else active
		#ran = self.show_boundary('ran') + ran_stmts
		ran = []

		memory = self.show_boundary('memory') + bindings


		current = self.show_boundary('running') + active[-1:]
		future = original
		rest = current + future if not self.ended else ['# Your Program Finished']


		return {
			"type": "statement_group",
			"statements": ran + memory + rest
		}

	def show_boundary(self, text):
		total_len = 50
		text = ' ' + text + ' '
		hashes = int((total_len - len(text)) / 2)
		hash_text = '#' * hashes
		return [hash_text + text + hash_text]

	def set_ended(self):
		self.ended = True