import instrumenter
import unittest

class TestFunctionDef(unittest.TestCase):

	def test_function_def(self):
		src = """
def add(x, y):
	return x + y
		""".strip()

		expected = """
def add(x, y):
	return x + y


stepper_lib.function_def('add', ['return x + y'], ['x', 'y'], add)
		""".strip()

		actual = instrumenter.instrument(src, "function_def").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()