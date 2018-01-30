import instrumenter
import unittest

class TestBinaryOperation(unittest.TestCase):

	def test_binary_operation(self):
		src = """
5 + 6
		""".strip()

		expected = """
stepper_lib.binary_operation(5, 'Add', 6)
		""".strip()

		actual = instrumenter.instrument(src, "binary_operation").strip()

		print(actual)

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()