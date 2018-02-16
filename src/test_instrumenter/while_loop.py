import instrumenter
import unittest

class TestWhileLoop(unittest.TestCase):

	def test_while_loop(self):
		src = """
while x < 3:
	a + b
	b
else:
	c
		""".strip()

		expected = """
stepper_lib.begin_while(['a + b', 'b'], ['c'])
while stepper_lib.while_test(x < 3):
	a + b
	b
	stepper_lib.loop_continue()
else:
	c
stepper_lib.end_group()
		""".strip()

		actual = instrumenter.instrument(src, "whileloop").strip()

		self.assertEqual(actual, expected)

if __name__ == '__main__':
	unittest.main()