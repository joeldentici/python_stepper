import instrumenter
import unittest

class TestExprStmt(unittest.TestCase):

	def test_expr_stmt(self):
		src = """
5 + 5
		""".strip()

		expected = """
stepper_lib.expr_stmt(5 + 5)
		""".strip()

		actual = instrumenter.instrument(src, "expr_stmt").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()