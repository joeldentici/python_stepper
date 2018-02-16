from reducible import Reducible

perform_op = {
	'Add': lambda x,y: x + y,
	'Mult': lambda x,y: x * y,
	'Sub': lambda x,y: x - y,
	'And': lambda x,y: x and y,
	'Or': lambda x,y: x or y,
	"Lt": lambda x,y: x < y,
	'Eq': lambda x,y: x == y,
	'Gt': lambda x,y: x > y,
	'GtE': lambda x,y: x >= y,
	'LtE': lambda x,y: x <= y,
	'NotEq': lambda x,y: x != y,
	'Is': lambda x,y: x is y,
	'IsNot': lambda x,y: x is not y,
	'In': lambda x,y: x in y,
	'NotIn': lambda x,y: x not in y,
}

show_op = {
	'Add': '+',
	'Mult': '*',
	'Sub': '-',
	'And': 'and',
	'Or': 'or',
	'Lt': '<',
	'Eq': '==',
	'Gt': '>',
	'GtE': '>=',
	'LtE': '<=',
	'NotEq': '!=',
	'Is': 'is',
	'IsNot': 'is not',
	'In': 'in',
	'NotIn': 'not in'
}

def showop(op):
	return " " + show_op[op] + " "

class BinaryOperation(Reducible):
	def __init__(self, program, op, left, right):
		super().__init__(program, 1)
		self.op = op
		self.left = self.program.wrap(left)
		self.right = self.program.wrap(right)
		self.state = 'initial'

	def reduce(self):
		left = self.left.reduce()
		right = self.right.reduce()
		self.value = perform_op[self.op](left, right)
		self.state = 'reduced'

		self.report()

		return self.value

	def show(self):
		if self.state == 'initial':
			return [self.left.show(), showop(self.op), self.right.show()]
		elif self.state == 'reduced':
			return self.program.show_value(self.value, '<unknown>')