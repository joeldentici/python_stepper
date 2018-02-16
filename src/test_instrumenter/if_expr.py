import instrumenter
import unittest

class TestIfExpr(unittest.TestCase):

	def test_if_expr(self):
		src = """
5 if x > 7 else 10
		""".strip()

		expected = """
stepper_lib.if_expr(x > 7, 5, 10)
		""".strip()

		actual = instrumenter.instrument(src, "ifexpr").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()