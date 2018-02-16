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
		raise NotImplementedError("No reduce method implemented for this Reducible")

	def show(self):
		'''
		show :: Reducible a -> ProgramState

		Gets the state of this reducible, which changes as it is reduced.
		'''
		raise NotImplementedError("No show method implemented for this Reducible")

	def report(self):
		'''
		report :: Reducible a -> ()

		Asks the program to report its state.
		'''
		self.program.report(self.granularity)