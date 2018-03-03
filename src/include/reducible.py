'''
Reducible
written by Joel Dentici
on 02/15/2018

Represents reducible components of a program.
'''

class Reducible:
	'''
	Reducible class definition
	'''
	def __init__(self, program, granularity):
		'''
		__init__ :: (Reducible a, Program, int) -> ()

		Initializes the Reducible.
		'''
		self.program = program
		self.granularity = granularity

	def reduce(self):
		'''
		reduce :: Reducible a -> a

		Performs a reduction on a Reducible component of the user's
		program.

		Implementations have the opportunity to ask the program to report
		its state at any time.
		'''
		self.program.start_reducing(self)
		result = self.do_reduce()
		self.program.stop_reducing(self)
		return result

	def show(self):
		'''
		show :: Reducible a -> ProgramState

		Gets the state of this reducible, which changes as it is reduced.
		'''
		state = self.do_show()
		if (self.program.is_reducing(self)):
			return {
				"type": "active_component",
				"value": state
			}
		else:
			return state

	def report(self):
		'''
		report :: Reducible a -> ()

		Asks the program to report its state.
		'''
		self.program.report(self.granularity)

	def do_reduce(self):
		raise NotImplementedError("No do_reduce method implemented for this Reducible")

	def do_show(self):
		raise NotImplementedError("No do_show method implemented for this Reducible")

	def __getitem__(self, key):
		return Indexer(self.program, self.granularity, self, self.program.wrap(key))

class Indexer(Reducible):
	def __init__(self, program, granularity, on, key):
		super().__init__(program, granularity)
		self.key = key
		self.on = on
		self.state = 'initial'

	def do_reduce(self):
		self.report()
		val = self.on.reduce()
		self.value = val[self.key.reduce()]
		self.state = 'reduced'
		return self.value

	def do_show(self):
		if self.state == 'initial':
			return [self.on.show(), '[', self.key.show(), ']']
		elif self.state == 'reduced':
			return self.program.show_value(self.value, '<unknown>')