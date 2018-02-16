import instrumenter
import unittest

class TestIfStmt(unittest.TestCase):

	def test_if_stmt(self):
		src = """
if x > 7:
	return 5
else:
	return 10
		""".strip()

		expected = """
if stepper_lib.begin_if(x > 7, ['return 5'], ['return 10']):
	return 5
else:
	return 10
stepper_lib.end_group()
		""".strip()

		actual = instrumenter.instrument(src, "ifstmt").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()