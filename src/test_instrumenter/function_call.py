import instrumenter
import unittest

class TestFunctionCall(unittest.TestCase):

	def test_function_call(self):
		src = """
def add(a, b):
	return a + b

add(10, 11)
		""".strip()

		expected = """
def add(a, b):
	return a + b


stepper_lib.function_call('add(10, 11)', add, 10, 11)
		""".strip()

		actual = instrumenter.instrument(src, "function_call").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()