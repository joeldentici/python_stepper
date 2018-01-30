import instrumenter
import unittest

class TestSimpleProg(unittest.TestCase):

	def test_simple_prog(self):
		src = """
def add(x):
	def f(y):
		return x + y
	return f

add(5)(10)
		""".strip()

		expected = """
abc(stepper_lib.ref('x', x))
		""".strip()

		actual = instrumenter.instrument(src).strip()

		print(actual)

		#self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()