import instrumenter
import unittest

class TestSimpleProg(unittest.TestCase):

	def test_simple_prog(self):
		src = """
(lambda x: x + 1)(5)
		""".strip()

		expected = """
abc(stepper_lib.ref('x', x))
		""".strip()

		actual = instrumenter.instrument(src).strip()

		print(actual)

		#self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()