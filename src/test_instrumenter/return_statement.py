import instrumenter
import unittest

class TestReturnStatement(unittest.TestCase):

	def test_return_statement(self):
		src = """
def add(x, y):
	if x > y:
		return x + y
	else:
		return x - y
		""".strip()

		expected = """
def add(x, y):
	if x > y:
		return stepper_lib.return_statement(x + y)
	else:
		return stepper_lib.return_statement(x - y)
		""".strip()

		actual = instrumenter.instrument(src, "return_statement").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()