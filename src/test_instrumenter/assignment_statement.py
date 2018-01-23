import instrumenter
import unittest

class TestAssignmentStatement(unittest.TestCase):

	def test_assignment_statement(self):
		src = """
x,y = (5, 6)
		""".strip()

		expected = """
x, y = stepper_lib.assignment_statement('x, y', (5, 6))
		""".strip()

		actual = instrumenter.instrument(src, "assignment_statement").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()