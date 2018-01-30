import instrumenter
import unittest

class TestLambdaExpression(unittest.TestCase):

	def test_lambda_expression(self):
		src = """
lambda x,y: x + y
		""".strip()

		expected = """
stepper_lib.lambda_expression('(lambda x, y: x + y)', ['x', 'y'], lambda x,
    y: x + y)
		""".strip()

		actual = instrumenter.instrument(src, "lambda_expression").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()